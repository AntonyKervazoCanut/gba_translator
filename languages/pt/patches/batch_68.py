"""Finalise les 296 consommateurs PT-68 après les réparations génériques."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_20 import BorriusTextPatch

CALLBACK_BASE = 0x3E23E0
CALLBACK_BYTES = bytes.fromhex('9df20908a5f20908')
CALLBACK_OWNER = 0x9F294
FALSE_TEXT_SITE = 0x3E23E3


class MagnoliaTextPatch(BorriusTextPatch):
    """Préserve la table de callbacks que le scan brut confond avec un texte."""

    def __init__(self, source: bytes, definitions: list[dict], combined: Path) -> None:
        if (source[CALLBACK_BASE:CALLBACK_BASE + 8] != CALLBACK_BYTES
                or int.from_bytes(source[CALLBACK_OWNER:CALLBACK_OWNER + 4], 'little')
                != CALLBACK_BASE + 0x08000000):
            raise ValueError('PT-68 : préimage de la table de callbacks différente')
        super().__init__(source, definitions, combined)

    def apply(self, rom: bytearray) -> dict[str, int]:
        """Restaure les callbacks puis finalise les vrais lecteurs atomiquement."""
        working = bytearray(rom)
        # 08 A5 F2 09 chevauche 0809F29D et 0809F2A5 : ce n'est pas
        # un pointeur texte. Le builder générique peut déjà l'avoir repointé.
        working[CALLBACK_BASE:CALLBACK_BASE + 8] = CALLBACK_BYTES
        stats = super().apply(working)
        rom[:] = working
        return stats

    def verify(self, rom: bytes | bytearray) -> None:
        """Vérifie le texte livré et les deux fonctions natives de la table."""
        super().verify(rom)
        if rom[CALLBACK_BASE:CALLBACK_BASE + 8] != CALLBACK_BYTES:
            raise ValueError('PT-68 : référence non textuelle altérée')



def make_patch(source: bytes) -> MagnoliaTextPatch:
    """Charge les pointeurs de scripts et de tables audités, sans cellule brute."""
    audit = json.loads((ROOT / 'languages/pt/data/pt68_audit.json').read_text())
    return MagnoliaTextPatch(source, [r for r in audit['entries'] if r['status'] != 'exception'], ROOT / 'languages/pt/combined_pt.txt')


def main() -> int:
    """Sauvegarde puis livre les textes complets aux consommateurs vivants."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-68 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
