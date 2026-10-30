"""Finalise les consommateurs PT-47 et la table fixe des types CFRU."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_20 import BorriusTextPatch
from src.core.text_codec import TextEncoder


class Batch47Patch(BorriusTextPatch):
    """Conserve le pas de sept octets des lecteurs de types existants."""

    def __init__(self, source: bytes, rows: list[dict]):
        self.cells = [r for r in rows if 'cell_offset' in r]
        pointers = [dict(r, offset=r['live_offset']) for r in rows
                    if 'cell_offset' not in r]
        super().__init__(source, pointers, ROOT / 'languages/pt/combined_pt.txt')
        for row in rows:
            self.texts[int(row['live_offset'], 16)] = self.texts[int(row['offset'], 16)]

    def cell_entries(self) -> list[tuple[int, bytes]]:
        """Valide les cellules réelles, les lecteurs et les budgets fixes."""
        entries = []
        for row in self.cells:
            cell = int(row['cell_offset'], 16)
            if (cell - 0xA4EAD4) % 7 or not 0xA4EAD4 <= cell <= 0xA4EB75:
                raise ValueError('Cellule hors table PT-47')
            if self.source[cell:cell + 7] != bytes.fromhex(row['cell_hex']):
                raise ValueError(f'{cell:#x}: préimage différente')
            for ref in row['table_references']:
                if int.from_bytes(self.source[ref:ref + 4], 'little') != 0x08A4EAD4:
                    raise ValueError('Lecteur de types différent')
            raw = TextEncoder.encode_pokemon(self.texts[cell], strict=True)
            if len(raw) > 7:
                raise ValueError(f'{cell:#x}: cellule dépassée')
            entries.append((cell, raw.ljust(7, b'\xff')))
        return entries

    def apply(self, rom: bytearray) -> dict[str, int]:
        """Finalise atomiquement les textes et cellules, sans toucher aux voisins."""
        working = bytearray(rom)
        for cell, raw in self.cell_entries():
            working[cell:cell + 7] = raw
        stats = super().apply(working)
        rom[:] = working
        return dict(stats, fixed_cells=len(self.cells))

    def verify(self, rom: bytes | bytearray) -> None:
        """Vérifie les pointeurs relogés et les octets des cellules indexées."""
        super().verify(rom)
        for cell, raw in self.cell_entries():
            if rom[cell:cell + 7] != raw:
                raise ValueError(f'{cell:#x}: cellule non livrée')
        for row in self.cells:
            for ref in row['table_references']:
                if rom[ref:ref + 4] != self.source[ref:ref + 4]:
                    raise ValueError('Base de table modifiée')


def make_patch(source: bytes) -> Batch47Patch:
    """Charge seulement les 212 entrées dont le consommateur est établi."""
    audit = json.loads((ROOT / 'languages/pt/data/pt47_audit.json').read_text())
    return Batch47Patch(source, [r for r in audit['entries'] if r['status'] != 'exception'])


def main() -> int:
    """Sauvegarde puis finalise la ROM PT construite."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-47 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
