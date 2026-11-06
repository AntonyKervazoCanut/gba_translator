"""PT-80 : périmètre exact, pages, services et instructions de Thundercap."""
import json
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]


def audit():
    return json.loads((ROOT / 'languages/pt/data/pt80_audit.json').read_text())['entries']


def test_manifest_protections_and_command_budgets():
    rows = audit()
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-80')
    assert len(rows) == 300
    assert [r['offset'] for r in rows] == manifest
    texts = entries()
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    for row in rows:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['full_english']
        if row['status'] == 'exception':
            assert row['index'] in (125, 174, 218, 219)
            assert not row['references']
            assert offset not in texts and offset not in guards
            continue
        text = texts[offset].replace(r'\n', '\n')
        assert row['portuguese'] == texts[offset] == guards[offset]
        encoded = TextEncoder.encode_pokemon(text, strict=True)
        assert len(encoded) == row['encoded_bytes']
        assert encoded[-1] == 255 and 255 not in encoded[:-1]
        assert [c for c in commands(encoded) if c != b'\xfe'] == [
            c for c in commands(bytes.fromhex(row['source_hex'])) if c != b'\xfe']
        assert line_widths(text) == row['line_widths']
        assert max(row['line_widths']) <= row['max_width']
        assert row['references']
        if row['layout'] == 'dialogue':
            for page in text.split('<0xFB>'):
                for n, part in enumerate(page.split('<0xFA>')):
                    assert part.count('\n') <= (1 if n == 0 else 0), row['offset']
        elif row['index'] in (101, 135, 136, 137, 138, 139, 185):
            assert text.count('\n') <= 2


def test_domain_rules_and_complete_long_dialogues():
    rows = audit()
    for i in (72, 73):
        text = rows[i]['portuguese'].replace(r'\n', ' ')
        assert 'Mega Stone' in text and '<0xF8><0x04>' in text
        assert 'por batalha' in text and 'nocauteado' in text
        assert 'humanidade' in text and 'diferença' in text
    assert '50000' in rows[158]['portuguese']
    assert '50000' in rows[159]['portuguese']
    assert 'Amulet Coin' in rows[113]['portuguese'].replace(r'\n', ' ')
    assert rows[175]['portuguese'] == 'Thundercap Mt.'
    assert rows[176]['portuguese'] == 'Thundercap Mt. A'
    assert rows[177]['portuguese'] == 'Thundercap Mt. B'
    assert '3' in rows[193]['portuguese']
    assert 'Rock Smash, Strength e Surf' in rows[279]['portuguese'].replace(r'\n', ' ')
    assert 'direito' in rows[280]['portuguese'] and 'Surf' in rows[280]['portuguese']
    assert len(rows[209]['portuguese'].split(r'\n')) == 3
    assert all(len(line) <= 11 for line in rows[209]['portuguese'].split(r'\n'))
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_80') == 1
    assert all(steps.index(p) < steps.index('batch_80') for p in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))
