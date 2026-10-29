"""PT-32 : périmètre fermé, termes, commandes et cellules d'objets."""
import json
import re
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_width
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt32_audit.json').read_text())


def test_exact_manifest_protections_and_control_flow():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    offsets = next(b['offsets'] for b in batches if b['id'] == 'PT-32')
    texts = entries()
    guards = {int(r['offset'], 16): r.get('expected_raw', r['expected']) for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    rows = AUDIT['entries']
    assert [r['offset'] for r in rows] == offsets
    assert len(rows) == 288
    assert {s: sum(r['status'] == s for r in rows) for s in
            ('translated', 'retained', 'exception')} == {
                'translated': 155, 'retained': 120, 'exception': 13}
    for row in rows:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['source_hex'] and row['english_reference']
        if row['status'] == 'exception':
            assert offset not in texts
            continue
        assert texts[offset] == guards[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(texts[offset].replace(r'\n', '\n'), strict=True)
        assert len(raw) == row['encoded_bytes'] <= 512
        assert raw[-1] == 0xFF and 0xFF not in raw[:-1]
        assert [c for c in commands(raw) if c != b'\xfe'] == [
            c for c in commands(bytes.fromhex(row['source_hex'])) if c != b'\xfe']
        assert [line_width(s) for s in re.split(r'<0xF[AB]>|\\n', texts[offset])] == row['line_widths']
        assert max(row['line_widths']) <= row['max_width']
        if 'table_base' in row:
            assert row['status'] == 'retained'
            assert raw == bytes.fromhex(row['source_hex'])
            assert row['cell_bytes'] == 14
            assert len(raw) <= row['cell_bytes']
            assert (offset - int(row['table_base'], 16)) % row['stride'] == 0


def test_battle_mechanics_forms_and_glossary():
    texts = entries()
    for offset, word in [(0x8A0B40, 'Fogo'), (0x8B7850, 'Água'),
                         (0x8BC450, 'Fantasma'), (0x8BC470, 'Planta'),
                         (0x8B4EC0, 'Ataque Especial'), (0x8B9D40, 'Defesa Especial'),
                         (0x8AA8DB, 'quatro movimentos'), (0x8AA355, 'Deoxys'),
                         (0x8AA575, 'Kyurem'), (0x8AAA55, 'Therian'),
                         (0x8AAA77, 'Incarnate'), (0x8B9A40, 'PS'),
                         (0x8A98D0, 'Wide Guard'), (0x8A9903, 'Crafty Shield')]:
        assert word in texts[offset].replace(r'\n', ' ')
    assert texts[0x8B9010] != texts[0x8B9032]
    assert texts[0x8B905C] != texts[0x8B907E]
    assert texts[0x8AA39F] != texts[0x8AA3D4]
    assert texts[0x8A90F9] == 'AKLOV'
    assert texts[0x8AA459] == r'O Pokémon não reage\nao meteoro.'
    config = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())
    assert config['patches'].count('batch_32') == 1
    assert len(config['patches']) == len(set(config['patches']))
    for step in ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale'):
        assert config['patches'].index(step) < config['patches'].index('batch_32')
