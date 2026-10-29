"""Vérifie les pointeurs vivants ES et la préservation des polices moteur."""
from pathlib import Path

import pytest

# Aucun BPS es-maint versionné à ce stade : ces contrôles consomment le
# build local explicite, contrairement à make test-rom (patchs distribués).
pytestmark = pytest.mark.rom


@pytest.mark.private_build
def test_maintained_spanish_live_status_bytes():
    rom = Path('output/roms/GenedRom-es-maint.gba').read_bytes()
    # SLP/PSN/PAR/BRN/FRZ, ordre de la table moteur ; octets littéraux CFRU.
    expected = ['be c9 cc ff', 'bf c8 d0 ff', 'ca bb cc ff', 'cb cf bf ff', 'bd c9 c8 ff']
    for index, raw in enumerate(expected):
        pointer = int.from_bytes(rom[0x3DFE18 + index*8:0x3DFE1C + index*8], 'little') - 0x8000000
        assert rom[pointer:pointer+4] == bytes.fromhex(raw)


@pytest.mark.private_build
def test_maintained_spanish_preserves_all_native_engine_glyphs():
    source = Path('input/roms/englishrom.gba').read_bytes()
    rom = Path('output/roms/GenedRom-es-maint.gba').read_bytes()
    codes = bytes.fromhex('17 1b 6f 23 27 f6 29 02 06 5a 0e 12 f3 14 52 51')
    for base, stride in [(0x1EAF00,32), (0x1F3100,64), (0x1FF300,64), (0x20F618,64), (0x21F930,64)]:
        for cp in codes:
            start = base + stride*cp
            assert rom[start:start+stride] == source[start:start+stride]


@pytest.mark.private_build
def test_maintained_spanish_compressed_fonts_and_nonfont_graphics():
    from languages.de.patches.font import extract_diaeresis_dots, find_font_blocks
    from languages.fr.patches.font import lz77_decompress
    source = Path('input/roms/englishrom.gba').read_bytes()
    rom = Path('output/roms/GenedRom-es-maint.gba').read_bytes()
    fonts = [b.decompressed for b in find_font_blocks(rom)
             if extract_diaeresis_dots(b.decompressed, 0x08, 0xBF)
             and extract_diaeresis_dots(b.decompressed, 0x1D, 0xD9)]
    assert len(fonts) == 6
    for font in fonts:
        for cp, base in [(0xF3, 0xCF), (0xF6, 0xE9)]:
            assert font[cp*32:(cp+1)*32] != font[base*32:(base+1)*32]
    # Ce graphisme passe l'heuristique générale de densité, mais n'est pas latin.
    _, size = lz77_decompress(source, 0x40C650)
    assert rom[0x40C650:0x40C650+size] == source[0x40C650:0x40C650+size]
