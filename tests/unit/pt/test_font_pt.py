"""Composition des tildes et conservation des glyphes hors PT."""
from pathlib import Path

import pytest

from languages.pt.patches.font import TARGETS, apply_patches, build_tilde
from src.core.font_glyphs import LATIN_FONTS


def test_tilde_keeps_body_and_uses_reference_accent():
    # Format moteur : 8x16, deux octets par rangée ; base sans accent.
    base = bytes.fromhex('0000' * 6 + '8055' * 6 + '0000' * 4)
    reference = bytes.fromhex('0000' * 3 + '80d9c066' + '0000' * 11)
    result = build_tilde(base, reference)
    assert result[:6] == base[:6]
    assert result[6:10] == reference[6:10]
    assert result[10:] == base[10:]
    assert result != base



@pytest.mark.parametrize('relocated', [False, True])
def test_real_fonts_slots_widths_and_live_pointers(relocated):
    # Vrais blocs EN ; les copies mortes restent intactes après relocalisation.
    rom = bytearray(0x50000)
    allowed = set()
    for i, spec in enumerate(LATIN_FONTS):
        fixture = (Path(__file__).parents[1] / 'fixtures/pt_fonts' / f'latin_{i}.bin').read_bytes()
        old = 0x8000 + i * 0x5000
        live = old + 0x20000 if relocated else old
        rom[old:old + len(fixture)] = fixture
        rom[live:live + len(fixture)] = fixture
        width = live + spec.stride * 256
        for pointer, offset in ((spec.glyph_pointer, live), (spec.width_pointer, width)):
            rom[pointer:pointer + 4] = (0x08000000 + offset).to_bytes(4, 'little')
        for target, _, _ in TARGETS:
            allowed.update(range(live + target * spec.stride, live + (target + 1) * spec.stride))
            allowed.add(width + target)
    before = bytes(rom)

    assert apply_patches(rom) == 20

    assert {i for i, (a, b) in enumerate(zip(before, rom)) if a != b} <= allowed
    for spec in LATIN_FONTS:
        glyphs, widths = spec.offsets(rom)
        shapes = set()
        for target, base, ref in TARGETS:
            start = glyphs + target * spec.stride
            tile = bytes(rom[start:start + spec.stride])
            base_tile = bytes(rom[glyphs + base * spec.stride:glyphs + (base + 1) * spec.stride])
            assert tile != base_tile and any(tile)
            assert rom[widths + target] == rom[widths + base] > 0
            accent_start = (2 if spec.stride == 32 else 0) if ref == 0x14 else 6
            assert tile[:accent_start] == base_tile[:accent_start]
            assert tile[accent_start + 4:] == base_tile[accent_start + 4:]
            shapes.add(tile)
        assert len(shapes) == 4
    patched = bytes(rom)
    assert apply_patches(rom) == 0
    assert bytes(rom) == patched


def test_allocated_slots_were_empty_in_all_source_fonts():
    for i, spec in enumerate(LATIN_FONTS):
        font = (Path(__file__).parents[1] / 'fixtures/pt_fonts' / f'latin_{i}.bin').read_bytes()
        for target, _, _ in TARGETS:
            tile = font[target * spec.stride:(target + 1) * spec.stride]
            # Valeurs 0 et 3 : colonnes inutilisées ou fond opaque, aucune encre/ombre.
            assert all((byte >> shift) & 3 in (0, 3) for byte in tile for shift in (0, 2, 4, 6))


def test_invalid_live_pointer_fails_before_writing():
    rom = bytearray(0x8000)
    before = bytes(rom)
    with pytest.raises(ValueError, match='Pointeur'):
        apply_patches(rom)
    assert bytes(rom) == before
