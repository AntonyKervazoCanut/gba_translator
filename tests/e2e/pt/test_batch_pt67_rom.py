"""PT-67 : injection réelle, pointeurs, préimages et budgets des cinq polices."""
import hashlib
import re

import pytest

from languages.fr.patches.font import lz77_decompress
from languages.pt.patches.batch_67 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths
from tests.unit.pt.test_batch_pt67 import AUDIT, LIVE, ROOT

pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_exact_preimages_pointers_and_two_padding_prefixes(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[off:off + len(raw)] == raw
        matches = [m.start() for m in re.finditer(
            re.escape((off + 0x08000000).to_bytes(4, 'little')), source)]
        excluded = [int(m['site'], 16) for m in row['non_text_matches']]
        assert matches == sorted(row['references'] + excluded)
        if row['status'] == 'exception':
            assert source[off - 16:off + 32] == bytes.fromhex(row['context_hex'])
            assert raw[0] == 0
            for ref in row['owner_references']:
                assert int.from_bytes(source[ref:ref + 4], 'little') == off + 1 + 0x08000000
    assert [(r['offset'], r['owner_offset']) for r in AUDIT['entries']
            if r['status'] == 'exception'] == [('0x1f219df', '0x1f219e0'),
                                               ('0x1f21c7f', '0x1f21c80')]


def test_all_live_consumers_after_build_and_unchanged_padding(source, built):
    patch = make_patch(source)
    assert len(patch.entries()) == 298
    patch.verify(built)
    # Les espaces fantômes sont intacts ; les cibles utiles sont repointées.
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            off = int(row['offset'], 16)
            assert built[off] == source[off] == 0
    probe = bytearray(built)
    assert patch.apply(probe) == {'verified': 298, 'relocated': 0}
    assert probe == built


def test_native_five_font_budgets_and_expanded_buffers(built):
    for row in LIVE:
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        buffers = {(0xFD, int(k)): v for k, v in row['buffers'].items()}
        for font, expected in zip(LATIN_FONTS, row['native_widths']):
            _, table = font.offsets(built)
            measured = [w for part in re.split(b'[\xfa\xfb]', raw)
                        for w in widths(part, built, table, buffers)]
            assert measured == expected
            assert max(measured) <= row['max_width'], (row['offset'], font.glyph_pointer, measured)


def test_patch_bounded_atomic_and_idempotent(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 298
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 298, 'relocated': 0}
    assert rom == after
    allowed = set()
    spans = []
    for _, refs, raw in patch.entries():
        spans.extend((ref, raw) for ref in refs)
    spans.extend(patch.context_entries())
    for ref, raw in spans:
        target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
        allowed.update(range(ref, ref + 4))
        allowed.update(range(target, target + len(raw)))
    assert {i for i, (a, b) in enumerate(zip(source, rom)) if a != b} <= allowed
    patch.definitions[-1] = dict(patch.definitions[-1], source_hex='00ff')
    with pytest.raises(ValueError, match='préimage'):
        patch.apply(rom)
    assert rom == after


def test_non_text_matches_have_binary_owners_and_are_preserved(source, built):
    evidence = [m for r in LIVE for m in r['non_text_matches']]
    assert len(evidence) == 6
    for match in evidence:
        site = int(match['site'], 16)
        assert built[site:site + 4] == source[site:site + 4]
        if match['kind'] == 'PCM M4A':
            base, end = int(match['wave_base'], 16), int(match['sample_end'], 16)
            ref = int(match['instrument_pointer'], 16)
            assert int.from_bytes(source[ref:ref + 4], 'little') == base + 0x08000000
            assert source[base:base + 16] == bytes.fromhex(match['wave_header_hex'])
            assert base + 16 <= site < end
            assert end == base + 16 + int.from_bytes(source[base + 12:base + 16], 'little')
        elif match['kind'] == 'lz77':
            start = int(match['start'], 16)
            data, size = lz77_decompress(source, start)
            assert size == match['compressed_bytes'] and len(data) == match['decoded_bytes']
            assert start <= site < start + size
            for ref in match['asset_pointers']:
                assert int.from_bytes(source[ref:ref + 4], 'little') == start + 0x08000000
        else:
            start, end = int(match['start'], 16), int(match['end_exclusive'], 16)
            assert start <= site < end
            if match['kind'] == 'compressed_wave':
                assert source[start:start + 16] == bytes.fromhex(match['header_hex'])
                assert source[start:start + 4] == b'\x01\x00\x00\x00'
                for ref in match['asset_pointers']:
                    assert int.from_bytes(source[ref:ref + 4], 'little') == start + 0x08000000
            else:
                assert int.from_bytes(source[match['asset_pointer']:match['asset_pointer'] + 4], 'little') == start + 0x08000000
                assert int.from_bytes(source[match['next_pointer']:match['next_pointer'] + 4], 'little') == end + 0x08000000
    # Le builder peut repointer ces faux matches ; le finaliseur les restaure.
    probe = bytearray(built)
    for match in evidence:
        site = int(match['site'], 16)
        probe[site:site + 4] = b'\x00\x00\x00\x08'
    make_patch(source).apply(probe)
    assert probe == built


def test_archaeologist_both_tenses_and_script_opcodes(source, built):
    for ref, raw in make_patch(source).context_entries():
        assert built[ref - 2:ref] == source[ref - 2:ref] == b'\x85\x00'
        target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
        assert built[target:target + len(raw)] == raw
    patch = make_patch(source)
    patch.definitions[150]['context_buffers'][0] = dict(
        patch.definitions[150]['context_buffers'][0], source_hex='00ff')
    probe = bytearray(built)
    with pytest.raises(ValueError, match='temps verbal'):
        patch.apply(probe)
    assert probe == built
