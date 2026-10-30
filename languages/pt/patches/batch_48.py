#!/usr/bin/env python3
"""PT-48 : injecte les 173 textes de descriptions et de zones aux pointeurs vivants."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_20 import BorriusTextPatch


def make_patch(source: bytes) -> BorriusTextPatch:
    """Charge les seuls consommateurs prouvés du manifeste PT-48."""
    rows = json.loads((ROOT / 'languages/pt/data/pt48_audit.json').read_text())['entries']
    return BorriusTextPatch(source, [dict(r) for r in rows if r['status'] != 'exception'],
                               ROOT / 'languages/pt/combined_pt.txt')


def main() -> int:
    """Sauvegarde puis injecte les textes et contrôle tous leurs consommateurs."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch(source).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-48 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
