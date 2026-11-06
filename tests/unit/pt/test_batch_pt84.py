"""PT-84 : Battle Frontier, services et pointeurs de menus audités."""
import json
from pathlib import Path

import yaml

from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.dialogue_linewrap import line_widths
from src.core.fixed_tables import in_fixed_table
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt84_audit.json').read_text())
EXCEPTIONS = [47, 103, 117, 118, 119, 123, 130, 131, 132, 135]


def test_closed_manifest_protections_controls_and_budgets():
    manifest = next(row['offsets'] for row in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if row['id'] == 'PT-84')
    texts = entries()
    guards = {int(row['offset'], 16): row['expected'] for row in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert len(manifest) == 300
    assert [row['offset'] for row in AUDIT['entries']] == manifest
    assert [row['index'] for row in AUDIT['entries'] if row['status'] == 'exception'] == EXCEPTIONS
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert not in_fixed_table(offset)
        assert row['reason'] and row['scene']
        if row['status'] == 'exception':
            assert not row['references'] and offset not in texts and offset not in guards
            continue
        assert texts[offset] == guards[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(texts[offset].replace(r'\n', '\n'), strict=True)
        commands = lambda value: [c for c in _extract_control_sequences_from_raw(value) if c[0] != 0xFE]
        assert commands(raw) == commands(bytes.fromhex(row['source_hex']))
        assert len(raw) == row['encoded_bytes']
        assert line_widths(texts[offset].replace(r'\n', '\n')) == row['line_widths']
        assert max(row['line_widths']) <= row['max_width'] <= 208
        assert row['references']
        if row['layout'] == 'dialogue':
            for page in raw.split(b'\xfb'):
                assert page.split(b'\xfa')[0].count(b'\xfe') <= 1
                assert all(b'\xfe' not in part for part in page.split(b'\xfa')[1:])


def test_lottery_training_and_complete_tutorial_rules():
    rows = AUDIT['entries']
    assert '9999' in rows[142]['portuguese'] and '0' in rows[142]['portuguese']
    assert '9999' in rows[144]['portuguese']
    assert 'três turnos' in rows[107]['portuguese']
    assert '6' in rows[115]['portuguese']
    assert len(rows[107]['english_full']) > len(rows[107]['english'])
    assert len(rows[115]['english_full']) > len(rows[115]['english'])
    for index in (120, 121, 122, 124):
        assert '<0xFD><0x03>' in rows[index]['portuguese']
        assert '<0xFD><0x02>' in rows[index]['portuguese']
    assert rows[222]['portuguese'] == 'Lutador'
    assert rows[223]['portuguese'] == 'Voador'
    assert rows[229]['portuguese'] == 'Fogo'
    for index in list(range(248, 253)) + list(range(264, 291)):
        assert rows[index]['portuguese'] == rows[index]['english']


def test_finalizer_runs_after_repairs_and_font():
    patches = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert patches.count('batch_84') == 1
    assert all(patches.index(step) < patches.index('batch_84') for step in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'font', 'repoint_stale'))


def test_audit_matches_reference_sources():
    import re

    def read(path):
        return {int(m[1], 16): m[2] for line in path.read_text().splitlines()
                if (m := re.match(r'0x([0-9a-fA-F]+): ?(.*)', line))}

    english = read(ROOT / 'languages/en/combined_en.txt')
    french = read(ROOT / 'languages/fr/combined_fr.txt')
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['english'] == english.get(offset, '')
        assert row['french_reference'] == french.get(offset, '')
