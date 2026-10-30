"""PT-61 : contrat fermé, contrôles exacts, budgets et faits du scénario."""
import json
from pathlib import Path

import yaml

from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt61_audit.json').read_text())


def test_manifest_protections_controls_and_budgets():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-61')
    texts = entries()
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert len(manifest) == 300
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        if row['status'] == 'exception':
            assert offset == 0x1EF5586 and not row['references']
            assert offset not in texts and offset not in guards
            assert row['interior_hits'] and row['reason']
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
        if b'\xfb' in raw or b'\xfa' in raw:
            assert all(page.split(b'\xfa')[0].count(b'\xfe') <= 1 for page in raw.split(b'\xfb'))
        if row['index'] <= 10:
            assert raw == source  # crédits, noms et centrage inchangés
        assert row['references'] or row['consumer_references']


def test_story_facts_and_glossary():
    texts = entries()
    assert 'Drifloon' in texts[0x1EF1137]
    assert 'Ditto' in texts[0x1EF14D7]
    assert 'Cube Corp.' in texts[0x1EF2874]
    assert 'Earthquake' in texts[0x1EF2D51]
    assert 'Defesa' in texts[0x1EF2D87] and 'Barrier' in texts[0x1EF2D87]
    assert 'Arceus' in texts[0x1EF517F] and 'Mítico' in texts[0x1EF517F]
    assert 'um único dia' in texts[0x1EF5BEA]
    assert '12 horas' in texts[0x1EF6904] and 'Dialga' in texts[0x1EF6904]
    assert '100 Ovos' in texts[0x1EF7449]
    assert 'B1F' in texts[0x1EF6F6C]
    assert '3F' in texts[0x1EF7018] and '2F' in texts[0x1EF7018]
    assert 'Dawn Stone' == texts[0x1EF4BAF]


def test_finalizer_follows_repairs():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_61') == 1
    assert all(steps.index(p) < steps.index('batch_61') for p in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))


def test_long_source_dialogues_are_complete_and_mission_windows_fit():
    rows = {r['index']: r for r in AUDIT['entries']}
    assert 'cientista muito importante?' in rows[232]['portuguese']
    assert 'vou te recompensar.' in rows[234]['portuguese']
    assert 'usar isto... hum, sim.' in rows[237]['portuguese']
    for index in [29, 40, 223, 231, *range(264, 287)]:
        row = rows[index]
        assert row['max_width'] == 172
        assert len(row['line_widths']) <= 3
        assert max(row['line_widths']) <= 172


def test_fixed_pointer_tables_keep_their_cells():
    rows = {r['index']: r for r in AUDIT['entries']}
    for index in range(180, 186):
        assert rows[index]['references'] == [0x1FB1D1C + (index - 180) * 4]
    for index in range(241, 264):
        assert rows[index]['references'] == [0x1E616F0 + (index - 241) * 16]
    for index in range(264, 287):
        assert rows[index]['references'] == [0x1E616F4 + (index - 264) * 16]
    assert rows[11]['consumer_offset'] == '0x1ef0c68'
    assert len(rows[11]['consumer_references']) == 7
