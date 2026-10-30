"""PT-59 : octets finaux, lecteurs, exceptions, bornes et métriques réelles."""
import hashlib
import re

import pytest

from languages.pt.patches.batch_59 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths
from tests.unit.pt.test_batch_pt59 import AUDIT, ROOT

pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_source_references_and_final_delivery(source, built):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    patch = make_patch(source)
    assert len(patch.entries()) == 298
    patch.verify(built)
    # Faux pointeur au sein d'un échantillon sonore : conservation intégrale.
    assert built[0x5758AC:0x5758AC + 16 + 12030] == source[0x5758AC:0x5758AC + 16 + 12030]
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        refs = [m.start() for m in re.finditer(
            re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert refs == row.get('raw_references', row['references'])
        refs = row['references']
        if row['status'] == 'exception':
            assert source[offset - 1] == 0xFF and not refs
            assert built[offset:offset + len(raw)] == raw
            for neighbor in row['related_consumers']:
                for ref in neighbor['references']:
                    assert int.from_bytes(source[ref:ref + 4], 'little') == int(neighbor['offset'], 16) + 0x08000000
            continue
        encoded = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        for ref in refs:
            target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
            assert built[target:target + len(encoded)] == encoded


def test_patch_atomic_idempotent_bounded(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 298
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 298, 'relocated': 0}
    assert bytes(rom) == after
    allowed = set()
    for _, refs, encoded in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(target, target + len(encoded)))
    assert {i for i, (a, b) in enumerate(zip(source, rom)) if a != b} <= allowed
    patch.definitions[0] = dict(patch.definitions[0], source_hex='00ff')
    with pytest.raises(ValueError, match='préimage'):
        patch.apply(rom)
    assert rom == after


def test_actual_fonts_and_expanded_buffers(built):
    for i, row in enumerate(AUDIT['entries']):
        if row['status'] == 'exception':
            continue
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        buffers = {(0xFD, j): 'W' * 10 for j in range(16)}
        if i in (187, 188):
            buffers.update({(0xFD, 2): '12', (0xFD, 3): '31', (0xFD, 4): '2000', (0xFD, 7): '99'})
        if i == 254:
            buffers.update({(0xFD, 2): 'Blue Shard', (0xFD, 3): '99'})
        if i in (212, 213, 269, 271):
            buffers.update({(0xFD, 2): '999', (0xFD, 3): '999'})
        if i in (47, 48, 50, 52, 54, 55, 56):
            buffers[(0xFD, 4)] = 'moça'
        for font in LATIN_FONTS:
            _, table = font.offsets(built)
            for segment in re.split(b'[\xfa\xfb]', raw):
                assert max(widths(segment, built, table, buffers)) <= (172 if i == 146 else 208), row['offset']
    # La mission est un appel BB/00 avec un pointeur, pas une cellule fixe adjacente.
    assert built[0x1E5599E:0x1E559A0] == b'\xbb\x00'
