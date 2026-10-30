"""PT-74 : livraison exacte, polices réelles, tables et préimages binaires."""
import re

import pytest

from languages.pt.patches.batch_74 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths
from tests.unit.pt.test_batch_pt74 import ROOT, audit

pytestmark = pytest.mark.rom
AUDIT = audit()


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_every_live_pointer_delivers_the_complete_translation(source, built):
    patch = make_patch(source)
    patch.verify(built)
    assert len(patch.entries()) == 296
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        matches = [m.start() for m in re.finditer(
            re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert sorted(matches) == sorted(row['references'] + row['non_text_references'])
        if row['status'] == 'exception':
            assert not matches
            if 'owner_offset' in row:
                owner = int(row['owner_offset'], 16)
                assert owner == offset + 1 and raw[0] == 0
                assert raw[1:] == bytes.fromhex(row['owner_source_hex'])
                for site in row['owner_sites']:
                    ref = int(site, 16)
                    assert int.from_bytes(source[ref:ref + 4], 'little') == owner + 0x08000000
            else:
                assert built[offset:offset + len(raw)] == raw
                for site, target in zip(row['neighbor_sites'], row['neighbor_targets']):
                    assert int.from_bytes(source[site:site + 4], 'little') == int(target, 16) + 0x08000000
            continue
        encoded = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        for ref in row['references']:
            target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
            assert built[target:target + len(encoded)] == encoded


def test_all_five_fonts_with_expanded_runtime_buffers(built):
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            continue
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        buffers = {(0xFD, int(k)): v for k, v in row['buffers'].items()}
        measured = [max(max(widths(seg, built, font.offsets(built)[1], buffers))
                        for seg in re.split(b'[\xfa\xfb]', raw)) for font in LATIN_FONTS]
        assert measured == row['expanded_widths'], row['offset']
        assert max(measured) <= row['pixel_budget'], row['offset']
        if 'small_font_budget' in row:
            assert measured[0] <= row['small_font_budget'] == 32


def test_dpcm_false_pointer_and_window_templates_remain_intact(source, built):
    row = AUDIT['entries'][114]
    pcm = row['pcm_matches'][0]
    base, site = pcm['wave_base'], pcm['site']
    header = bytes.fromhex(pcm['header_hex'])
    assert source[base:base + 16] == header
    assert header[:2] == b'\x01\x00'
    samples = int.from_bytes(header[12:16], 'little')
    size = (samples + 63) // 64 * 33
    assert size == pcm['stored_bytes'] and samples == pcm['sample_count']
    for ref in pcm['instrument_pointers']:
        assert int.from_bytes(source[ref:ref + 4], 'little') == base + 0x08000000
    assert base + 16 <= site < base + 16 + size
    assert built[base:base + 16 + size] == source[base:base + 16 + size]
    assert built[0x1FB4174:0x1FB41AC] == source[0x1FB4174:0x1FB41AC]


def test_patch_atomic_idempotent_and_strictly_bounded(source):
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
    assert bytes(rom) == after
    with pytest.raises(ValueError, match='préimage ROM'):
        make_patch(bytes(1) + source[1:])
