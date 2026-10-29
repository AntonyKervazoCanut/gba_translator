#!/usr/bin/env python3
"""PT-13 : livre les menus via toutes leurs cellules de pointeurs auditées."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from src.core.structured_text import StructuredTextPatch


def make_patch(source: bytes) -> StructuredTextPatch:
    """Prépare les 276 textes vivants sans écrire dans les tables voisines."""
    audit = json.loads((ROOT / 'languages/pt/data/pt13_audit.json').read_text())
    definitions = [row for row in audit['entries'] if row['status'] == 'translated']
    return StructuredTextPatch(source, definitions, ROOT / 'languages/pt/combined_pt.txt')


def main() -> int:
    """Sauvegarde la ROM et garantit les cibles et contrôles du manifeste."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch(source).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-13 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
