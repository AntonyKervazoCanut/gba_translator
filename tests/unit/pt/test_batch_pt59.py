"""PT-59 : périmètre fermé, commandes, mission et règles du DexNav."""
import json
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt59_audit.json').read_text())


def test_manifest_protections_commands_and_budgets():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-59')
    texts = entries()
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 300
    assert sum(r['status'] == 'exception' for r in AUDIT['entries']) == 2
    assert sum(r['status'] == 'retained' for r in AUDIT['entries']) == 17
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['source_hex'] and row['english_full']
        if row['status'] == 'exception':
            assert offset not in texts and not row['references']
            assert row['related_consumers']
            continue
        assert texts[offset] == guards[offset] == row['portuguese']
        text = texts[offset].replace(r'\n', '\n')
        raw = TextEncoder.encode_pokemon(text, strict=True)
        assert len(raw) == row['encoded_bytes']
        assert raw[-1] == 0xFF and 0xFF not in raw[:-1]
        assert [c for c in commands(raw) if c != b'\xfe'] == [
            c for c in commands(bytes.fromhex(row['source_hex'])) if c != b'\xfe']
        assert line_widths(text) == row['line_widths']
        assert max(row['line_widths']) <= row['max_width']


def test_mission_and_dexnav_mechanics_are_preserved():
    texts = {o: t.replace(r'\n', ' ') for o, t in entries().items()}
    mission = entries()[0x1EE55DE].split(r'\n')
    assert len(mission) == 3 and max(line_widths(s)[0] for s in mission) <= 172
    assert '8 Líderes' in texts[0x1EE55DE] and 'Clássico' in texts[0x1EE55DE]
    assert all(s in texts[0x1EE02B5] for s in ('6 contra 6', '100', 'BP'))
    assert '750' in texts[0x1EE9125] and '420' in texts[0x1EE9125]
    assert all(s in texts[0x1EE9D32] for s in ('100', '50'))
    assert texts[0x1EEA031] == 'Candice' and texts[0x1EE8259] == 'Cheri Berry'
    assert 'Ice Punch' in texts[0x1EE8761] and 'Aurora Veil' in texts[0x1EE88F4]
    # Les fins au-delà du cap historique 500 caractères ont été réellement traduites.
    assert 'frustrações' in texts[0x1EE118A]
    assert 'prêmios' in texts[0x1EDFFBB]
    assert 'nível de busca' in texts[0x1EE92D1] and 'Pokémon melhores' in texts[0x1EE92D1]


def test_finalizer_follows_repairs():
    patches = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert patches.count('batch_59') == 1
    for step in ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'):
        assert patches.index(step) < patches.index('batch_59')
