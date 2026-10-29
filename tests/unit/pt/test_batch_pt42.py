"""PT-42 : portée exacte, vrais noms fixes et commandes du DexNav."""
import json
from collections import Counter
from pathlib import Path

import pytest

from languages.pt.patches.batch_42 import make_patch
from scripts.apply_combined_fr import _load_combined
from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt42_audit.json').read_text())
ROWS = AUDIT['entries']


def test_exact_manifest_names_and_dexnav_controls():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    assert [r['offset'] for r in ROWS] == next(b['offsets'] for b in batches if b['id'] == 'PT-42')
    assert Counter(r['status'] for r in ROWS) == {'translated': 50, 'retained': 231, 'exception': 2}
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    for row in ROWS:
        offset = int(row['offset'], 16)
        if row['status'] == 'exception':
            assert row['reason'] and not row['references']
            assert offset not in texts
            continue
        text = texts[offset].replace(r'\n', '\n')
        assert text == row['expected'].replace(r'\n', '\n')
        raw = TextEncoder.encode_pokemon(text, strict=True)
        assert len(raw) == row['pt_bytes']
        assert line_widths(text) == row['pixels']
        if row['kind'] == 'move_name':
            assert raw == bytes.fromhex(row['source_hex'])
            assert len(raw) <= 13
            assert offset == 0xa40a10 + row['move_id'] * 13
        else:
            commands = lambda b: [c for c in _extract_control_sequences_from_raw(b) if c[0] != 254]
            assert commands(raw) == commands(bytes.fromhex(row['source_hex']))
            assert max(row['pixels']) <= row['max_width']
            assert len(row['pixels']) <= 2
    assert TextEncoder.encode_pokemon(texts[0xa43a34], strict=True).endswith(b'\x00\xff')
    assert texts[0xa439b0] == 'Água'  # Absent de EN ; ne pas traduire le None Python.
    assert texts[0xa42dc3] == 'Apple Acid'  # Extraction EN = fragment français périmé.
    assert texts[0xa43ae4].index('<0xFD><0x03>') < texts[0xa43ae4].index('<0xFD><0x02>')


def fixture_source():
    """Reconstruit les extraits réels figés sans simuler les E/S ROM."""
    source = bytearray(b'\xff' * 0x1000000)
    source[0xa40a10:0xa40a12] = b'\xae\xff'
    for ref in AUDIT['move_table']['literals']:
        pos = int(ref, 16)
        source[pos:pos + 4] = (0x08a40a10).to_bytes(4, 'little')
    for row in ROWS:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row.get('source_cell_hex', row['source_hex']))
        source[offset:offset + len(raw)] = raw
        for ref in row['references']:
            source[ref:ref + 4] = (offset + 0x08000000).to_bytes(4, 'little')
    return source


def test_atomic_patch_bounded_idempotent_and_relocated_name_table():
    source = fixture_source()
    rom = bytearray(source)
    # Table vivante déplacée : la copie morte doit rester intacte.
    base = 0xb00000
    rom[base:base + 923 * 13] = source[0xa40a10:0xa40a10 + 923 * 13]
    for ref in AUDIT['move_table']['literals']:
        pos = int(ref, 16)
        rom[pos:pos + 4] = (base + 0x08000000).to_bytes(4, 'little')
    first = next(r for r in ROWS if r['kind'] == 'move_name')
    rom[base + first['move_id'] * 13] = 0
    before = bytes(rom)
    patch = make_patch(bytes(source))
    assert patch.apply(rom)['verified'] == 60
    patch.verify(rom)
    allowed = set()
    for row in ROWS:
        if row['kind'] == 'move_name':
            pos = base + row['move_id'] * 13
            allowed.update(range(pos, pos + 13))
        for ref in row['references']:
            allowed.update(range(ref, ref + 4))
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(target, target + row['pt_bytes']))
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(before, rom)))
    assert patch.apply(rom)['relocated'] == 0
    assert rom[0xa40a10:0xa438f0] == source[0xa40a10:0xa438f0]
    before = bytes(rom)
    for address, message in [(0xa42db6, 'préimage'), (0x9a51c8, 'pointeur source')]:
        corrupt = bytearray(source)
        corrupt[address] ^= 1
        patch.source = bytes(corrupt)
        with pytest.raises(ValueError, match=message):
            patch.apply(rom)
        assert rom == before
