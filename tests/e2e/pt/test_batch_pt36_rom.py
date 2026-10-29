"""PT-36 : octets injectés, lecteurs réels, exceptions mortes et idempotence."""
import hashlib
import re
import struct

import pytest

from languages.pt.patches.batch_36 import apply_patches, make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt36 import AUDIT, ROOT

pytestmark = pytest.mark.rom


def test_live_consumers_in_final_rom_and_dead_exceptions():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    make_patch(source).verify(built)
    for prefix in ('name', 'custom'):
        at = int(AUDIT[f'{prefix}_accessor_offset'], 16)
        code = bytes.fromhex(AUDIT[f'{prefix}_accessor_hex'])
        assert built[at:at + len(code)] == source[at:at + len(code)] == code
    assert struct.unpack_from('<I', built, 0x9A9CDC)[0] == 0x08A36398
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[off:off + len(raw)] == raw
        refs = [m.start() for m in re.finditer(
            re.escape(struct.pack('<I', off + 0x08000000)), source)]
        assert refs == row['references']
        if row['status'] == 'exception':
            ref = int(row['live_reference'], 16)
            assert struct.unpack_from('<I', source, ref)[0] == int(row['live_target'], 16) + 0x08000000
            assert not refs
            continue
        encoded = TextEncoder.encode_pokemon(row['portuguese'], strict=True)
        targets = ([off] if row['kind'] == 'name' else
                   [struct.unpack_from('<I', built, ref)[0] - 0x08000000 for ref in refs])
        for target in targets:
            assert built[target:target + len(encoded)] == encoded, row['offset']
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            assert sum(built[widths + c] for c in encoded[:-1]) <= (120 if row['kind'] == 'name' else 192)


def test_patch_is_idempotent_and_does_not_write_outside_manifest():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = bytearray((ROOT / 'output/roms/GenedRom-pt.gba').read_bytes())
    before = bytes(built)
    stats = apply_patches(built, source)
    assert stats == {'verified': 184, 'relocated': 0, 'names': 95}
    assert built == before
    # Sur EN, les cellules sont fixes ; toutes les autres écritures passent
    # exclusivement par les références déclarées et leurs nouvelles cibles.
    probe = bytearray(source)
    apply_patches(probe, source)
    allowed = bytearray(len(probe))
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            continue
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
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            off = int(row['offset'], 16)
            size = len(bytes.fromhex(row['source_hex']))
            assert probe[off:off + size] == source[off:off + size]
