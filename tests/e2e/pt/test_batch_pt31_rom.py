"""PT-31 : preuve binaire des 286 noms dans la table réellement consommée."""
import hashlib
import re
import struct

import pytest

from src.core.font_glyphs import LATIN_FONTS
from tests.unit.pt.test_batch_pt31 import AUDIT, ROOT

pytestmark = pytest.mark.rom


def test_live_indexed_names_and_residual_padding_in_built_rom():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    assert source[0x9A89C:0x9A8DC].hex() == AUDIT['accessor_hex']
    assert built[0x9A89C:0x9A8DC] == source[0x9A89C:0x9A8DC]
    assert struct.unpack_from('<I', built, 0x9A8D8)[0] == 0x08000000 + 0x876200
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        refs = [m.start() for m in re.finditer(
            re.escape(struct.pack('<I', offset + 0x08000000)), source)]
        assert refs == row['references']
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        assert built[offset:offset + len(raw)] == raw, row['offset']
        cell = int(row['cell'], 16)
        if row['status'] == 'exception':
            assert 0xFF in source[cell:offset] and not refs
            continue
        # Le nom est indexé, sans pointeur individuel : aucune relocation permise.
        assert offset == 0x876200 + 44 * row['item_id']
        assert built[cell + 13:cell + 20] == source[cell + 13:cell + 20]
        assert built[cell + 24:cell + 44] == source[cell + 24:cell + 44]
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            assert sum(built[widths + c] for c in raw[:-1]) <= 78
