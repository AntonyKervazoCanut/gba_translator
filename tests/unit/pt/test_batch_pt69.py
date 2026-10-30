"""PT-69 : scénario initial, quiz, fragments et périmètre fermé."""
import json
import re
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]


def audit():
    """Charge les décisions individuelles des 300 offsets du manifeste."""
    return json.loads((ROOT / 'languages/pt/data/pt69_audit.json').read_text())


def test_scope_protections_and_control_order():
    rows = audit()['entries']
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-69')
    texts = entries()
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in rows] == manifest
    assert len(rows) == 300
    assert sum(r['status'] == 'exception' for r in rows) == 7
    for row in rows:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['scene'] and row['source_hex']
        if row['status'] == 'exception':
            assert not row['references'] and offset not in texts
            continue
        assert texts[offset] == guards[offset] == row['portuguese']
        text = texts[offset].replace(r'\n', '\n')
        raw = TextEncoder.encode_pokemon(text, strict=True)
        source = bytes.fromhex(row['source_hex'])
        assert len(raw) == row['encoded_bytes']
        assert raw[-1] == 255 and 255 not in raw[:-1]
        assert [c for c in commands(raw) if c != b'\xfe'] == [
            c for c in commands(source) if c != b'\xfe']
        assert commands(raw).count(b'\xfe') == commands(source).count(b'\xfe')
        assert line_widths(text) == row['line_widths']
        assert max(row['expanded_widths']) <= row['pixel_budget'] == 208
        for page in text.split('<0xFB>'):
            for n, segment in enumerate(page.split('<0xFA>')):
                assert segment.count('\n') <= (1 if n == 0 else 0)


def test_quiz_answers_keyboard_and_rewards():
    rows = audit()['entries']
    assert [r['portuguese'] for r in rows[50:60]] == [
        'dupla', 'druddigon', 'agua', 'carbink', 'verde', 'marrom',
        'terceiro', 'void', 'mulheres', 'ditoh']
    assert all(re.fullmatch('[a-z]+', r['portuguese']) for r in rows[50:60])
    assert 'dois contra dois' in rows[30]['portuguese']
    assert 'Big Nugget' in rows[21]['portuguese']
    assert 'Tiny Mushroom' in rows[25]['portuguese']
    assert '¥500' in rows[60]['portuguese'] and 'PS' in rows[60]['portuguese']
    assert '¥6000' in rows[63]['portuguese']


def test_concatenated_fragments_and_complete_scenario():
    rows = audit()['entries']
    assert rows[91]['portuguese'].startswith('<0x00>')
    assert rows[91]['portuguese'].endswith(r'\n')
    assert rows[92]['portuguese'].endswith('<0x00>')
    assert rows[93]['portuguese'].endswith('<0x00>')
    assert 'três tipos diferentes' in rows[75]['portuguese']
    assert 'natureza' in rows[71]['portuguese']
    assert rows[208]['portuguese'].endswith('vai facilitar sua viagem.')
    assert rows[273]['portuguese'].endswith('quero que fique com isto.')
    assert 'Poção' in rows[167]['portuguese']
    assert 'Cut' in rows[226]['portuguese']
    assert rows[299]['portuguese'] == 'Staravia! Use Aerial Ace!'
    assert '3 primeiros' in rows[295]['portuguese']
    patches = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert patches.count('batch_69') == 1
    assert all(patches.index(step) < patches.index('batch_69') for step in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))
