"""Finalise les seuls consommateurs texte vivants du lot PT-71."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_29 import Batch29TextPatch


def make_patch(source: bytes) -> Batch29TextPatch:
    """Charge exclusivement les consommateurs texte prouvés du manifeste PT-71."""
    audit = json.loads((ROOT / 'languages/pt/data/pt71_audit.json').read_text())
    rows = [r for r in audit['entries'] if r['status'] != 'exception']
    return Batch29TextPatch(source, rows, ROOT / 'languages/pt/combined_pt.txt')


def main() -> int:
    """Sauvegarde puis finalise les pointeurs de la ROM PT construite."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    original = args.rom.read_bytes()
    rom = bytearray(original)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(original)
    args.rom.write_bytes(rom)
    print(f'PT-71 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
