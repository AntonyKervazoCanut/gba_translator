#!/usr/bin/env python3
"""F-761 : cellules PT-02 omises et message partagé restaurés après les réparations."""
from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.fr.patches.meteorite_dialogue import load_combined
from scripts.apply_inline_overrides_fr import (
    _extract_control_sequences_from_raw,
    _normalize_text,
)
from src.core.text_codec import TextEncoder
from src.core.text_reinserter import FreeSpaceAllocator

# Chaînes EN autonomes, sans pointeur absolu. Écriture bornée par leur FF.
INLINE = (
    0x19A650, 0x19BB53, 0x19BF8F, 0x19EABE, 0x1A1B8E, 0x1A231B,
    0x1A505B, 0x1A5103, 0x1A5133, 0x1A5160, 0x1A51A3, 0x1A51D0,
    0x1A5207, 0x1A5375, 0x1A5446, 0x1B1E07, 0x1BC590,
)
# loadpointer 0 (0F 00) + pointeur ; le second texte commence à l'intérieur
# du premier EN. Les deux corps doivent être indépendants après traduction.
SHARED = {0x1A51F6: (0x1A674A, 0x1A682F, 0x9A48DD), 0x1A5200: (0x1A6990,)}


def apply(rom: bytearray, source: bytes, texts: dict[int, str]) -> int:
    """Valide les budgets et les préimages, puis applique atomiquement le lot borné."""
    planned = []
    for offset in (*INLINE, *SHARED):
        encoded = TextEncoder.encode_pokemon(_normalize_text(texts[offset]), strict=True)
        end = source.index(b'\xff', offset) + 1
        def commands(raw: bytes) -> list[list[int]]:
            return [seq for seq in _extract_control_sequences_from_raw(raw)
                    if seq[0] not in (0xFA, 0xFE)]
        if commands(encoded) != commands(source[offset:end]):
            raise ValueError(f'{offset:#x}: commandes ou pages différentes')
        if offset in INLINE and len(encoded) > end - offset:
            raise ValueError(f'{offset:#x}: dépassement de cellule EN')
        for site in SHARED.get(offset, ()):
            if source[site - 2:site] != b'\x0f\x00' and source[site - 1] != 0x67:
                raise ValueError(f'{site:#x}: consommateur loadpointer/message absent')
            if struct.unpack_from('<I', source, site)[0] != offset + 0x08000000:
                raise ValueError(f'{site:#x}: pointeur EN inattendu')
        planned.append((offset, encoded))
    working = bytearray(rom)
    allocator = FreeSpaceAllocator(working)
    for offset, encoded in planned:
        if offset in INLINE:
            working[offset:offset + len(encoded)] = encoded
            continue
        sites = SHARED[offset]
        current = struct.unpack_from('<I', working, sites[0])[0] - 0x08000000
        if not 0 <= current < len(working):
            raise ValueError(f'{offset:#x}: cible vivante invalide')
        target = current if working[current:current + len(encoded)] == encoded else allocator.allocate(len(encoded))
        if target is None:
            raise ValueError('Espace libre insuffisant')
        working[target:target + len(encoded)] = encoded
        for site in sites:
            struct.pack_into('<I', working, site, target + 0x08000000)
    rom[:] = working
    return len(planned)


def main() -> int:
    """Patche uniquement la ROM PT dérivée après sauvegarde de son état précédent."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    original = args.rom.read_bytes()
    rom = bytearray(original)
    count = apply(rom, (ROOT / 'input/roms/englishrom.gba').read_bytes(),
                  load_combined(ROOT / 'languages/pt/combined_pt.txt'))
    Path(f'{args.rom}.bak').write_bytes(original)
    args.rom.write_bytes(rom)
    print(f'PT-02 : {count} cellules historiques vérifiées et injectées.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
