"""Préimages, lecteurs réels et injection finale des 300 cellules PT-53."""
import hashlib
import re
import struct

import pytest

from languages.pt.patches.batch_53 import apply_patches
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt53 import AUDIT, ROOT

pytestmark = pytest.mark.rom


def test_final_rom_cells_references_and_actual_font_budgets():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    refs = [m.start() for m in re.finditer(re.escape(struct.pack('<I', 0x0966A98C)), source)]
    assert refs == AUDIT['table_references'] and len(refs) == 42
    for ref in refs:
        assert built[ref:ref + 4] == source[ref:ref + 4]
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        assert source[off:off + 11].hex() == row['source_hex']
        assert built[off:off + 11].hex() == row['final_hex']
        encoded = TextEncoder.encode_pokemon(row['portuguese'], strict=True)
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            assert sum(built[widths + c] for c in encoded[:-1]) <= 70


def test_only_manifest_cells_are_written_and_patch_is_idempotent():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    probe = bytearray(source)
    expected = bytearray(source)
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        probe[off:off + 11] = b'\xff' * 11
        expected[off:off + 11] = bytes.fromhex(row['final_hex'])
    assert apply_patches(probe, source) == 300
    assert probe == expected
    assert apply_patches(probe, source) == 300
    assert probe == expected
    built = bytearray((ROOT / 'output/roms/GenedRom-pt.gba').read_bytes())
    before = bytes(built)
    apply_patches(built, source)
    assert built == before


@pytest.mark.parametrize('kind', ['reader', 'source', 'truncated'])
def test_preflight_failure_is_atomic(kind):
    source = bytearray((ROOT / 'input/roms/englishrom.gba').read_bytes())
    probe = bytearray(source)
    if kind == 'reader':
        probe[AUDIT['table_references'][-1]] ^= 1
    elif kind == 'source':
        source[int(AUDIT['entries'][-1]['offset'], 16)] ^= 1
    else:
        del probe[0x166BE16:]
    before = bytes(probe)
    with pytest.raises(ValueError, match='PT-53'):
        apply_patches(probe, source)
    assert probe == before
