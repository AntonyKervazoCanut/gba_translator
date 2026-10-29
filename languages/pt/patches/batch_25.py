"""Finalise les 272 consommateurs texte vivants du lot PT-25."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_20 import BorriusTextPatch


def make_patch(source: bytes) -> BorriusTextPatch:
    """Réutilise l'injection bornée, les contrôles et budgets Borrius."""
    audit = json.loads((ROOT / 'languages/pt/data/pt25_audit.json').read_text())
    rows = [row for row in audit['entries'] if row['status'] == 'translated']
    return BorriusTextPatch(source, rows, ROOT / 'languages/pt/combined_pt.txt')


def main() -> int:
    """Sauvegarde et repointe les textes après les passes génériques."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    original = args.rom.read_bytes()
    rom = bytearray(original)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(original)
    args.rom.write_bytes(rom)
    print(f'PT-25 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
