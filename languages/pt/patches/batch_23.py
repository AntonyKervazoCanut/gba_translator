#!/usr/bin/env python3
"""Finalise les pointeurs audités des zones Borrius du lot PT-23."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from src.core.structured_text import StructuredTextPatch


def make_patch(source: bytes) -> StructuredTextPatch:
    """Réutilise l'injecteur borné pour les seuls consommateurs PT-23."""
    audit = json.loads((ROOT / 'languages/pt/data/pt23_audit.json').read_text())
    return StructuredTextPatch(source, [r for r in audit['entries']
                                       if r['status'] == 'translated'],
                               ROOT / 'languages/pt/combined_pt.txt')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-23 : {stats}')
