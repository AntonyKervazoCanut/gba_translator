"""PT-56 : noms vivants, propriétaires graphiques et isolation du patch."""
import hashlib
import re

import pytest

from languages.fr.patches.font import lz77_decompress
from languages.fr.patches.mon_icon_repair import (
    ICON_STRIDE,
    MON_ICON_TABLE,
    MON_ICON_TABLE_ENTRIES,
)
from languages.pt.patches.batch_56 import apply_patches
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt56 import AUDIT, ROOT

pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


def test_source_pointers_and_all_graphics_exceptions(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    base = int(AUDIT['table_base'], 16)
    refs = [m.start() for m in re.finditer(re.escape((base + 0x08000000).to_bytes(4, 'little')), source)]
    assert refs == AUDIT['table_references'] and len(refs) == 42
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        refs = [m.start() for m in re.finditer(re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert refs == row['references']
        for owner in row.get('owners', []):
            site, start, size = owner['site'], owner['offset'], owner['size']
            assert int.from_bytes(source[site:site + 4], 'little') == start + 0x08000000
            assert start <= offset < start + size
            if owner['kind'] == 'icon':
                assert MON_ICON_TABLE <= site < MON_ICON_TABLE + MON_ICON_TABLE_ENTRIES * 4
                assert (site - MON_ICON_TABLE) % 4 == 0 and size == ICON_STRIDE
            else:
                decoded, consumed = lz77_decompress(source, start)
                assert len(decoded) == owner['decoded_bytes'] == 2048
                assert consumed == size


def test_built_names_widths_and_untouched_binary_entries(source):
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    for ref in AUDIT['table_references']:
        assert built[ref:ref + 4] == source[ref:ref + 4]
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        if row['status'] == 'exception_binary':
            for owner in row['owners']:
                start, size = owner['offset'], owner['size']
                assert built[start:start + size] == source[start:start + size], row['offset']
            continue
        raw = TextEncoder.encode_pokemon(row['portuguese'], strict=True)
        assert built[offset:offset + len(raw)] == raw
        for font, expected in zip(LATIN_FONTS, row['font_widths']):
            _, widths = font.offsets(built)
            assert sum(built[widths + c] for c in raw[:-1]) == expected <= 60
    probe = bytearray(built)
    assert apply_patches(probe, source) == 216
    assert probe == built


def test_repair_is_bounded_and_idempotent(source):
    probe = bytearray(source)
    allowed = set()
    for row in AUDIT['entries']:
        if row['status'] == 'retained_english':
            offset = int(row['offset'], 16)
            probe[offset:offset + 11] = b'\xff' * 11
            allowed.update(range(offset, offset + 11))
    before = bytes(probe)
    assert apply_patches(probe, source) == 216
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(before, probe)))
    for row in AUDIT['entries']:
        if row['status'] == 'retained_english':
            offset = int(row['offset'], 16)
            raw = TextEncoder.encode_pokemon(row['portuguese'], strict=True)
            assert probe[offset:offset + len(raw)] == raw
    first = bytes(probe)
    assert apply_patches(probe, source) == 216
    assert probe == first


def test_invalid_reader_and_preimage_fail_atomically(source):
    for position in [AUDIT['table_references'][-1], 0x166E11B]:
        bad_source = bytearray(source)
        bad_source[position] ^= 1
        probe = bytearray(source)
        with pytest.raises(ValueError, match='différent'):
            apply_patches(probe, bad_source)
        assert probe == source
