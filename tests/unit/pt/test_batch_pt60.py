"""PT-60 : périmètre fermé, protections, commandes et mécanique des quêtes."""
import json
import re
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_width
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt60_audit.json').read_text())


def test_manifest_protection_pages_and_budgets():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    offsets = next(b['offsets'] for b in batches if b['id'] == 'PT-60')
    rows, texts = AUDIT['entries'], entries()
    guards = {int(r['offset'], 16): r.get('expected_raw', r['expected']) for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in rows] == offsets
    assert len(rows) == 299
    assert sum(r['status'] == 'exception' for r in rows) == 3
    for row in rows:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['source_hex'] and row['english_reference']
        if row['status'] == 'exception':
            assert offset not in texts and not row['references']
            assert row['owner_sites']
            continue
        assert texts[offset] == guards[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(texts[offset].replace(r'\n', '\n'), strict=True)
        source = bytes.fromhex(row['source_hex'])
        assert len(raw) == row['encoded_bytes']
        assert raw[-1] == 0xFF and 0xFF not in raw[:-1]
        assert [c for c in commands(raw) if c[0] != 0xFE] == [
            c for c in commands(source) if c[0] != 0xFE]
        assert raw.count(b'\xfe') == source.count(b'\xfe')
        widths = [line_width(s) for s in re.split(r'<0xF[AB]>|\\n', texts[offset])]
        assert widths == row['line_widths'] and max(widths) <= row['max_width']
        if row['layout'] == 'mission':
            assert texts[offset].count(r'\n') <= 2
        if row.get('pcm_consumers'):
            assert {int(p['occurrence'], 16) for p in row['pcm_consumers']} == set(row['non_text_references'])
        if row['layout'] == 'credits':
            assert raw.count(b'\xfe') == 6


def test_recipes_evolution_mining_and_complete_history():
    texts = entries()
    for offset, terms in {
        0x1eea8a9: ['1 Pecha Berry', '1 Qualot Berry', '1 Fresh Water'],
        0x1eea909: ['3 Rawst Berries', '5 Belue Berries', '5 Watmel Berries', '5 Moomoo Milks'],
        0x1eea96a: ['10 Sitrus Berries', '10 Lum Berries', '2 Kee Berries', '2 Marang Berries', '5 Moomoo Milks'],
        0x1eea61b: ['Rock Smash', 'Blizzard City', 'Insígnia'],
        0x1eeb152: ['Alice', 'Voador'],
        0x1eeb463: ['Eviolite', 'defesas'],
        0x1eedcfb: ['KBT Expressway', '3 Carbink', 'Light Clay', 'recompensa'],
        0x1eee8be: ['Cube Corp.', 'Aros', 'Rayquaza', 'Valley City', 'East Borrius', 'heroico'],
        0x1eeeccc: ['desejo', 'preço', 'lar'],
        0x1eef2de: ['Heart Scale', 'movimento'],
    }.items():
        for term in terms:
            assert term in texts[offset].replace(r'\n', ' '), (hex(offset), term)
    assert texts[0x1eebadf] == r'A PRESSÃO É\nA CHAVE.'
    # Pas de traduction inventée des noms propres et des attributions.
    for row in AUDIT['entries']:
        if row['index'] >= 252 and row['status'] == 'retained':
            assert TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n')) == bytes.fromhex(row['source_hex'])


def test_finalizer_after_repairs():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_60') == 1
    for step in ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale'):
        assert steps.index(step) < steps.index('batch_60')


def test_exceptions_are_code_backed_and_long_extracts_are_complete():
    rows = {r['index']: r for r in AUDIT['entries']}
    assert rows[163]['alignment_hex'] == 'c046'
    assert rows[163]['owner_offset'] == '0x1eed330'
    for index in (155, 156):
        assert rows[index]['owner_offset'] == '0x1eed1d8'
        assert any(p['offset'] == '0x1eb20ec' and p['source_hex'] == 'd8d1ee09'
                   for p in rows[index]['consumer_code'])
    assert [len(bytes.fromhex(rows[i]['source_hex'])) for i in (181, 215, 216)] == [528, 1038, 586]
