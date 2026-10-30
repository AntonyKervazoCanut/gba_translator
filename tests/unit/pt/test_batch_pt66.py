"""PT-66 : périmètre fermé, pages, budgets et faits des huit Arènes."""
import json
from pathlib import Path

import yaml

from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt66_audit.json').read_text())


def test_manifest_protections_controls_and_budgets():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-66')
    texts = entries()
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert len(manifest) == 300
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        if row['status'] == 'exception':
            assert offset == 0x1F16225 and not row['references']
            assert offset not in texts and offset not in guards
            assert not row['interior_hits'] and row['reason']
            continue
        text = texts[offset]
        assert text == guards[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(text.replace(r'\n', '\n'), strict=True)
        assert len(raw) == row['encoded_bytes']
        source = bytes.fromhex(row['source_hex'])
        assert [c for c in _extract_control_sequences_from_raw(raw) if c[0] != 0xFE] == [
            c for c in _extract_control_sequences_from_raw(source) if c[0] != 0xFE]
        widths = line_widths(text.replace(r'\n', '\n'))
        assert widths == row['line_widths'] and max(widths) <= row['max_width']
        if row['layout'] == 'dialogue':
            assert all(page.split(b'\xfa')[0].count(b'\xfe') <= 1 for page in raw.split(b'\xfb'))
            assert all(b'\xfe' not in part for page in raw.split(b'\xfb') for part in page.split(b'\xfa')[1:])
        elif row['max_width'] == 172:
            assert len(widths) <= 3
        assert row['references'] or row['consumer_references']


def test_story_facts_and_glossary():
    rows = {r['index']: r for r in AUDIT['entries']}
    assert 'Caterpie' in rows[11]['portuguese'] and 'Weedle' in rows[11]['portuguese']
    assert '20' in rows[49]['portuguese'] and 'Hard Stone' in rows[49]['portuguese']
    assert 'KBT Expressway' in rows[51]['portuguese']
    assert '3' in rows[84]['portuguese']
    assert '57' in rows[203]['portuguese'] and 'Rock Climb' in rows[203]['portuguese']
    assert '61' in rows[213]['portuguese']
    assert 'dois primeiros' in rows[208]['portuguese']
    assert 'Butterfree' in rows[225]['portuguese'] and 'Caterpie' in rows[225]['portuguese']
    for index in [151, 178, 187, 219]:
        assert len(bytes.fromhex(rows[index]['source_hex'])) > 500
        assert rows[index]['portuguese'].endswith(('!', '.', '?', '<0xB0>'))
    for index in range(66, 84):
        assert rows[index]['portuguese'] == rows[index]['english']
        assert rows[index]['references'] == [0x1FB1D48 + (index - 66) * 4]


def test_finalizer_follows_repairs():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_66') == 1
    assert all(steps.index(p) < steps.index('batch_66') for p in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))
