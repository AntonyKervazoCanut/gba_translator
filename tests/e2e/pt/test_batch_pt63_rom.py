"""PT-63 : octets livrés, pointeurs vivants et budgets des cinq polices."""
import hashlib
import re

import pytest

from languages.pt.patches.batch_63 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths
from tests.unit.pt.test_batch_pt63 import AUDIT, ROOT

pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_source_pointers_and_documented_exceptions(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[off:off + len(raw)] == raw
        assert [m.start() for m in re.finditer(
            re.escape((off + 0x08000000).to_bytes(4, 'little')), source)] == sorted(
                row['references'] + row.get('non_text_references', []))
        if 'consumer_offset' in row:
            target = int(row['consumer_offset'], 16)
            assert [m.start() for m in re.finditer(
                re.escape((target + 0x08000000).to_bytes(4, 'little')), source)] == row['consumer_references']
        if row['status'] == 'exception':
            assert source[off - 16:off + 32] == bytes.fromhex(row['context_hex'])
            ref = int(row['replacement_pointer'], 16)
            assert int.from_bytes(source[ref:ref + 4], 'little') == int(row['replacement_target'], 16) + 0x08000000


def test_final_delivery_and_unused_text_preserved(source, built):
    patch = make_patch(source)
    assert len(patch.entries()) == 291
    patch.verify(built)
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            off = int(row['offset'], 16)
            raw = bytes.fromhex(row['source_hex'])
            assert built[off:off + len(raw)] == raw
    probe = bytearray(built)
    assert patch.apply(probe) == {'verified': 291, 'relocated': 0}
    assert probe == built


def test_native_font_budgets_and_expanded_runtime_buffers(built):
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            continue
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        buffers = {(0xFD, int(k)): v for k, v in row['buffers'].items()}
        for font in LATIN_FONTS:
            _, table = font.offsets(built)
            for page in re.split(b'[\xfa\xfb]', raw):
                measured = widths(page, built, table, buffers)
                assert max(measured) <= row['native_max_width'], (row['offset'], font.glyph_pointer, measured)


def test_finalizer_atomic_idempotent_and_bounded(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 291
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 291, 'relocated': 0}
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


def test_alignment_and_pcm_are_not_text_consumers(source, built):
    row = AUDIT['entries'][20]
    assert row['offset'] == '0x1efecf6' and row['references'] == []
    assert row['consumer_references'] == [0x1FB2E40, 0x1FB3EAC]
    assert built[0x1EFECF6:0x1EFECF8] == source[0x1EFECF6:0x1EFECF8] == b'\xc0\x46'
    assert built[0x141EB2B:0x141EB2F] == source[0x141EB2B:0x141EB2F]
    patch = make_patch(source)
    broken = bytearray(built)
    for entry in AUDIT['entries']:
        for site in entry.get('non_text_references', []):
            broken[site:site + 4] = (0x08123456).to_bytes(4, 'little')
    broken[0x1EFECF6:0x1EFECF8] = b'\0\0'
    with pytest.raises(ValueError, match='non textuelle'):
        patch.verify(broken)
    assert patch.apply(broken)['verified'] == 291
    assert broken == built
    broken_source = bytearray(source)
    broken_source[row['pcm_matches'][0]['wave_base']] ^= 1
    with pytest.raises(ValueError, match='préimage'):
        make_patch(broken_source)


def test_binary_owners_are_real_code_audio_and_compressed_graphics(source, built):
    from languages.fr.patches.font import lz77_decompress

    for row in AUDIT['entries']:
        for binary in row.get('binary_matches', []):
            base = binary['base']
            data = bytes.fromhex(binary['source_hex'])
            assert source[base:base + len(data)] == built[base:base + len(data)] == data
            if binary['kind'] == 'LZ77 graphics':
                output, consumed = lz77_decompress(source, base)
                assert consumed == len(data) and len(output) == binary['decompressed_bytes']
                ref = binary['owner_pointer']
                assert int.from_bytes(source[ref:ref + 4], 'little') == base + 0x08000000
            else:
                # Thumb : adds r0,r0,r1 suivi de bl 0x889cf46 ; le match
                # commence dans le second octet de adds, pas dans un littéral.
                assert binary['site'] == 0x89CF2F
                assert source[0x89CF2E:0x89CF34] == bytes.fromhex('401800f009f8')
        for pcm in row.get('pcm_matches', []):
            base, ref, site = pcm['wave_base'], pcm['instrument_pointer'], pcm['site']
            header = bytes.fromhex(pcm['header_hex'])
            assert source[base:base + 16] == header
            assert int.from_bytes(source[ref:ref + 4], 'little') == base + 0x08000000
            assert base + 16 <= site <= base + 12 + int.from_bytes(header[12:16], 'little')
            assert built[site:site + 4] == source[site:site + 4]
