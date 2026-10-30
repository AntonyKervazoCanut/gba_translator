"""PT-76 : périmètre fermé, pages et règles des routes et missions."""
import json
from pathlib import Path

import yaml

from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.dialogue_linewrap import line_widths
from src.core.fixed_tables import in_fixed_table
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt76_audit.json').read_text())


def test_manifest_protections_controls_and_budgets():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-76')
    texts = entries()
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert len(manifest) == 299
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert not in_fixed_table(offset)
        if row['status'] == 'exception':
            assert row['index'] in (13, 21, 188, 228)
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
        if row['index'] in (107, 253, *range(114, 132)):
            assert raw.count(b'\xfe') <= 2  # Description de mission : trois lignes.
        else:
            assert all(page.split(b'\xfa')[0].count(b'\xfe') <= 1 for page in raw.split(b'\xfb'))
            assert all(b'\xfe' not in part for page in raw.split(b'\xfb') for part in page.split(b'\xfa')[1:])
        assert row['references'] or row.get('consumer_references')


def test_routes_missions_and_battle_rules():
    rows = {r['index']: r.get('portuguese', '').replace(r'\n', ' ') for r in AUDIT['entries']}
    assert 'Rock Climb' in rows[5] and 'Seaport City' in rows[5]
    assert 'Voador' in rows[18] and 'Levitate' in rows[18]
    assert '17 dos 18' in rows[108]
    assert all(type_name in rows[109] for type_name in ('Água', 'Voador', 'Sombrio', 'Mega Gyarados'))
    assert all('Hall of Fame' in rows[i] for i in range(114, 132))
    assert all(name in rows[i] for i, name in ((124, 'Terrestre'), (127, 'Venenoso')))
    assert 'Route 2 e da Route 15' in rows[176]
    assert 'Lutador' in rows[180]
    assert 'Batalha Dupla' in rows[164] and 'nocauteado' in rows[164]
    assert 'Keen Eye' in rows[172] and 'Precisão' in rows[172] and 'Evasão' in rows[172]
    assert 'Poções' in rows[219]
    assert [rows[i].split('>')[-1] for i in (249, 250, 251)] == ['Snivy', 'Tepig', 'Oshawott']
    assert 'Synchronize' in rows[280] and 'natureza' in rows[280]
    assert rows[215].count('<0xFA>') == 2 and 'Sticky<0xFA>Hold' in rows[215]


def test_finalizer_follows_repairs():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_76') == 1
    assert all(steps.index(p) < steps.index('batch_76') for p in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))


def test_unlisted_battle_name_and_native_quotes():
    rows = {r['index']: r.get('portuguese', '') for r in AUDIT['entries']}
    assert 'Sky Battle' in rows[12] and 'Batalha Aérea' not in rows[12]
    for index in (68, 137, 281):
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
