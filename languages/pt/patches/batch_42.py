"""Finalise le DexNav PT-42 et conserve ses cellules de mouvements vivantes."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_20 import BorriusTextPatch


class DexNavPatch(BorriusTextPatch):
    """Repointe les textes et vérifie les noms indexés sans toucher aux voisins."""

    def __init__(self, source: bytes):
        audit = json.loads((ROOT / 'languages/pt/data/pt42_audit.json').read_text())
        self.names = [r for r in audit['entries'] if r['kind'] == 'move_name']
        self.literals = [int(p, 16) for p in audit['move_table']['literals']]
        super().__init__(source, [r for r in audit['entries'] if r['references']],
                         ROOT / 'languages/pt/combined_pt.txt')

    def name_cells(self, rom: bytes | bytearray) -> list[tuple[int, bytes]]:
        """Résout la table vivante et valide les préimages des seules cellules du lot."""
        bases = {int.from_bytes(rom[p:p + 4], 'little') - 0x08000000 for p in self.literals}
        if len(bases) != 1:
            raise ValueError('PT-42 : pointeurs de table incohérents')
        base = bases.pop()
        if not 0 <= base <= len(rom) - 923 * 13 or rom[base:base + 2] != b'\xae\xff':
            raise ValueError('PT-42 : table de mouvements invalide')
        cells = []
        for row in self.names:
            offset = int(row['offset'], 16)
            cell = bytes.fromhex(row['source_cell_hex'])
            if self.source[offset:offset + 13] != cell:
                raise ValueError(f'{offset:#x}: préimage de cellule différente')
            if self.texts[offset] != row['expected']:
                raise ValueError(f'{offset:#x}: nom contraire au glossaire figé')
            cells.append((base + row['move_id'] * 13, cell))
        return cells

    def apply(self, rom: bytearray) -> dict[str, int]:
        """Finalise atomiquement noms fixes et textes aux pointeurs audités."""
        working = bytearray(rom)
        for offset, cell in self.name_cells(working):
            working[offset:offset + 13] = cell
        stats = super().apply(working)
        rom[:] = working
        return {**stats, 'fixed_verified': len(self.names)}

    def verify(self, rom: bytes | bytearray) -> None:
        """Vérifie les octets réellement consommés, y compris les cellules fixes."""
        super().verify(rom)
        for offset, cell in self.name_cells(rom):
            if rom[offset:offset + 13] != cell:
                raise ValueError(f'{offset:#x}: cellule vivante différente')


def make_patch(source: bytes) -> DexNavPatch:
    """Charge exclusivement les 281 entrées vivantes du lot PT-42."""
    return DexNavPatch(source)


def main() -> int:
    """Sauvegarde puis finalise la ROM PT construite."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    original = args.rom.read_bytes()
    rom = bytearray(original)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(original)
    args.rom.write_bytes(rom)
    print(f'PT-42 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
