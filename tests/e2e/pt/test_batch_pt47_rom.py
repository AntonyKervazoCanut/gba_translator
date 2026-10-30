"""PT-47 : vrais consommateurs, cellules fixes et texte injecté dans la ROM."""
import hashlib
import re

import pytest

from languages.pt.patches.batch_47 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths
from tests.unit.pt.test_batch_pt47 import AUDIT, ROOT, ROWS

pytestmark = pytest.mark.rom


def test_source_consumers_and_final_rom():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    rom = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    make_patch(source).verify(rom)
    # Cellule ??? absente du manifeste et préfixes de données hors texte.
    for start, size in ((0xA4EB13, 7), (0xA4EAD2, 2), (0xA4EE0A, 2), (0xA4E43E, 2)):
        assert rom[start:start + size] == source[start:start + size]
    for row in ROWS:
        offset = int(row['live_offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        refs = [m.start() for m in re.finditer(
            re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert refs == row['references']
        if row['status'] == 'exception':
            continue
        expected = TextEncoder.encode_pokemon(row['expected'].replace(r'\n', '\n'), strict=True)
        if 'cell_offset' in row:
            assert rom[offset:offset + 7] == expected.ljust(7, b'\xff')
        else:
            for ref in refs:
                target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
                assert rom[target:target + len(expected)] == expected, row['offset']


def test_real_font_budgets_and_dynamic_buffers():
    rom = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    for row in ROWS:
        if row['status'] == 'exception':
            continue
        offset = int(row['offset'], 16)
        raw = TextEncoder.encode_pokemon(row['expected'].replace(r'\n', '\n'), strict=True)
        buffers = {(0xFD, 1): 'W' * 7, (0xFD, 2): 'W' * 10,
                   (0xFD, 3): 'W' * 12, (0xFD, 4): 'unidades',
                   (0xFD, 6): 'W' * 7, (0xFD, 0x23): 'W' * 7}
        # Les deux premiers tampons de ces messages contiennent quantité et objet.
        if offset in (0xA4D82B, 0xA4D83B):
            buffers[(0xFD, 2)] = '999'
            buffers[(0xFD, 3)] = 'W' * 18
        if offset == 0xA4D84B:
            buffers[(0xFD, 2)] = 'W' * 18  # nom du mouvement contenu dans la TM
        if offset == 0xA4E00D:
            buffers[(0xFD, 2)] = '999'
            buffers[(0xFD, 3)] = '999999'
        if offset in (0xA4E240, 0xA4E276, 0xA4E299):
            buffers[(0xFD, 3)] = 'Defesa Especial'
        if offset in (0xA4E37C, 0xA4E397):
            buffers[(0xFD, 3)] = 'W' * 17
        for font in LATIN_FONTS:
            _, table = font.offsets(rom)
            for page in re.split(b'[\xfa\xfb]', raw):
                assert max(widths(page, rom, table, buffers)) <= row['max_width'], (row['offset'], font.glyph_pointer, widths(page, rom, table, buffers))
