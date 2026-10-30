"""Livre les dialogues PT-59 complets via leurs consommateurs vivants."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_29 import Batch29TextPatch


def make_patch(source: bytes) -> Batch29TextPatch:
    """Exclut les deux textes sans lecteur identifié et protège les commandes."""
    audit = json.loads((ROOT / 'languages/pt/data/pt59_audit.json').read_text())
    rows = [row for row in audit['entries'] if row['status'] != 'exception']
    return Batch29TextPatch(source, rows, ROOT / 'languages/pt/combined_pt.txt')


def main() -> int:
    """Finalise après les réparations génériques, avec sauvegarde obligatoire."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-59 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
