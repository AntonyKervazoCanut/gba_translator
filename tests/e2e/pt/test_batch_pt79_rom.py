"""PT-79 : pointeurs vivants, octets complets, fenêtres et écritures bornées."""
import re

import pytest

from languages.pt.patches.batch_79 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths
from tests.unit.pt.test_batch_pt79 import ROOT, audit

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
    assert len(patch.entries()) == 299
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        matches = [m.start() for m in re.finditer(
            re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert sorted(matches) == sorted(row['references'] + row['non_text_references'])
        if row['status'] == 'exception':
            for target in range(offset, offset + len(raw)):
                assert (target + 0x08000000).to_bytes(4, 'little') not in source
            assert built[offset:offset + len(raw)] == raw
            for site, target in zip(row['neighbor_sites'], row['neighbor_targets']):
                assert int.from_bytes(source[site:site + 4], 'little') == int(target, 16) + 0x08000000
            continue
        encoded = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        for ref in row['references']:
            target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
            assert built[target:target + len(encoded)] == encoded


def test_real_fonts_with_expanded_runtime_buffers(built):
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            continue
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        buffers = {(0xFD, int(k)): v for k, v in row['buffers'].items()}
        measured = [max(max(widths(seg, built, font.offsets(built)[1], buffers))
                        for seg in re.split(b'[\xfa\xfb]', raw)) for font in LATIN_FONTS]
        assert measured == row['expanded_widths'], row['offset']
        relevant = measured[:1] if 225 <= row['index'] <= 231 else measured
        assert max(relevant) <= row['pixel_budget'], row['offset']


def test_scanner_native_window_templates_are_preserved(source, built):
    # Font0, x4, fenêtre1 de 27 tuiles : 216 - 4 = 212 pixels.
    assert source[0x1FB6BD4:0x1FB6BDC].hex() == '0100121b020f0100'
    # Catégorie : fenêtre14 de 15 tuiles ; libellé <=60 pour laisser le niveau à droite.
    assert source[0x1FB6C3C:0x1FB6C44].hex() == '0220050f03008202'
    assert built[0x1FB6BCC:0x1FB6C44] == source[0x1FB6BCC:0x1FB6C44]


def test_patch_atomic_idempotent_and_strictly_bounded(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 299
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 299, 'relocated': 0}
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
