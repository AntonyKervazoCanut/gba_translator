"""Finalise les descriptions, catégories et cellules d'espèces du seul lot PT-52."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_20 import BorriusTextPatch
from src.core.text_codec import TextEncoder


class Batch52Patch(BorriusTextPatch):
    """Conserve les noms anglais canoniques dans les cellules indexées de 11 octets."""

    def __init__(self, source: bytes, audit: dict):
        self.audit = audit
        self.cells = [r for r in audit['entries'] if r['kind'] == 'species']
        super().__init__(source, [r for r in audit['entries'] if r['kind'] != 'species'],
                         ROOT / 'languages/pt/combined_pt.txt')

    def cell_entries(self, rom: bytes | bytearray) -> list[tuple[int, bytes]]:
        """Valide tous les lecteurs et préimages avant toute écriture fixe."""
        for table in self.audit['indirect_tables']:
            ref = int(table['reader'], 16)
            pointer = (int(table['base'], 16) + 0x08000000).to_bytes(4, 'little')
            start = int(table['code_offset'], 16)
            code = bytes.fromhex(table['code_hex'])
            if (self.source[ref:ref + 4] != pointer or rom[ref:ref + 4] != pointer
                    or self.source[start:start + len(code)] != code
                    or rom[start:start + len(code)] != code):
                raise ValueError(f'{ref:#x}: lecteur Pokédex différent')
        for row in self.definitions:
            for consumer in row.get('indirect_consumers', []):
                site = int(consumer['site'], 16)
                species = consumer['species_id'].to_bytes(2, 'little')
                if self.source[site - 4:site - 2] != species or rom[site - 4:site - 2] != species:
                    raise ValueError(f'{site:#x}: espèce Pokédex différente')
        base = int(self.audit['species_table_base'], 16)
        for ref in self.audit['species_table_references']:
            pointer = (base + 0x08000000).to_bytes(4, 'little')
            if self.source[ref:ref + 4] != pointer or rom[ref:ref + 4] != pointer:
                raise ValueError(f'{ref:#x}: lecteur d’espèces différent')
        entries = []
        for row in self.cells:
            offset = int(row['offset'], 16)
            cell = bytes.fromhex(row['cell_hex'])
            raw = TextEncoder.encode_pokemon(self.texts[offset], strict=True)
            if (offset != base + row['species_id'] * 11 or len(cell) != 11
                    or self.source[offset:offset + 11] != cell
                    or self.texts[offset] != row['english_rom']
                    or len(raw) > 11 or cell[:len(raw)] != raw):
                raise ValueError(f'{offset:#x}: cellule canonique différente')
            entries.append((offset, cell))
        return entries

    def apply(self, rom: bytearray) -> dict[str, int]:
        """Finalise atomiquement les consommateurs, puis vérifie chaque cible."""
        cells = self.cell_entries(rom)
        working = bytearray(rom)
        for offset, raw in cells:
            working[offset:offset + 11] = raw
        stats = super().apply(working)
        rom[:] = working
        return dict(stats, fixed_cells=len(cells))

    def verify(self, rom: bytes | bytearray) -> None:
        """Vérifie les références relocalisées et les cellules réellement lues."""
        super().verify(rom)
        for offset, raw in self.cell_entries(rom):
            if rom[offset:offset + 11] != raw:
                raise ValueError(f'{offset:#x}: cellule non livrée')


def make_patch(source: bytes) -> Batch52Patch:
    """Charge exclusivement le manifeste audité de PT-52."""
    audit = json.loads((ROOT / 'languages/pt/data/pt52_audit.json').read_text())
    return Batch52Patch(source, audit)


def main() -> None:
    """Sauvegarde et finalise la ROM construite sans modifier les voisins."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch(source).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-52 : {stats}')


if __name__ == '__main__':
    main()
