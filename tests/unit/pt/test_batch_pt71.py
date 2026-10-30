"""PT-71 : périmètre fermé, scripts, pages et faits du scénario."""
import json
from pathlib import Path

import yaml

from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt71_audit.json').read_text())


def test_manifest_protections_controls_and_budgets():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-71')
    texts = entries()
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert len(manifest) == 300
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        if row['status'] == 'exception':
            assert row['index'] in (107, 120, 261, 262, 263, 264)
            assert not row['references'] and row['reason']
            assert offset not in texts and offset not in guards
            continue
        text = texts[offset]
        assert text == guards[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(text.replace(r'\n', '\n'), strict=True)
        assert len(raw) == row['encoded_bytes']
        source = bytes.fromhex(row['source_hex'])
        assert [c for c in _extract_control_sequences_from_raw(raw) if c[0] != 0xFE] == [
            c for c in _extract_control_sequences_from_raw(source) if c[0] != 0xFE]
        assert line_widths(text.replace(r'\n', '\n')) == row['line_widths']
        assert max(row['line_widths']) <= row['max_width']
        assert all(page.split(b'\xfa')[0].count(b'\xfe') <= 1 for page in raw.split(b'\xfb'))
        assert all(b'\xfe' not in part for page in raw.split(b'\xfb') for part in page.split(b'\xfa')[1:])
        assert row['references']


def test_story_facts_and_glossary():
    rows = {r['index']: {**r, 'portuguese': r.get('portuguese', '').replace(r'\n', ' ')} for r in AUDIT['entries']}
    for index in (37, 76, 142, 214):
        assert len(bytes.fromhex(rows[index]['source_hex'])) > 500
        assert rows[index]['portuguese'].endswith(('.', '<0xB0>'))
    assert 'poder de Hoopa' in rows[3]['portuguese']
    assert '16' in rows[31]['portuguese']
    assert 'dezessete' in rows[152]['portuguese']
    assert 'dezesseis' in rows[149]['portuguese']
    assert 'Red Orb' in rows[110]['portuguese']
    assert 'Rock Smash' in rows[124]['portuguese']
    assert 'Vivill Town' in rows[200]['portuguese']
    assert 'filho' == rows[207]['portuguese']
    assert 'filha' == rows[208]['portuguese']
    assert '6' in rows[272]['portuguese'] and '5' in rows[272]['portuguese']
    assert rows[277]['portuguese'] == 'aklov'
    assert 'E' in rows[279]['portuguese']
    assert 'Prison Bottle' in rows[142]['portuguese']
    assert 'Ultimate' in rows[290]['portuguese']


def test_finalizer_follows_repairs():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_71') == 1
    assert all(steps.index(p) < steps.index('batch_71') for p in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))
