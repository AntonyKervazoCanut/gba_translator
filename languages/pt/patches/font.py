#!/usr/bin/env python3
"""Compose ã õ Ã Õ dans les polices latines vivantes du moteur CFRU."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from src.core.font_glyphs import LATIN_FONTS, copy_accent_rows

# Cibles PT exclusives ; DE 0xF1–0xF6 et contrôles 0xF7–0xFF intacts.
TARGETS = ((0x60, 0xD5, 0x29), (0x61, 0xE3, 0x29),
           (0x62, 0xBB, 0x14), (0x63, 0xC9, 0x14))


def build_tilde(base: bytes, reference: bytes, uppercase: bool = False) -> bytes:
    """Copie le tilde de Ñ/ñ à la hauteur native de chaque police."""
    start = (2 if len(base) == 32 else 0) if uppercase else 6
    return copy_accent_rows(base, reference, start, start + 4)


def apply_patches(rom: bytearray) -> int:
    """Patche les cinq polices et copie les largeurs des lettres de base."""
    count = 0
    for spec in LATIN_FONTS:
        glyphs, widths = spec.offsets(rom)
        for target, base, reference in TARGETS:
            base_start = glyphs + base * spec.stride
            ref_start = glyphs + reference * spec.stride
            composed = build_tilde(
                bytes(rom[base_start:base_start + spec.stride]),
                bytes(rom[ref_start:ref_start + spec.stride]),
                reference == 0x14,
            )
            offset = glyphs + target * spec.stride
            if rom[offset:offset + spec.stride] != composed:
                rom[offset:offset + spec.stride] = composed
                count += 1
            rom[widths + target] = rom[widths + base]
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    original = args.rom.read_bytes()
    rom = bytearray(original)
    count = apply_patches(rom)
    Path(str(args.rom) + '.bak').write_bytes(original)
    args.rom.write_bytes(rom)
    print(f'{count} glyphes PT composés ; 20 largeurs synchronisées.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
