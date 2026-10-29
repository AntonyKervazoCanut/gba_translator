"""Contrôle des 282 cellules réellement lues dans la ROM finale PT."""
import hashlib
import re
import struct

import pytest

from languages.pt.patches.batch_41 import apply_patches
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt41 import AUDIT, ROOT

pytestmark = pytest.mark.rom


def test_source_and_final_live_cells_and_actual_font_widths():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    refs = [m.start() for m in re.finditer(re.escape(struct.pack('<I', 0x08A40A10)), source)]
    assert refs == AUDIT['table_references'] and len(refs) == 41
    for ref in refs:
        assert built[ref:ref + 4] == source[ref:ref + 4]
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        cell = bytes.fromhex(row['source_hex'])
        assert built[off:off + 13] == source[off:off + 13] == cell
        encoded = TextEncoder.encode_pokemon(row['portuguese'], strict=True)
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            assert sum(built[widths + c] for c in encoded[:-1]) <= 80


def test_patch_repairs_only_manifest_cells_and_is_idempotent():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    probe = bytearray(source)
    allowed = set()
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        probe[off:off + 13] = b'\xff' * 13
        allowed.update(range(off, off + 13))
    before = bytes(probe)
    assert apply_patches(probe, source) == 282
    assert probe == source
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(before, probe)))
    assert apply_patches(probe, source) == 282
    assert probe == source
    built = bytearray((ROOT / 'output/roms/GenedRom-pt.gba').read_bytes())
    before = bytes(built)
    apply_patches(built, source)
    assert built == before


def test_changed_reader_rejected_without_partial_write():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    probe = bytearray(source)
    probe[AUDIT['table_references'][-1]] ^= 1
    before = bytes(probe)
    with pytest.raises(ValueError, match='Lecteur'):
        apply_patches(probe, source)
    assert probe == before
