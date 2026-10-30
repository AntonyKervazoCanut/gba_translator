"""PT-63 : finalise les dialogues, missions et menus aux pointeurs audités."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_20 import BorriusTextPatch


def make_patch(source: bytes) -> BorriusTextPatch:
    """Charge exclusivement les consommateurs texte prouvés du manifeste PT-63."""
    audit = json.loads((ROOT / 'languages/pt/data/pt63_audit.json').read_text())
    rows = [r for r in audit['entries'] if r['status'] != 'exception']
    return BorriusTextPatch(source, rows, ROOT / 'languages/pt/combined_pt.txt')


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
    print(f'PT-63 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
