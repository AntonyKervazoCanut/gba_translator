"""PT-81 : périmètre fermé, pages et règles des routes et missions."""
import json
from pathlib import Path

import yaml

from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.dialogue_linewrap import line_widths
from src.core.fixed_tables import in_fixed_table
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt81_audit.json').read_text())


def test_manifest_protections_controls_and_budgets():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-81')
    texts = entries()
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert len(manifest) == 299
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert not in_fixed_table(offset)
        if row['status'] == 'exception':
            assert row['index'] in (11, 155)
            assert not row['references'] and row['reason']
            assert offset not in texts and offset not in guards
            continue
        text = texts[offset]
        assert text == guards[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(text.replace(r'\n', '\n'), strict=True)
        assert len(raw) == row['encoded_bytes']
        source = bytes.fromhex(row['source_hex'])[row.get('prefix_bytes', 0):]
        assert [c for c in _extract_control_sequences_from_raw(raw) if c[0] != 0xFE] == [
            c for c in _extract_control_sequences_from_raw(source) if c[0] != 0xFE]
        assert line_widths(text.replace(r'\n', '\n')) == row['line_widths']
        assert max(row['line_widths']) <= row['max_width']
        if row['index'] in (37, 148):
            assert raw.count(b'\xfe') <= 2  # Description de mission : trois lignes.
        elif row['index'] not in (35, 131, 158, 165, 182, 274):
            assert all(page.split(b'\xfa')[0].count(b'\xfe') <= 1 for page in raw.split(b'\xfb'))
            assert all(b'\xfe' not in part for page in raw.split(b'\xfb') for part in page.split(b'\xfa')[1:])
        assert row['references'] or row.get('consumer_references')


def test_tomb_mining_and_daily_challenge_rules():
    rows = {r['index']: r.get('portuguese', '').replace(r'\n', ' ') for r in AUDIT['entries']}
    assert 'Lutador' in rows[23] and 'Challenge Rock' in rows[23]
    assert 'Borrius III' in rows[35] and 'câmara funerária' in rows[35]
    assert '10 segundos' in rows[135] and 'menos de 15 segundos' in rows[135]
    assert '200000' in rows[183] and '45000' in rows[184]
    assert 'Voador' not in rows[219] and 'Dragão' in rows[219]
    assert 'Durant' in rows[223] and 'Heatmor' in rows[226]
    assert 'Seed Bomb' in rows[287] and 'Seed Bomb' in rows[288]
    assert 'INSETO' in rows[180] and 'RELÓGIO' in rows[274]
    assert all(rows[i].endswith('<0x00>') for i in range(110, 122))
    assert 'Hall of Fame' in rows[108]
    assert 'achado<0xFD><0x07>' in rows[152]
    assert 'Jan.' in rows[110] and 'Dez.' in rows[121]


def test_finalizer_follows_repairs():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_81') == 1
    assert all(steps.index(p) < steps.index('batch_81') for p in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))


def test_unlisted_names_and_native_quotes():
    rows = {r['index']: r.get('portuguese', '') for r in AUDIT['entries']}
    for row in AUDIT['entries'][67:102]:
        assert row['portuguese'] == row['english'].strip()
    for index in (124, 183, 184):
        raw = TextEncoder.encode_pokemon(rows[index].replace(r'\n', '\n'), strict=True)
        assert raw.count(b'\xb1') == raw.count(b'\xb2') == 1


def test_audit_matches_english_and_french_sources():
    """Empêche de valider un audit détaché des sources de référence."""
    import re

    def read_entries(path):
        return {int(m[1], 16): m[2] for line in path.read_text().splitlines()
                if (m := re.match(r'0x([0-9a-fA-F]+): ?(.*)', line))}

    english = read_entries(ROOT / 'languages/en/combined_en.txt')
    french = read_entries(ROOT / 'languages/fr/combined_fr.txt')
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['english'] == english.get(offset, '')
        assert row['french_reference'] == french.get(offset, '')
