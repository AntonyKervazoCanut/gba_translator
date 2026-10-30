"""PT-52 : chaque consommateur et chaque budget dans la ROM PT reconstruite."""
import hashlib
import re

import pytest

from languages.pt.patches.batch_52 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt52 import AUDIT, ROOT, ROWS

pytestmark = pytest.mark.rom


def test_source_consumers_and_all_final_rom_strings():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    rom = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    make_patch(source).verify(rom)
    base = int(AUDIT['species_table_base'], 16)
    readers = [m.start() for m in re.finditer(re.escape((base + 0x08000000).to_bytes(4, 'little')), source)]
    assert readers == AUDIT['species_table_references']
    for row in ROWS:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        refs = [m.start() for m in re.finditer(re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert refs == row['references']
        expected = TextEncoder.encode_pokemon(row['expected'].replace(r'\n', '\n'), strict=True)
        for consumer in row.get('indirect_consumers', []):
            site = int(consumer['site'], 16)
            assert int.from_bytes(source[site - 4:site - 2], 'little') == consumer['species_id']
            assert rom[site - 4:site] == source[site - 4:site]
            assert site in refs
            assert (site - int(consumer['table_base'], 16) - 4) % 8 == 0
        if row['kind'] == 'species':
            assert offset == base + row['species_id'] * 11
            assert rom[offset:offset + 11] == bytes.fromhex(row['cell_hex'])
        else:
            for ref in refs:
                target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
                assert rom[target:target + len(expected)] == expected, row['offset']
            if 'dex_index' in row:
                assert refs[0] == 0x1A35800 + row['dex_index'] * 36
    # Les cellules immédiatement avant/après le sous-ensemble sont hors lot.
    assert rom[base:base + 11] == source[base:base + 11]
    assert rom[0x166B040:0x166B04B] == source[0x166B040:0x166B04B]


def test_actual_five_font_budgets():
    rom = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    for row in ROWS:
        raw = TextEncoder.encode_pokemon(row['expected'].replace(r'\n', '\n'), strict=True)
        for font in LATIN_FONTS:
            _, widths = font.offsets(rom)
            measured = [sum(rom[widths + c] for c in line) for line in raw[:-1].split(b'\xfe')]
            assert max(measured) <= row['max_width'], (row['offset'], font.glyph_pointer, measured)
