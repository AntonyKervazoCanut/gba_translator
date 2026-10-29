"""Contrôle de la ROM PT finale, après toutes les étapes du build."""
from pathlib import Path

import pytest

from languages.pt.patches.font import TARGETS, build_tilde
from src.core.font_glyphs import LATIN_FONTS

pytestmark = pytest.mark.rom


def test_final_live_fonts():
    rom = (Path(__file__).parents[3] / 'output/roms/GenedRom-pt.gba').read_bytes()
    for spec in LATIN_FONTS:
        glyphs, widths = spec.offsets(rom)
        def tile(cp, glyphs=glyphs, stride=spec.stride):
            return rom[glyphs + cp * stride:glyphs + (cp + 1) * stride]
        rendered = set()
        for target, base, ref in TARGETS:
            assert tile(target) == build_tilde(tile(base), tile(ref), ref == 0x14)
            assert tile(target) != tile(base) and any(tile(target))
            assert rom[widths + target] == rom[widths + base] > 0
            rendered.add(tile(target))
        assert len(rendered) == 4
