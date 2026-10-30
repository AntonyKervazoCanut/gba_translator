"""PT-68 : texte réellement livré, tables vivantes, écritures et pixels bornés."""
import hashlib
import re

import pytest

from languages.pt.patches.batch_68 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths
from tests.unit.pt.test_batch_pt68 import AUDIT, ROOT

pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source() -> bytes:
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built() -> bytes:
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_every_source_reader_delivers_the_complete_translation(source, built):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    patch = make_patch(source)
    assert len(patch.entries()) == 296
    patch.verify(built)
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            continue
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        refs = [m.start() for m in re.finditer(
            re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert refs == row['references']
        encoded = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        for ref in refs:
            target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
            assert built[target:target + len(encoded)] == encoded


def test_finalizer_atomic_idempotent_and_bounded(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 296
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 296, 'relocated': 0}
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


def test_actual_fonts_with_expanded_names_counters_dates_and_plural_suffixes(built):
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            continue
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        buffers = {(0xFD, int(j)): value for j, value in row['buffers'].items()}
        measured = []
        for font in LATIN_FONTS:
            _, table = font.offsets(built)
            measured.append(max(max(widths(segment, built, table, buffers))
                                for segment in re.split(b'[\xfa\xfb]', raw)))
        assert measured == row['expanded_widths'], row['offset']
        assert max(measured) <= row['pixel_budget'], row['offset']


def test_exceptions_and_neighbor_pointers(source, built):
    for row in AUDIT['entries']:
        if row['status'] != 'exception':
            continue
        offset = int(row['offset'], 16)
        assert (offset + 0x08000000).to_bytes(4, 'little') not in source
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        if 'owner_offset' in row:
            owner = int(row['owner_offset'], 16)
            raw = bytes.fromhex(row['owner_source_hex'])
            for site in row['owner_sites']:
                assert int.from_bytes(source[site:site + 4], 'little') == owner + 0x08000000
                live = int.from_bytes(built[site:site + 4], 'little') - 0x08000000
                assert built[live:live + len(raw)] == raw
        else:
            for neighbor in row['neighbor_offsets']:
                adjacent = next(r for r in AUDIT['entries'] if r['offset'] == neighbor)
                assert adjacent['references']
