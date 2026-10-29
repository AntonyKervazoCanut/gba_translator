"""PT-40 : noms réellement accessibles dans la ROM reconstruite."""
import hashlib
import re
import struct

import pytest

from src.core.font_glyphs import LATIN_FONTS
from tests.unit.pt.test_batch_pt40 import AUDIT, ROOT

pytestmark = pytest.mark.rom


def test_all_names_at_live_indexed_cells_after_build():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    pointer = struct.pack('<I', 0x08A40A10)
    refs = [m.start() for m in re.finditer(re.escape(pointer), source)]
    assert refs == AUDIT['table_pointer_matches']
    assert 0x308A4 in refs
    for at in refs:
        assert built[at:at + 4] == pointer
    base = struct.unpack_from('<I', built, 0x308A4)[0] - 0x08000000
    assert built[base:base + 2] == b'\xae\xff'
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        target = base + row['move_id'] * AUDIT['stride']
        assert source[offset:offset + 13] == raw
        assert built[target:target + 13] == raw, row['offset']
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            assert sum(built[widths + c] for c in raw[:row['encoded_bytes'] - 1]) <= 80
