"""PT-83 : lecteurs vivants, audio, alias et budgets des polices réelles."""
import re

import pytest

from languages.pt.patches.batch_83 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths
from tests.unit.pt.test_batch_pt83 import ROOT, audit

pytestmark = pytest.mark.rom
AUDIT = audit()


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_every_live_consumer_delivers_complete_portuguese(source, built):
    patch = make_patch(source)
    patch.verify(built)
    assert len(patch.entries()) == 292
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        matches = [m.start() for m in re.finditer(
            re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert sorted(matches) == sorted(row['references'] + row['non_text_references'])
        for site in row['non_text_references']:
            assert built[site:site + 4] == source[site:site + 4]
        if row['status'] == 'exception':
            continue
        encoded = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        for ref in row.get('consumer_references', row['references']):
            target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
            assert built[target:target + len(encoded)] == encoded
        if 'consumer_offset' in row:
            end = int(row['consumer_offset'], 16)
            assert built[offset:end] == source[offset:end]


def test_exceptions_and_audio_matches_have_binary_evidence(source):
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        for pcm in row.get('pcm_matches', []):
            base, site = pcm['wave_base'], pcm['site']
            assert source[base:base + 16].hex() == pcm['header_hex']
            ref = pcm['instrument_pointer']
            assert int.from_bytes(source[ref:ref + 4], 'little') == base + 0x08000000
            assert base + 16 <= site <= base + 12 + int.from_bytes(source[base + 12:base + 16], 'little')
        for binary in row.get('binary_matches', []):
            base = binary['base']
            raw = bytes.fromhex(binary['source_hex'])
            assert source[base:base + len(raw)] == raw
            assert base <= binary['site'] <= base + len(raw) - 4
        if row['status'] != 'exception':
            continue
        assert not row['references']
        if 'alias_offset' in row:
            target = int(row['alias_offset'], 16)
            assert source[offset:target].hex() == row['prefix_hex']
            for site in row['alias_references']:
                assert int.from_bytes(source[site:site + 4], 'little') == target + 0x08000000
        elif 'parent_offset' in row:
            parent = next(r for r in AUDIT['entries'] if r['offset'] == row['parent_offset'])
            assert int(parent['offset'], 16) < offset < int(parent['offset'], 16) + len(bytes.fromhex(parent['source_hex']))
            assert parent['status'] == 'translated'
        else:
            excluded = row['interior_non_text_references']
            for match in excluded:
                base, raw = match['base'], bytes.fromhex(match['source_hex'])
                assert source[base:base + len(raw)] == raw
            for target in range(offset, offset + len(bytes.fromhex(row['source_hex']))):
                matches = [m.start() for m in re.finditer(re.escape(
                    (target + 0x08000000).to_bytes(4, 'little')), source)]
                assert matches == [m['site'] for m in excluded if int(m['target'], 16) == target]
            for site, target in zip(row['neighbor_sites'], row['neighbor_targets']):
                assert int.from_bytes(source[site:site + 4], 'little') == int(target, 16) + 0x08000000


def test_real_fonts_with_runtime_buffers(built):
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            continue
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        buffers = {(0xFD, int(k)): v for k, v in row['buffers'].items()}
        measured = [max(max(widths(seg, built, font.offsets(built)[1], buffers))
                        for seg in re.split(b'[\xfa\xfb]', raw)) for font in LATIN_FONTS]
        assert measured == row['expanded_widths'], row['offset']
        assert max(measured) <= row['pixel_budget'], row['offset']


def test_patch_atomic_idempotent_and_strictly_bounded(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 292
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 292, 'relocated': 0}
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
