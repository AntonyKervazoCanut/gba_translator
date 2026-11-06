"""PT-78 : pointeurs réels, cinq polices, PCM et écritures bornées."""
import hashlib
import re

import pytest

from languages.pt.patches.batch_78 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths
from tests.unit.pt.test_batch_pt78 import AUDIT, LIVE, ROOT, ROWS

pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_all_live_consumers_deliver_complete_text(source, built):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    patch = make_patch(source)
    assert len(patch.entries()) == 297
    patch.verify(built)
    for row in ROWS:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        refs = [m.start() for m in re.finditer(
            re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert refs == sorted(row['references'] + row['non_text_references'])
        for context in row.get('consumer_contexts', []):
            start = int(context['start'], 16)
            assert source[start:start + 16] == bytes.fromhex(context['hex'])


def test_five_fonts_with_real_runtime_expansions(built):
    for row in LIVE:
        expanded = row['portuguese'].replace(r'\n', '\n')
        for key, value in row['buffers'].items():
            expanded = expanded.replace(f'<0xFD><0x{int(key):02X}>', value)
        assert '<0xFD>' not in expanded
        raw = TextEncoder.encode_pokemon(expanded, strict=True)
        measured = [max(max(widths(seg, built, font.offsets(built)[1]))
                        for seg in re.split(b'[\xfa\xfb]', raw)) for font in LATIN_FONTS]
        assert measured == row['expanded_widths'], row['offset']
        assert max(measured) <= 192, row['offset']


def test_dead_reply_padding_and_three_pcm_samples(source, built):
    for row in ROWS:
        for pcm in row.get('pcm_matches', []):
            start = pcm['wave_base']
            end = start + 16 + pcm['stored_bytes']
            assert source[start:start + 16] == bytes.fromhex(pcm['header_hex'])
            assert source[start] == 0
            assert pcm['sample_count'] == pcm['stored_bytes']
            assert start + 16 <= pcm['site'] < end
            for ref in pcm['instrument_pointers']:
                assert int.from_bytes(source[ref:ref + 4], 'little') == start + 0x08000000
            assert built[start:end] == source[start:end]
    dead, padding = ROWS[23], ROWS[234]
    assert dead['references'] == padding['references'] == []
    for site, target in zip(dead['neighbor_sites'], dead['neighbor_targets']):
        assert int.from_bytes(source[site:site + 4], 'little') == int(target, 16) + 0x08000000
    offset = int(padding['offset'], 16)
    assert bytes.fromhex(padding['source_hex'])[0] == 0
    assert bytes.fromhex(padding['source_hex'])[1:] == bytes.fromhex(padding['owner_source_hex'])
    assert int(padding['owner_offset'], 16) == offset + 1
    for site in padding['owner_sites']:
        ref = int(site, 16)
        assert int.from_bytes(source[ref:ref + 4], 'little') == offset + 1 + 0x08000000
    # La routine du tampon conserve le s pluriel et le défilement FA natifs.
    assert source[0x1FB542C:0x1FB5430] == bytes.fromhex('e7fffaff')
    assert built[0x1FB542C:0x1FB5430] == source[0x1FB542C:0x1FB5430]


def test_patch_atomic_idempotent_and_bounded(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 297
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 297, 'relocated': 0}
    assert bytes(rom) == after
    allowed = set()
    for _, refs, raw in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(target, target + len(raw)))
    assert all(i in allowed for i, (a, b) in enumerate(zip(source, rom)) if a != b)
    patch.definitions[0] = dict(patch.definitions[0], source_hex='00ff')
    with pytest.raises(ValueError, match='préimage'):
        patch.apply(rom)
    assert bytes(rom) == after


def test_build_finalizer_is_idempotent(built, source):
    rom = bytearray(built)
    assert make_patch(source).apply(rom) == {'verified': 297, 'relocated': 0}
    assert rom == built
