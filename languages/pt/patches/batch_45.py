"""Finalise les 282 consommateurs texte vivants de PT-45 après les réparations."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_20 import BorriusTextPatch


def make_patch(source: bytes) -> BorriusTextPatch:
    """Exclut la fausse clé précédant le message de type et valide les consommateurs."""
    audit = json.loads((ROOT / 'languages/pt/data/pt45_audit.json').read_text())
    rows = [r for r in audit['entries'] if r['status'] != 'exception']
    return BorriusTextPatch(source, rows, ROOT / 'languages/pt/combined_pt.txt')


def main() -> int:
    """Sauvegarde et livre les textes aux seuls consommateurs audités de PT-45."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-45 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
