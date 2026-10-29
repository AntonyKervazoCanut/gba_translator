"""Primitives des polices latines 2bpp du moteur FireRed/CFRU.

Les adresses désignent les littéraux du code, pas les blocs de données :
une police relocalisée reste accessible par son pointeur vivant.
"""
from dataclasses import dataclass

ROM_BASE = 0x08000000


@dataclass(frozen=True)
class LatinFont:
    """Décrit une police brute utilisée par le moteur de texte."""

    glyph_pointer: int
    width_pointer: int
    stride: int

    def offsets(self, rom: bytes) -> tuple[int, int]:
        """Résout et valide les deux tables vivantes dans la ROM."""
        offsets = []
        for pointer, size in ((self.glyph_pointer, self.stride * 256),
                              (self.width_pointer, 256)):
            offset = int.from_bytes(rom[pointer:pointer + 4], 'little') - ROM_BASE
            if not 0 <= offset <= len(rom) - size:
                raise ValueError(f'Pointeur de police invalide : 0x{pointer:X}')
            offsets.append(offset)
        return tuple(offsets)


# Littéraux des routines de décompression des polices 0, 1, 2, 4 et 5.
LATIN_FONTS = (
    LatinFont(0x64C4, 0x64CC, 32),
    LatinFont(0x658C, 0x6594, 64),
    LatinFont(0x66EC, 0x66F4, 64),
    LatinFont(0x6920, 0x6928, 64),
    LatinFont(0x6A8C, 0x6A94, 64),
)


def copy_accent_rows(base: bytes, reference: bytes, start: int, end: int) -> bytes:
    """Compose les rangées d'accent sans déplacer ni tronquer la lettre."""
    if len(base) != len(reference) or len(base) not in (32, 64):
        raise ValueError('Les glyphes doivent avoir le même format 2bpp')
    if not 0 <= start < end <= 16 or start % 2 or end % 2:
        raise ValueError('Rangées 2bpp invalides')
    return base[:start] + reference[start:end] + base[end:]
