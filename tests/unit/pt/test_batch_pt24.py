"""PT-24 : périmètre exact, protections et contrat des fenêtres Borrius."""
import json
import re
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_width
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
ROWS = json.loads((ROOT / 'languages/pt/data/pt24_audit.json').read_text())['entries']


def test_manifest_protection_and_control_flow():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    manifest = next(b['offsets'] for b in batches if b['id'] == 'PT-24')
    protected = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    guards = {int(r['offset'], 16): r.get('expected_raw', r['expected']) for r in protected['entries']}
    texts = entries()
    assert [r['offset'] for r in ROWS] == manifest
    assert len(ROWS) == 288
    assert {s: sum(r['status'] == s for r in ROWS) for s in
            ('translated', 'verified', 'exception')} == {
                'translated': 243, 'verified': 12, 'exception': 33}
    for row in ROWS:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['source_hex']
        if row['status'] == 'exception':
            assert offset not in texts
            continue
        text = texts[offset]
        assert text == guards[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(text.replace(r'\n', '\n'), strict=True)
        assert len(raw) == row['encoded_bytes']
        assert raw[-1] == 0xFF and 0xFF not in raw[:-1]
        assert commands(raw) == commands(bytes.fromhex(row['source_hex']))
        measured = [line_width(line) for line in re.split(r'\\n|<0xFA>|<0xFB>', text)]
        assert measured == row['line_widths']
        assert max(measured) <= row['layout']['max_width']
        for page in text.split('<0xFB>'):
            assert page.count(r'\n') + 1 <= row['layout']['max_lines']


def test_objects_and_geography_keep_their_meaning():
    texts = entries()
    assert 'PS' in texts[0x7B3C6A] and '20' not in texts[0x7B3C6A]  # Life Orb, pas Poção
    assert 'início' in texts[0x7B3EB0]  # Quick Ball, pas Master Ball
    assert 'Venenoso' in texts[0x7B3D8E]
    assert 'Ataque Especial' in texts[0x7B4395]
    assert 'SES Expressway' in texts[0x7A9EA3]
    assert 'KBT' not in texts[0x7A9EA3]
    assert 'Thundercap Mt.' in texts[0x7B14D6]
    assert 'The Shadows' in texts[0x7B2B02]
    assert 'Growl' in texts[0x7BB372] and 'Tail Whip' in texts[0x7BB372]
    assert 'Poções' in texts[0x7BA857]
    assert len(bytes.fromhex(ROWS[6]['source_hex'])) > 1000
    assert 'Rayquaza' in texts[0x7A9A75]  # fin absente du combined EN tronqué
    assert 'Meus estudos dependem' in texts[0x7AAECA]
    config = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())
    assert config['patches'].index('batch_24') > config['patches'].index('repoint_stale')


def test_corrupted_suffixes_are_identified_before_injection():
    by_offset = {int(r['offset'], 16): r for r in ROWS}
    for suffix, parent in ((0x7AB089, 0x7AAECA), (0x7B4A4E, 0x7B4A3B),
                           (0x7B8EDD, 0x7B8E3A)):
        row = by_offset[suffix]
        assert row['status'] == 'exception' and row['references']
        assert bytes.fromhex(row['source_hex']) == bytes.fromhex(
            by_offset[parent]['source_hex'])[suffix - parent:]


def test_exception_owners_really_overlap_the_extracted_fragment():
    for row in ROWS:
        if row['status'] != 'exception' or 'owner_offset' not in row:
            continue
        delta = int(row['offset'], 16) - int(row['owner_offset'], 16)
        fragment = bytes.fromhex(row['source_hex'])
        owner = bytes.fromhex(row['owner_source_hex'])
        if delta > 0:
            assert fragment == owner[delta:]
        else:
            assert fragment[-delta:] == owner
            assert set(fragment[:-delta]) <= {0x00, 0xAA}
