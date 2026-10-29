"""PT-39 : consommateurs réels, ROM finale et écritures strictement bornées."""
import hashlib
import re
import struct

import pytest

from languages.pt.patches.batch_39 import apply_patches, make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt39 import AUDIT, ROOT

pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


def test_preimages_and_exhaustive_absolute_references(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[off:off + len(raw)] == raw
        refs = [m.start() for m in re.finditer(
            re.escape(struct.pack('<I', off + 0x08000000)), source)]
        assert refs == row['references'], row['offset']
    # Le code ARM/Thumb du résumé charge la table de descriptions courante.
    for instruction, literal in ((0xE541A, 0xE5440), (0x137B7A, 0x137BC8), (0x9F3B4C, 0x9F3B64)):
        opcode = struct.unpack_from('<H', source, instruction)[0]
        assert opcode & 0xF800 == 0x4800
        assert ((instruction + 4) & ~3) + (opcode & 0xFF) * 4 == literal
        assert struct.unpack_from('<I', source, literal)[0] == 0x0899F194
    assert struct.unpack_from('<I', source, 0x308A4)[0] == 0x08A40A10


def test_live_final_rom_bytes_and_real_font_budgets(source):
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    make_patch(source).verify(built)
    assert struct.unpack_from('<I', built, 0x308A4)[0] == 0x08A40A10
    for row in AUDIT['entries']:
        encoded = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        targets = ([int(row['offset'], 16)] if row['kind'] == 'name' else
                   [struct.unpack_from('<I', built, ref)[0] - 0x08000000 for ref in row['references']])
        for target in targets:
            assert built[target:target + len(encoded)] == encoded, row['offset']
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            for line in encoded[:-1].split(b'\xfe'):
                assert sum(built[widths + c] for c in line) <= 122, (row['offset'], font)
    probe = bytearray(built)
    assert apply_patches(probe, source) == {'verified': 149, 'relocated': 0, 'names': 133}
    assert probe == built


def test_patch_is_atomic_and_does_not_touch_other_offsets(source):
    probe = bytearray(source)
    apply_patches(probe, source)
    allowed = bytearray(len(probe))
    for row in AUDIT['entries']:
        size = row['encoded_bytes']
        if row['kind'] == 'name':
            start = int(row['offset'], 16)
            allowed[start:start + size] = b'\1' * size
        else:
            for ref in row['references']:
                allowed[ref:ref + 4] = b'\1' * 4
                target = struct.unpack_from('<I', probe, ref)[0] - 0x08000000
                allowed[target:target + size] = b'\1' * size
    assert all(a == b or allowed[i] for i, (a, b) in enumerate(zip(source, probe)))
    before = bytes(probe)
    assert apply_patches(probe, source)['relocated'] == 0
    assert probe == before
    corrupt = bytearray(source)
    corrupt[0x308A4] ^= 1
    before = bytes(corrupt)
    with pytest.raises(ValueError, match='Table de noms'):
        apply_patches(corrupt, source)
    assert corrupt == before
