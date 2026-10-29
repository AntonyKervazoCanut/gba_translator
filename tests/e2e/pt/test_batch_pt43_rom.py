"""PT-43 : consommateurs et octets de la ROM PT reconstruite."""
import hashlib
import re

import pytest

from languages.pt.patches.batch_43 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt43 import AUDIT, ROOT, ROWS

pytestmark = pytest.mark.rom


def test_source_pointers_and_final_texts():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    rom = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    make_patch(source).verify(rom)
    for row in ROWS:
        offset = int(row['live_offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        pointer = (offset + 0x08000000).to_bytes(4, 'little')
        matches = [m.start() for m in re.finditer(re.escape(pointer), source)]
        assert sorted(row['references'] + row.get('excluded_pointer_matches', [])) == matches
        if row['status'] == 'exception':
            continue
        expected = TextEncoder.encode_pokemon(row['expected'].replace(r'\n', '\n'), strict=True)
        for ref in row['references']:
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            assert 0 <= target <= len(rom) - len(expected)
            assert rom[target:target + len(expected)] == expected, row['offset']
        # Mesures réelles des noms conservés, dans les cinq polices natives.
        if row['status'] == 'retained':
            for font in LATIN_FONTS:
                _, widths = font.offsets(rom)
                assert sum(rom[widths + c] for c in expected[:-1]) <= 204
    # Tables de choix et de prénoms : les pointeurs de base restent inchangés.
    for table in (0xA6B6E8, 0xA6B768, 0xA6B7A0, 0xA6B870, 0xA762F4, 0xA76484):
        p = (table + 0x08000000).to_bytes(4, 'little')
        refs = [m.start() for m in re.finditer(re.escape(p), source)]
        assert refs, hex(table)
        for ref in refs:
            assert rom[ref:ref + 4] == p


def test_real_font_widths_with_expanded_battle_names():
    from tests.e2e.pt.test_batch_pt13_rom import widths

    rom = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    buffers = {(0xFD, key): 'The opposing ' + 'W' * 10 for key in (15, 16)}
    buffers.update({(0xFD, key): 'adversária' for key in (0x35, 0x36)})
    for row in ROWS:
        if row['status'] != 'translated':
            continue
        raw = TextEncoder.encode_pokemon(row['expected'].replace(r'\n', '\n'), strict=True)
        for font in LATIN_FONTS:
            _, table = font.offsets(rom)
            for page in re.split(b'[\xfa\xfb]', raw):
                assert max(widths(page, rom, table, buffers)) <= 204, row['offset']
