"""Préimages, pointeurs, champs voisins et octets livrés du lot PT-57."""
import hashlib
import re

import pytest

from languages.pt.patches.batch_57 import apply_patches
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt57 import AUDIT, ROOT

pytestmark = pytest.mark.rom


def test_final_rom_categories_and_binary_exceptions():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    refs = [m.start() for m in re.finditer(re.escape((0x09A357CC).to_bytes(4, 'little')), source)]
    assert refs == AUDIT['table_references'] and len(refs) == 10
    for p in refs:
        assert source[p:p + 4] == built[p:p + 4]
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        if row['status'] == 'exception':
            raw = bytes.fromhex(row['source_hex'])
            assert source[offset:offset + len(raw)] == built[offset:offset + len(raw)] == raw
            assert source.find((offset + 0x08000000).to_bytes(4, 'little')) == -1
            continue
        cell = int(row['cell_offset'], 16)
        assert source[cell:cell + 12].hex() == row['source_hex']
        assert built[cell:cell + 12].hex() == row['final_hex']
        # +16 est un pointeur de description relogé par les lots Pokédex.
        # Les champs taille/poids restent fixes ; l'absence de toute écriture
        # PT-57 hors cellule est contrôlée sur la ROM entière ci-dessous.
        assert built[cell + 12:cell + 16] == source[cell + 12:cell + 16]
        assert built[offset:cell].hex() == row['prefix_hex']
        encoded = TextEncoder.encode_pokemon(row['portuguese'], strict=True)
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            assert sum(built[widths + c] for c in encoded[:-1]) <= 76


def test_patch_writes_only_manifest_cells_and_is_idempotent():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    rom = bytearray(source)
    expected = bytearray(source)
    for row in AUDIT['entries']:
        if row['status'] == 'translated':
            cell = int(row['cell_offset'], 16)
            expected[cell:cell + 12] = bytes.fromhex(row['final_hex'])
    assert apply_patches(rom, source) == 166
    assert rom == expected
    assert apply_patches(rom, source) == 166
    assert rom == expected
    built = bytearray((ROOT / 'output/roms/GenedRom-pt.gba').read_bytes())
    before = bytes(built)
    apply_patches(built, source)
    assert built == before


@pytest.mark.parametrize('kind', ['reader', 'source', 'prefix', 'truncated'])
def test_preflight_failure_is_atomic(kind):
    source = bytearray((ROOT / 'input/roms/englishrom.gba').read_bytes())
    rom = bytearray(source)
    last = AUDIT['entries'][-1]
    if kind == 'reader':
        rom[AUDIT['table_references'][-1]] ^= 1
    elif kind == 'source':
        source[int(last['cell_offset'], 16)] ^= 1
    elif kind == 'prefix':
        rom[int(last['offset'], 16)] ^= 1
    else:
        del rom[int(last['cell_offset'], 16):]
    before = bytes(rom)
    with pytest.raises(ValueError, match='PT-57'):
        apply_patches(rom, source)
    assert rom == before


def test_native_pokedex_copy_loop_keeps_every_category_and_terminator():
    """Exécute la boucle Thumb réelle : plafond de onze glyphes, sans troncature."""
    from unicorn import UC_ARCH_ARM, UC_MODE_THUMB, Uc
    from unicorn.arm_const import UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_SP

    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    cpu = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    cpu.mem_map(0x08000000, (len(built) + 4095) & ~4095)
    cpu.mem_write(0x08000000, built)
    cpu.mem_map(0x03000000, 0x8000)
    table = int.from_bytes(built[0x105860:0x105864], 'little')
    assert table == 0x09A357CC
    for row in AUDIT['entries']:
        if row['status'] != 'translated':
            continue
        cpu.reg_write(UC_ARM_REG_SP, 0x03007F00)
        cpu.reg_write(UC_ARM_REG_R4, 0)
        cpu.reg_write(UC_ARM_REG_R5, table + row['dex_index'] * 36)
        cpu.mem_write(0x03007F08, b'\x55' * 16)
        cpu.emu_start(0x0810583B, 0x08105882, count=200)
        encoded = TextEncoder.encode_pokemon(row['portuguese'], strict=True)
        assert bytes(cpu.mem_read(0x03007F08, len(encoded))) == encoded
        assert bytes(cpu.mem_read(0x03007F08 + len(encoded), 1)) == b'\x55'
