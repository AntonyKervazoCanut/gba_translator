#!/usr/bin/env python3
"""PT-49 : injecte les 210 descriptions d’objets et de mouvements aux pointeurs vivants."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from src.core.structured_text import StructuredTextPatch


def make_patch(source: bytes) -> StructuredTextPatch:
    """Charge les seuls consommateurs prouvés du manifeste PT-49."""
    rows = json.loads((ROOT / 'languages/pt/data/pt49_audit.json').read_text())['entries']
    rows = [r for r in rows if r['status'] == 'translated']
    for row in rows:
        for item, ref in zip(row.get('item_ids', []), row['references']):
            if ref != 0x876074 + item * 44 + 20:
                raise ValueError('Table des descriptions PT-49 différente')
    return StructuredTextPatch(source, [dict(r) for r in rows if r['status'] == 'translated'],
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
    print(f'PT-49 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
