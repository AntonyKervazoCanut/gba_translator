"""PT-69 : pointeurs vivants, préimages binaires et consommateurs natifs."""
import re

import pytest

from languages.pt.patches.batch_69 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths
from tests.unit.pt.test_batch_pt69 import ROOT, audit

pytestmark = pytest.mark.rom
AUDIT = audit()


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_every_reader_delivers_exact_translation(source, built):
    patch = make_patch(source)
    patch.verify_consumers(built)
    assert len(patch.entries()) == 293
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        matches = [m.start() for m in re.finditer(
            re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert sorted(matches) == sorted(row['references'] + row.get('non_text_references', []))
        if row['status'] == 'exception':
            assert not row['references']
            if 'owner_offset' in row:
                parent = int(row['owner_offset'], 16)
                owner = bytes.fromhex(row['owner_source_hex'])
                assert source[parent:parent + len(owner)] == owner
                assert raw == owner[offset - parent:]
                for ref in row['owner_sites']:
                    site = int(ref, 16)
                    assert int.from_bytes(source[site:site + 4], 'little') == parent + 0x08000000
            continue
        encoded = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        for ref in row['references']:
            target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
            assert built[target:target + len(encoded)] == encoded


def test_pixels_with_runtime_buffers_in_all_five_fonts(built):
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            continue
        encoded = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        buffers = {(0xFD, int(k)): v for k, v in row['buffers'].items()}
        measured = [max(max(widths(seg, built, font.offsets(built)[1], buffers))
                        for seg in re.split(b'[\xfa\xfb]', encoded)) for font in LATIN_FONTS]
        assert measured == row['expanded_widths'], row['offset']
        assert max(measured) <= 208, row['offset']


def test_excluded_matches_are_audio_or_code(source, built):
    for row in AUDIT['entries']:
        for pcm in row.get('pcm_matches', []):
            base, site, ref = pcm['wave_base'], pcm['site'], pcm['instrument_pointer']
            header = bytes.fromhex(pcm['header_hex'])
            assert source[base:base + 16] == header
            assert int.from_bytes(source[ref:ref + 4], 'little') == base + 0x08000000
            assert base + 16 <= site < base + 16 + int.from_bytes(header[12:16], 'little')
        for binary in row.get('binary_matches', []):
            start, raw = binary['base'], bytes.fromhex(binary['source_hex'])
            assert source[start:start + len(raw)] == raw
            assert built[start:start + len(raw)] == raw
    for site in AUDIT['preserved_sites']:
        assert built[site:site + 4] == source[site:site + 4]


def test_patch_atomic_idempotent_and_strictly_bounded(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 293
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 293, 'relocated': 0}
    assert bytes(rom) == after
    allowed = set()
    for _, refs, encoded in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(target, target + len(encoded)))
    for row in AUDIT['native_edits']:
        allowed.update(range(row['offset'], row['offset'] + len(bytes.fromhex(row['expected_hex']))))
    for row in AUDIT['local_buffers']:
        site = row['call_site']
        allowed.update(range(site, site + 5))
        target = int.from_bytes(rom[site + 1:site + 5], 'little') - 0x08000000
        allowed.update(range(target, target + len(patch._wrapper(row, rom))))
    assert {i for i, (a, b) in enumerate(zip(source, rom)) if a != b} <= allowed
    site = AUDIT['local_buffers'][0]['call_site']
    rom[site] = 0
    corrupted = bytes(rom)
    with pytest.raises(ValueError, match='préimage appel'):
        patch.apply(rom)
    assert bytes(rom) == corrupted
    with pytest.raises(ValueError, match='préimage ROM'):
        make_patch(bytes(1) + source[1:])


def test_only_local_gender_calls_are_replaced_and_cafe_possessive_is_gone(source, built):
    for row in AUDIT['local_buffers']:
        site = row['call_site']
        assert source[site:site + 5] == bytes.fromhex(row['source_hex'])
        target = int.from_bytes(built[site + 1:site + 5], 'little') - 0x08000000
        wrapper = built[target:target + 12]
        assert wrapper[:5] == source[site:site + 5]
        assert wrapper[5:7] == bytes([0x85, row['buffer_slot']])
        empty = int.from_bytes(wrapper[7:11], 'little') - 0x08000000
        assert built[empty] == 255 and wrapper[-1] == 3
    # Helpers partagés et chaînes des autres lots restent à leurs propriétaires.
    for helper in (0x1E92DC2, 0x1E68354):
        assert built[helper:helper + 30] == source[helper:helper + 30]
    assert built[0x1EBB938:0x1EBB93A] == b'\xf0\x23'
    assert built[0x1EBBB88:0x1EBBB8C] == b'\xf0\x00\xff\xff'


def test_quiz_native_table_reads_the_ten_portuguese_answers(source, built):
    for i, row in enumerate(AUDIT['entries'][50:60]):
        site = 0x1FB583C + i * 4
        assert row['references'] == [site]
        target = int.from_bytes(built[site:site + 4], 'little') - 0x08000000
        expected = TextEncoder.encode_pokemon(row['portuguese'])
        assert built[target:target + len(expected)] == expected
    for name in ('selector', 'normalizer'):
        meta = AUDIT['special_consumers']['quiz']
        start = int(meta[name + '_function'], 16)
        raw = bytes.fromhex(meta[name + '_source_hex'])
        assert built[start:start + len(raw)] == source[start:start + len(raw)] == raw


def test_cafe_complete_concatenations_fit_with_long_nicknames_and_counters(built):
    rows = AUDIT['entries']
    fragment = lambda n: TextEncoder.encode_pokemon(
        rows[n]['portuguese'].replace(r'\n', '\n'), strict=True)[:-1]
    for nickname in ('W' * 10, 'S' * 10):
        prefix = TextEncoder.encode_pokemon(nickname + ': ')[:-1]
        # Les six statistiques réellement sélectionnables sont lues dans la ROM finale.
        for index in range(6):
            site = 0x3FD5D0 + index * 4
            target = int.from_bytes(built[site:site + 4], 'little') - 0x08000000
            stat = built[target:built.index(b'\xff', target)]
            for direction in (92, 93):
                text = prefix + stat + fragment(91) + fragment(direction) + TextEncoder.encode_pokemon('255')
                for font in LATIN_FONTS:
                    assert max(widths(text, built, font.offsets(built)[1])) <= 208
        for font in LATIN_FONTS:
            assert max(widths(prefix + fragment(90) + b'\xff', built, font.offsets(built)[1])) <= 208
