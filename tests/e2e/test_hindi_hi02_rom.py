"""HI-02 : consommateurs réels, atomicité et cellules voisines sur ROM EN."""
from pathlib import Path

import pytest

from languages.indie.patches.batch_02 import make_patch

ROOT = Path(__file__).resolve().parents[2]
pytestmark = pytest.mark.rom


def test_real_rom_patch_is_atomic_bounded_and_idempotent():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    patch = make_patch(source)
    working = bytearray(source)

    patch.apply(working)
    once = bytes(working)
    patch.apply(working)

    assert working == once
    patch.verify(working)
    for site in (0x10C2A7, 0x10C333, 0x133F573, 0x1FC5A9F):
        assert working[site:site + 4] == source[site:site + 4]
    changed_cells = {int(r['offset'], 16) for r in patch.rows if 'cell_start' in r}
    for offset in range(0x23E558, 0x23E642, 13):
        if offset not in changed_cells:
            assert working[offset:offset + 13] == source[offset:offset + 13]
    # Les polices sont des faux textes exclus ; aucun rendu de glyphe n'est patché ici.
    assert working[0x1EAF00:0x230000] == source[0x1EAF00:0x230000]
    patch.texts[0x1A532F] = patch.texts[0x1A532F].replace(r'\n', ' ')
    with pytest.raises(ValueError, match='contrôles ou sauts'):
        patch.apply(working)
    assert working == once


def test_built_rom_delivers_every_hi02_translation():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-indie.gba').read_bytes()
    patch = make_patch(source)

    patch.verify(built)

    assert len(patch.checked()) == 280
    assert len(patch.entries()) == 271


def test_changed_preimage_is_rejected():
    source = bytearray((ROOT / 'input/roms/englishrom.gba').read_bytes())
    source[0x1A532F] ^= 1

    with pytest.raises(ValueError, match='ROM EN différente'):
        make_patch(source)
