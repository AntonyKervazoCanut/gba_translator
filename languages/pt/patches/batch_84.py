"""PT-84 : finalise les formats et services de la Battle Frontier."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_63 import ScenarioTextPatch


class Batch84Patch(ScenarioTextPatch):
    """Préserve les instructions Thumb ressemblant à des pointeurs texte."""

    def __init__(self, source: bytes, definitions: list[dict], binary_regions: list[dict]):
        super().__init__(source, definitions, ROOT / 'languages/pt/combined_pt.txt')
        self.binary_regions = binary_regions
        for region in binary_regions:
            base, data = region['base'], bytes.fromhex(region['source_hex'])
            if source[base:base + len(data)] != data:
                raise ValueError('PT-84 : préimage Thumb différente')

    def apply(self, rom: bytearray) -> dict[str, int]:
        """Restaure les faux pointeurs avant une injection atomique bornée."""
        working = bytearray(rom)
        for region in self.binary_regions:
            site = region['site']
            working[site:site + 4] = self.source[site:site + 4]
        stats = super().apply(working)
        rom[:] = working
        return stats

    def verify(self, rom: bytes | bytearray) -> None:
        """Contrôle tous les consommateurs et les deux blocs de code exclus."""
        super().verify(rom)
        for region in self.binary_regions:
            base, data = region['base'], bytes.fromhex(region['source_hex'])
            if rom[base:base + len(data)] != data:
                raise ValueError('PT-84 : instructions Thumb modifiées')


def make_patch(source: bytes) -> Batch84Patch:
    """Charge les 290 textes vivants et exclut les dix clés mortes ou alias."""
    audit = json.loads((ROOT / 'languages/pt/data/pt84_audit.json').read_text())
    rows = [dict(row) for row in audit['entries'] if row['status'] != 'exception']
    regions = [region for row in audit['entries'] for region in row.get('binary_matches', [])]
    return Batch84Patch(source, rows, regions)


def main() -> int:
    """Sauvegarde puis injecte les seuls consommateurs du manifeste PT-84."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-84 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
