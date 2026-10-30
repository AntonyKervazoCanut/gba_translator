"""PT-58 : cellules réelles, pointeurs, exceptions binaires et largeurs natives."""
import hashlib
import re

import pytest

from languages.pt.patches.batch_58 import apply_patches, make_patch
from languages.pt.patches.font import apply_patches as patch_font
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths
from tests.unit.pt.test_batch_pt58 import AUDIT, ROOT

pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_source_pointers_cells_and_nontext_exceptions(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[off:off + len(raw)] == raw
        assert [m.start() for m in re.finditer(
            re.escape((off + 0x08000000).to_bytes(4, 'little')), source)] == row['references']
        if row['kind'] == 'non_text':
            assert source[off - 16:off + 32] == bytes.fromhex(row['context_hex'])
        if row['kind'] == 'category':
            assert source[off:off + 2] == b'\0\0'
            assert source[off + 2:off + 14] == bytes.fromhex(row['cell_hex'])
    base = int(AUDIT['table_base'], 16)
    assert [m.start() for m in re.finditer(
        re.escape((base + 0x08000000).to_bytes(4, 'little')), source)] == AUDIT['table_references']


def test_native_font_budgets_including_expanded_names(source):
    rom = bytearray(source)
    patch_font(rom)
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            continue
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        buffers = {(0xFD, i): 'W' * 10 for i in (1, 2, 3)}
        # Le nom d'objet rendu par STR_VAR_1 peut remplir une cellule de 19 lettres.
        if row['offset'] in ('0x1ede7e9', '0x1edf2cf'):
            buffers[(0xFD, 2)] = 'W' * 19
        for font in LATIN_FONTS:
            _, table = font.offsets(rom)
            for page in re.split(b'[\xfa\xfb]', raw):
                measured = widths(page, rom, table, buffers)
                limit = 66 if row['kind'] == 'category' else 208
                assert max(measured) <= limit, (row['offset'], font.glyph_pointer, measured)


def test_final_delivery_and_neighbour_fields(source, built):
    make_patch(source).verify(built)
    for ref in AUDIT['table_references']:
        assert built[ref:ref + 4] == source[ref:ref + 4]
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        if row['kind'] == 'non_text':
            assert built[off - 16:off + 32] == source[off - 16:off + 32]
        elif row['kind'] == 'category':
            raw = TextEncoder.encode_pokemon(row['portuguese'], strict=True)
            cell = int(row['consumer_offset'], 16)
            assert built[cell:cell + 12] == raw + b'\xff' * (12 - len(raw))
            assert built[off:cell] == source[off:cell]
            # Les deux pointeurs de descriptions (16..23) peuvent déjà avoir
            # été relogés par les lots Pokédex ; les champs numériques restent EN.
            assert built[cell + 12:cell + 16] == source[cell + 12:cell + 16]
            assert built[cell + 24:cell + 36] == source[cell + 24:cell + 36]
            for relative in (16, 20):
                target = int.from_bytes(built[cell + relative:cell + relative + 4], 'little') - 0x08000000
                assert 0 <= target < len(built)
    probe = bytearray(built)
    assert apply_patches(probe, source)['relocated'] == 0
    assert probe == built


def test_finalizer_atomic_idempotent_and_bounded(source):
    rom = bytearray(source)
    stats = apply_patches(rom, source)
    assert stats['verified'] == 126 and stats['categories'] == 113
    after = bytes(rom)
    assert apply_patches(rom, source)['relocated'] == 0
    assert rom == after
    allowed = set()
    for offset, refs, raw in make_patch(source).entries():
        for ref in refs:
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(ref, ref + 4))
            allowed.update(range(target, target + len(raw)))
    for row in AUDIT['entries']:
        if row['kind'] == 'category':
            cell = int(row['consumer_offset'], 16)
            allowed.update(range(cell, cell + 12))
    assert {i for i, (a, b) in enumerate(zip(source, rom)) if a != b} <= allowed
    rom[AUDIT['table_references'][-1]] ^= 1
    before = bytes(rom)
    with pytest.raises(ValueError, match='Lecteur'):
        apply_patches(rom, source)
    assert rom == before


def test_native_category_reader_stride_and_copy_limit(source, built):
    # Thumb : (index * 8 + index) * 4 + base ; retour du record de 36 octets.
    # Le lecteur Pokédex copie ensuite au plus 11 caractères avant le terminateur.
    for rom in (source, built):
        assert rom[0x88E26:0x88E32] == bytes.fromhex('c80040188000014940187047')
        assert int.from_bytes(rom[0x88E34:0x88E38], 'little') == 0x09A357CC
        assert rom[0x105840:0x10584C] == bytes.fromhex('694609190831281900780870')
        assert rom[0x105856:0x10585E] == bytes.fromhex('ff280ed00a2cf0d9')
