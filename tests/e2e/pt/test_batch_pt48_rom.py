"""PT-48 : tous les pointeurs, tables et octets de la ROM finale sont vérifiés."""
import hashlib
import re

import pytest

from languages.fr.patches.font import lz77_decompress
from languages.pt.patches.batch_48 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths
from tests.unit.pt.test_batch_pt48 import AUDIT, ROOT

pytestmark = pytest.mark.rom


def test_final_rom_live_consumers_and_binary_exceptions():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    make_patch(source).verify(built)
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        original = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(original)] == original
        ptr = (offset + 0x08000000).to_bytes(4, 'little')
        assert row['references'] == [m.start() for m in re.finditer(re.escape(ptr), source)]
        if row['status'] == 'exception':
            if 'compression' in row:
                decoded, size = lz77_decompress(source, offset)
                assert len(decoded) == row['compression']['decompressed_bytes']
                assert size == row['compression']['compressed_bytes']
                assert hashlib.sha256(decoded).hexdigest() == row['compression']['sha256']
                assert built[offset:offset + size] == source[offset:offset + size]
                for ref in row['references']:
                    assert built[ref:ref + 4] == ptr
            else:
                assert not row['references']
                assert built[offset:offset + len(original)] == original
            continue
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        for ref in row['references']:
            target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
            assert built[target:target + len(raw)] == raw, row['offset']
        for font in LATIN_FONTS:
            _, table = font.offsets(built)
            assert max(widths(raw, built, table, {})) <= 192, row['offset']


def test_patch_is_atomic_bounded_and_idempotent():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 173
    before = bytes(rom)
    assert patch.apply(rom) == {'verified': 173, 'relocated': 0}
    assert bytes(rom) == before
    allowed = set()
    for _, refs, raw in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(target, target + len(raw)))
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(source, rom)))
    row = next(r for r in patch.definitions if r['status'] == 'translated')
    patch.texts[int(row['offset'], 16)] = 'x' * 200
    with pytest.raises(ValueError, match='largeur dépassée'):
        patch.apply(rom)
    assert bytes(rom) == before
