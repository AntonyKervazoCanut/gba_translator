"""PT-77 : consommateurs vivants, polices natives et audio delta-PCM préservé."""
import hashlib
import re

import pytest

from languages.pt.patches.batch_77 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths
from tests.unit.pt.test_batch_pt77 import AUDIT, LIVE, ROOT

pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_source_preimages_all_references_and_exceptions(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        matches = [m.start() for m in re.finditer(
            re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert matches == sorted(row['references'] + row['non_text_references'])
        if row['index'] == 59:
            owner = int(row['owner_offset'], 16)
            assert owner == offset + 1 and source[offset] == 0
            for ref in row['owner_references']:
                assert int.from_bytes(source[ref:ref + 4], 'little') == owner + 0x08000000
        if row['index'] == 284:
            assert source[0x1E8E29C:0x1E8E2A2] == bytes.fromhex('0f0069a9f609')
            assert all((inside + 0x08000000).to_bytes(4, 'little') not in source
                       for inside in range(offset, offset + len(raw)))


def test_all_final_consumers_and_idempotence(source, built):
    patch = make_patch(source)
    assert len(patch.entries()) == 298
    patch.verify(built)
    probe = bytearray(built)
    assert patch.apply(probe) == {'verified': 298, 'relocated': 0}
    assert probe == built


def test_native_font_widths_with_expanded_buffers(built):
    for row in LIVE:
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        buffers = {(0xFD, int(k)): v for k, v in row['buffers'].items()}
        for font, expected in zip(LATIN_FONTS, row['native_widths']):
            _, table = font.offsets(built)
            measured = [w for part in re.split(b'[\xfa\xfb]', raw)
                        for w in widths(part, built, table, buffers)]
            assert measured == expected, row['offset']
            if row['kind'] != 'safari_hud' or font == LATIN_FONTS[0]:
                assert max(measured) <= row.get('native_max_width', row['max_width']), (row['offset'], measured)


def test_false_reference_is_inside_compressed_wave_and_audio_unchanged(source, built):
    row = next(r for r in LIVE if r['non_text_references'])
    owner = row['binary_owner']
    start = int(owner['wave_base'], 16)
    end = int(owner['compressed_payload_end'], 16)
    assert source[start:start + 16] == bytes.fromhex(owner['header_hex'])
    samples = int.from_bytes(source[start + 12:start + 16], 'little') + 1
    blocks, tail = divmod(samples, 64)
    # Le bloc partiel contient sa base, un octet low-only, puis les paires high/low.
    # Onze échantillons exigent sept octets, comme l'encodeur aif2pcm de pret.
    assert end == start + 16 + blocks * 33 + (1 + (tail + 1) // 2 if tail else 0)
    assert hashlib.sha256(source[start + 16:end]).hexdigest() == owner['payload_sha256']
    for instrument in owner['instrument_rows']:
        offset = int(instrument['offset'], 16)
        assert source[offset:offset + 12] == bytes.fromhex(instrument['hex'])
    assert built[start:end] == source[start:end]
    for site in row['non_text_references']:
        assert start + 16 <= site < end
        assert built[site:site + 4] == source[site:site + 4]


def test_patch_atomic_bounded_and_idempotent(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 298
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 298, 'relocated': 0}
    assert rom == after
    allowed = set()
    for _, refs, raw in patch.entries():
        for ref in refs:
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(ref, ref + 4))
            allowed.update(range(target, target + len(raw)))
    assert {i for i, (a, b) in enumerate(zip(source, rom)) if a != b} <= allowed
    patch.definitions[-1] = dict(patch.definitions[-1], source_hex='00ff')
    with pytest.raises(ValueError, match='préimage'):
        patch.apply(rom)
    assert rom == after


def test_safari_hud_window_font_and_single_line_contract(source, built):
    hud = AUDIT['safari_hud']
    for proof in (hud['window_template'], hud['render']):
        offset = int(proof.get('offset', proof.get('routine')), 16)
        raw = bytes.fromhex(proof['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        assert built[offset:offset + len(raw)] == raw
    assert hud['window_template']['pixel_height'] == 16
    assert hud['render']['font_id'] == 0 and hud['render']['x'] == 3
    assert hud['render']['max_width'] == 237
    _, table = LATIN_FONTS[0].offsets(built)
    for proof in hud['entries']:
        row = AUDIT['entries'][proof['index']]
        assert row['portuguese'] == proof['text']
        assert r'\n' not in row['portuguese']
        raw = TextEncoder.encode_pokemon(row['portuguese'], strict=True)
        code = 3 if proof['index'] == 185 else 2
        for buffer, expected in proof['buffers'].items():
            assert widths(raw, built, table, {(253, code): buffer}) == [expected]
            assert expected <= 237
