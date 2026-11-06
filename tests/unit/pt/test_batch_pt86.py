"""PT-86 : périmètre fermé, Ring Challenge et missions d'Antisis."""
import json
import re
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_widths
from src.core.fixed_tables import in_fixed_table
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt86_audit.json').read_text())
ROWS = AUDIT['entries']
LIVE = [r for r in ROWS if r['status'] != 'exception']


def test_manifest_protections_controls_and_budgets():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-86')
    texts = entries()
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert len(manifest) == 299
    assert [r['offset'] for r in ROWS] == manifest
    assert len(LIVE) == 295
    for row in ROWS:
        offset = int(row['offset'], 16)
        assert not in_fixed_table(offset)
        assert row['reason'] and row['full_english']
        if row['status'] == 'exception':
            assert row['index'] in (89, 165, 206, 212)
            assert not row['references']
            assert offset not in texts and offset not in guards
            continue
        text = texts[offset]
        assert text == guards[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(text.replace(r'\n', '\n'), strict=True)
        assert len(raw) == row['encoded_bytes']
        assert raw[-1] == 255 and 255 not in raw[:-1]
        assert [c for c in commands(raw) if c != b'\xfe'] == [
            c for c in commands(bytes.fromhex(row['source_hex'])) if c != b'\xfe']
        assert line_widths(text.replace(r'\n', '\n')) == row['line_widths']
        assert max(row['line_widths']) <= row['max_width']
        assert row['references']
        if row['layout'] == 'mission':
            assert raw.count(b'\xfe') <= 2
        elif row['layout'] == 'dialogue':
            for page in raw.split(b'\xfb'):
                assert page.split(b'\xfa')[0].count(b'\xfe') <= 1
                assert all(b'\xfe' not in part for part in page.split(b'\xfa')[1:])


def test_sources_and_official_name_policy():
    def load(lang):
        return {int(m[1], 16): m[2] for line in (ROOT / f'languages/{lang}/combined_{lang}.txt').read_text().splitlines()
                if (m := re.match(r'0x([0-9a-fA-F]+): ?(.*)', line))}
    en, fr = load('en'), load('fr')
    for row in ROWS:
        offset = int(row['offset'], 16)
        assert row['english'] == en.get(offset, '')
        assert row['french_reference'] == fr.get(offset, '')
    for index in (*range(20), *range(23, 33), 94, 107, 178, 179, 279, 282):
        row = ROWS[index]
        raw = TextEncoder.encode_pokemon(row['portuguese'], strict=True)
        assert raw.hex() == row['source_hex']


def test_ring_challenge_and_gang_mission_rules():
    texts = {r['index']: re.sub(r'<0xF[AB]>|\\n', ' ', r.get('portuguese', '')) for r in ROWS}
    assert '50' in texts[36] and 'Regigigas' in texts[36] and 'Stall' in texts[36]
    assert all(name in texts[36] for name in ('Dynamax', 'Destiny Bond', 'Perish Song', 'Standard'))
    assert 'Frontier Card' in texts[37] and 'Battle Frontier' in texts[37]
    assert '99' in texts[57] and '100' in texts[58]
    assert '4000' in texts[83] and 'Return' in texts[92]
    assert 'Pikachu' in texts[86] and 'Route 8' in texts[86]
    assert 'Black Ferrothorn' in texts[245] and 'Science Society' in texts[245]
    assert 'Electrode' in texts[262] and 'Explosion' in texts[264]
    assert '20' in texts[202] and '0' in texts[202]
    assert 'data' in texts[203]


def test_finalizer_follows_all_generic_repairs():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_86') == 1
    assert all(steps.index(p) < steps.index('batch_86') for p in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))
