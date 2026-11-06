"""PT-82 : livraison binaire, cinq polices natives et faux pointeurs protégés."""
import hashlib
import re

import pytest

from languages.pt.patches.batch_82 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths
from tests.unit.pt.test_batch_pt82 import AUDIT, LIVE, ROOT

pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_all_preimages_references_and_unreachable_exceptions(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        matches = [match.start() for match in re.finditer(
            re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert matches == sorted(row['references'] + row['non_text_references'])
        if row['index'] in (26, 98):
            assert row['status'] == 'exception' and not matches
            assert all((inside + 0x08000000).to_bytes(4, 'little') not in source
                       for inside in range(offset, offset + len(raw)))
        if row['index'] == 150:
            owner = int(row['owner_offset'], 16)
            parent = bytes.fromhex(AUDIT['entries'][149]['source_hex'])
            assert raw == parent[offset - owner:]
            for ref in row['owner_references']:
                assert int.from_bytes(source[ref:ref + 4], 'little') == owner + 0x08000000


def test_every_final_consumer_delivers_the_complete_translation(source, built):
    patch = make_patch(source)
    assert len(patch.entries()) == 297
    patch.verify(built)
    for row in LIVE:
        expected = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        for ref in row['references']:
            target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
            assert built[target:target + len(expected)] == expected
    probe = bytearray(built)
    assert patch.apply(probe) == {'verified': 297, 'relocated': 0}
    assert probe == built


def test_native_fonts_with_expanded_runtime_buffers(built):
    for row in LIVE:
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        buffers = {(0xFD, int(code)): text for code, text in row['buffers'].items()}
        for font, expected in zip(LATIN_FONTS, row['native_widths']):
            _, table = font.offsets(built)
            measured = [width for part in re.split(b'[\xfa\xfb]', raw)
                        for width in widths(part, built, table, buffers)]
            assert measured == expected, row['offset']
            assert max(measured) <= row.get('native_max_width', row['max_width']), row['offset']


def test_audio_false_pointer_is_inside_a_live_delta_pcm_wave(source, built):
    row = AUDIT['entries'][3]
    owner = row['binary_owner']
    start = int(owner['wave_base'], 16)
    end = int(owner['compressed_payload_end'], 16)
    header = bytes.fromhex(owner['header_hex'])
    assert source[start:start + 16] == header and header[:4] == bytes([1, 0, 0, 0])
    samples = int.from_bytes(header[12:16], 'little') + 1
    blocks, tail = divmod(samples, 64)
    assert samples == owner['decoded_samples']
    assert end == start + 16 + blocks * 33 + (1 + (tail + 1) // 2 if tail else 0)
    assert hashlib.sha256(source[start + 16:end]).hexdigest() == owner['payload_sha256']
    for instrument in owner['instrument_rows']:
        offset = int(instrument['offset'], 16)
        assert source[offset:offset + 12] == bytes.fromhex(instrument['hex'])
        assert built[offset:offset + 12] == source[offset:offset + 12]
        ref = int(instrument['pointer_site'], 16)
        assert int.from_bytes(source[ref:ref + 4], 'little') == start + 0x08000000
    for site in row['non_text_references']:
        assert start + 16 <= site and site + 4 <= end
    assert built[start:end] == source[start:end]


def test_fragment_false_pointer_is_a_pixel_in_a_live_sprite_frame(source, built):
    row = AUDIT['entries'][150]
    owner = row['binary_owner']
    start, end = int(owner['frame_base'], 16), int(owner['frame_end'], 16)
    assert end - start == owner['frame_bytes'] == 0x800
    assert hashlib.sha256(source[start:end]).hexdigest() == owner['frame_sha256']
    for image in owner['image_rows']:
        offset = int(image['offset'], 16)
        raw = bytes.fromhex(image['hex'])
        assert source[offset:offset + 8] == raw
        assert int.from_bytes(raw[:4], 'little') == start + 0x08000000
        assert int.from_bytes(raw[4:6], 'little') == 0x800
        assert built[offset:offset + 8] == raw
    ref = int(owner['template_pointer_site'], 16)
    assert source[ref:ref + 4] == bytes.fromhex(owner['template_pointer_hex'])
    assert int.from_bytes(source[ref:ref + 4], 'little') == int(owner['image_rows'][0]['offset'], 16) + 0x08000000
    assert built[ref:ref + 4] == source[ref:ref + 4]
    assert all(start <= site and site + 4 <= end for site in row['non_text_references'])
    assert built[start:end] == source[start:end]


def test_patch_atomic_idempotent_and_strictly_bounded(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 297
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 297, 'relocated': 0}
    assert rom == after
    allowed = set()
    for _, refs, raw in patch.entries():
        for ref in refs:
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(ref, ref + 4))
            allowed.update(range(target, target + len(raw)))
    assert {index for index, (before, final) in enumerate(zip(source, rom)) if before != final} <= allowed
    patch.definitions[-1] = dict(patch.definitions[-1], source_hex='00ff')
    with pytest.raises(ValueError, match='préimage'):
        patch.apply(rom)
    assert rom == after


def test_circus_dynamic_effects_follow_the_header_without_overflow(source, built):
    proof = AUDIT['runtime_279']
    for preimage in proof['preimages']:
        site = int(preimage['offset'], 16)
        raw = bytes.fromhex(preimage['source_hex'])
        assert source[site:site + len(raw)] == raw
        assert built[site:site + len(raw)] == raw
    row = AUDIT['entries'][279]
    header = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
    assert header.endswith(b'\xfe\xfd\x0c\xff')
    # Special 0x72 copie un effet entier (pages incluses), pas un simple nom.
    # Ses 32 chaînes appartiennent à PT-43 ; on suit les vrais pointeurs finaux.
    for entry in proof['entries']:
        site = entry['pointer_site']
        assert int.from_bytes(source[site:site + 4], 'little') == int(entry['source_target'], 16) + 0x08000000
        target = int.from_bytes(built[site:site + 4], 'little') - 0x08000000
        expected = TextEncoder.encode_pokemon(entry['portuguese'].replace(r'\n', '\n'), strict=True)
        assert built[target:target + len(expected)] == expected
        expanded = header[:-3] + expected
        pages = re.split(b'[\xfa\xfb]', expanded)
        assert pages[0].count(b'\xfe') == 1
        for font in LATIN_FONTS:
            _, table = font.offsets(built)
            assert max(width for page in pages for width in widths(page, built, table)) <= 208


def test_tier_query_buffers_are_the_three_format_names(source, built):
    row = AUDIT['entries'][298]
    template = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
    for proof in AUDIT['runtime_298']['entries']:
        call = int(proof['call_site'], 16)
        raw = bytes.fromhex(proof['source_hex'])
        assert source[call:call + 6] == raw and raw[:2] == b'\x85\x00'
        assert built[call:call + 2] == raw[:2]
        target = int.from_bytes(raw[2:6], 'little') - 0x08000000
        assert target == int(proof['source_target'], 16)
        expected = TextEncoder.encode_pokemon(proof['text'], strict=True)
        assert source[target:target + len(expected)] == expected
        # Ces noms sont hors PT-82 ; leur pointeur final reste l'autorité.
        live_target = int.from_bytes(built[call + 2:call + 6], 'little') - 0x08000000
        end = built.index(255, live_target)
        expanded = template.replace(b'\xfd\x02', built[live_target:end])
        for font in LATIN_FONTS:
            assert max(widths(expanded, built, font.offsets(built)[1])) <= 192
