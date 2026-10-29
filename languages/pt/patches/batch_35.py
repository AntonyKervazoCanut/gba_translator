"""Livre les messages PT-35 et les cellules de types historiques à pas fixe."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_20 import BorriusTextPatch
from src.core.text_codec import TextEncoder


class Batch35TextPatch(BorriusTextPatch):
    """Finalise les pointeurs audités et les cellules de sept octets."""

    def __init__(self, source: bytes, rows: list[dict]):
        self.cells = [r for r in rows if 'cell_offset' in r]
        super().__init__(source, [r for r in rows if 'cell_offset' not in r],
                         ROOT / 'languages/pt/combined_pt.txt')

    def cell_entries(self) -> list[tuple[dict, int, bytes]]:
        """Valide les préimages et refuse toute troncature de nom canonique."""
        result = []
        for row in self.cells:
            offset, cell = int(row['offset'], 16), int(row['cell_offset'], 16)
            source = bytes.fromhex(row['source_hex'])
            if self.source[offset:offset + len(source)] != source:
                raise ValueError(f'{offset:#x}: préimage de type différente')
            if (cell - 0x961B50) % 7 or not 0x961B50 <= cell <= 0x961BF1:
                raise ValueError('Cellule de type hors table')
            for ref in row['table_references']:
                if int.from_bytes(self.source[ref:ref + 4], 'little') != 0x08961B50:
                    raise ValueError('Pointeur de table des types différent')
            raw = TextEncoder.encode_pokemon(self.texts[offset], strict=True)
            if len(raw) > 7:
                raise ValueError(f'{offset:#x}: cellule de type dépassée')
            result.append((row, cell, raw))
        return result

    def apply(self, rom: bytearray) -> dict[str, int]:
        """Écrit atomiquement les cellules, puis les seules références texte."""
        working = bytearray(rom)
        cells = self.cell_entries()
        for row, cell, _ in cells:
            offset = int(row['offset'], 16)
            # Des clés du manifeste commencent dans le bourrage de la cellule précédente.
            if offset < cell:
                working[offset:cell] = self.source[offset:cell]
        # Restaurer tous les préfixes avant d'écrire les cellules voisines :
        # un préfixe peut être le bourrage final d'un autre type traduit.
        for row, cell, raw in cells:
            working[cell:cell + 7] = raw.ljust(7, b'\xff')
            for ref in row['references']:
                working[ref:ref + 4] = (cell + 0x08000000).to_bytes(4, 'little')
        stats = super().apply(working)
        rom[:] = working
        return dict(stats, fixed_cells=len(self.cells))

    def verify(self, rom: bytes | bytearray) -> None:
        """Vérifie les cibles finales et chaque cellule indexée réellement utilisée."""
        super().verify(rom)
        for row, cell, raw in self.cell_entries():
            if rom[cell:cell + 7] != raw.ljust(7, b'\xff'):
                raise ValueError(f'{cell:#x}: texte de type non livré')
            for ref in row['references']:
                if int.from_bytes(rom[ref:ref + 4], 'little') != cell + 0x08000000:
                    raise ValueError('Référence directe de type non livrée')


def make_patch(source: bytes) -> Batch35TextPatch:
    """Charge les 163 entrées livrables, sans toucher aux 125 exceptions."""
    audit = json.loads((ROOT / 'languages/pt/data/pt35_audit.json').read_text())
    return Batch35TextPatch(source, [r for r in audit['entries'] if r['status'] != 'exception'])


def main() -> int:
    """Sauvegarde et finalise la ROM construite depuis le combined PT."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-35 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
