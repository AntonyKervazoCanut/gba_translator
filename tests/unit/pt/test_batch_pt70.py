"""PT-70 : périmètre, contrôles, budgets et faits du scénario."""
import json
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt70_audit.json').read_text())


def test_manifest_protections_controls_and_budgets():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-70')
    texts = entries()
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert len(manifest) == 299
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['scene'] and row['full_english']
        if row['french'] is None:
            assert row['index'] in (4, 55, 67, 179, 214, 216, 293)
        if row['status'] == 'exception':
            assert offset == 0x1F34CC9 and not row['references']
            assert offset not in texts and offset not in guards
            assert not row['interior_hits']
            continue
        text = texts[offset]
        assert text == guards[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(text.replace(r'\n', '\n'), strict=True)
        assert len(raw) == row['encoded_bytes']
        assert raw[-1] == 0xFF and 0xFF not in raw[:-1]
        assert [c for c in commands(raw) if c != b'\xfe'] == [
            c for c in commands(bytes.fromhex(row['source_hex'])) if c != b'\xfe']
        widths = line_widths(text.replace(r'\n', '\n'))
        assert widths == row['line_widths'] and max(widths) <= 192
        assert row['references']
        for page in raw.split(b'\xfb'):
            assert page.split(b'\xfa')[0].count(b'\xfe') <= 1
            assert all(b'\xfe' not in part for part in page.split(b'\xfa')[1:])


def test_story_facts_and_complete_long_dialogues():
    rows = AUDIT['entries']
    assert 'Moltres' in rows[5]['portuguese'] and 'Cinder Volcano' in rows[5]['portuguese']
    assert 'Route 9' in rows[23]['portuguese']
    assert 'Cut' in rows[58]['portuguese'] and 'Valley Cave' in rows[58]['portuguese']
    assert '100' in rows[70]['portuguese'] and 'DexNav' in rows[70]['portuguese']
    assert 'quatro' in rows[150]['portuguese']
    assert 'Discharge' in rows[175]['portuguese']
    assert 'Ability Capsules' in rows[219]['portuguese']
    assert 'Prison Bottle' in rows[282]['portuguese']
    assert 'Hoopa' in rows[287]['portuguese']
    for i in (58, 70, 142, 149, 217, 218, 221, 282):
        row = rows[i]
        assert len(bytes.fromhex(row['source_hex'])) > 500
        assert row['portuguese'].endswith(('.', '!', '?', '<0xB0>'))
    assert 'Daríamos muito' in rows[115]['portuguese']


def test_finalizer_follows_repairs_and_only_changes_one_gender_setup():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_70') == 1
    assert all(steps.index(p) < steps.index('batch_70') for p in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))
    setups = [r for r in AUDIT['entries'] if 'buffer_setup' in r]
    assert [r['index'] for r in setups] == [238]
    assert setups[0]['buffer_setup']['replacement_hex'] == '046ae0e609'


def test_audio_matches_are_not_text_consumers():
    row = AUDIT['entries'][15]
    assert row['references'] == [0x1E57D4A]
    assert row['non_text_references'] == [0x13DF497, 0x13E7D7B]
    assert {p['site'] for p in row['pcm_matches']} == set(row['non_text_references'])
    assert not set(row['references']).intersection(row['non_text_references'])
