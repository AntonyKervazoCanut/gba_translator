"""PT-62 : livraison binaire, consommateurs, largeurs natives et exceptions."""
import hashlib
import re

import pytest

from languages.pt.patches.batch_62 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths
from tests.unit.pt.test_batch_pt62 import AUDIT, LIVE, ROOT

pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_exact_preimages_pointers_and_unused_drafts(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[off:off + len(raw)] == raw
        matches = [m.start() for m in re.finditer(
            re.escape((off + 0x08000000).to_bytes(4, 'little')), source)]
        excluded = [int(m['site'], 16) for m in row.get('non_text_matches', [])]
        assert matches == sorted(row['references'] + excluded)
        if row['status'] == 'exception':
            assert source[off - 16:off + 32] == bytes.fromhex(row['context_hex'])
            for neighbour in row['active_neighbours']:
                ref = int(neighbour['pointer'], 16)
                assert int.from_bytes(source[ref:ref + 4], 'little') == int(neighbour['offset'], 16) + 0x08000000
    # Marqueur explicite de brouillon, puis dialogues Win/Lose non référencés.
    assert 'Crim wants this once Aros is rescued' in AUDIT['entries'][223]['english_reference']


def test_all_live_consumers_after_build_and_unchanged_exceptions(source, built):
    patch = make_patch(source)
    assert len(patch.entries()) == 296
    patch.verify(built)
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            off = int(row['offset'], 16)
            raw = bytes.fromhex(row['source_hex'])
            assert built[off:off + len(raw)] == raw
    probe = bytearray(built)
    assert patch.apply(probe) == {'verified': 296, 'relocated': 0}
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
    assert patch.apply(rom)['verified'] == 296
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 296, 'relocated': 0}
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


def test_pcm_false_pointer_is_not_a_text_consumer(source, built):
    row = AUDIT['entries'][256]
    match = row['non_text_matches'][0]
    base, end = int(match['wave_base'], 16), int(match['sample_end'], 16)
    site, start = int(match['site'], 16), int(match['sample_start'], 16)
    assert row['references'] == [0x1E641C3]
    assert source[0x1E641BD:0x1E641C3] == bytes.fromhex('5c0e1d000000')
    assert int.from_bytes(source[0xCD7780:0xCD7784], 'little') == base + 0x08000000
    assert source[base:base + 16] == bytes.fromhex(match['wave_header_hex'])
    assert start == base + 16 and start < site < end
    assert end == start + int.from_bytes(source[base + 12:base + 16], 'little')
    assert built[site:site + 4] == source[site:site + 4]
    # Reproduit le repointage aveugle de ces quatre échantillons, puis sa réparation.
    probe = bytearray(built)
    probe[site:site + 4] = built[0x1E641C3:0x1E641C7]
    before = bytes(probe)
    assert make_patch(source).apply(probe) == {'verified': 296, 'relocated': 0}
    assert probe[:site] == before[:site] and probe[site + 4:] == before[site + 4:]
    assert probe[site:site + 4] == source[site:site + 4]
