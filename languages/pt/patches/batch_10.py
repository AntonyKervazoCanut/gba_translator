#!/usr/bin/env python3
"""Finalise les messages de combat PT-10 par leurs pointeurs audités."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from src.core.structured_text import StructuredTextPatch


def make_patch(source: bytes) -> StructuredTextPatch:
    """Construit l'injecteur partagé à partir des seules cellules vivantes PT-10."""
    audit = json.loads((ROOT / 'languages/pt/data/pt10_audit.json').read_text())
    definitions = [row for row in audit['entries'] if row['status'] == 'translated']
    return StructuredTextPatch(source, definitions, ROOT / 'languages/pt/combined_pt.txt')


def main() -> int:
    """Sauvegarde le build et garantit les commandes et cibles du manifeste."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    original = args.rom.read_bytes()
    rom = bytearray(original)
    stats = make_patch(source).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(original)
    args.rom.write_bytes(rom)
    print(f'PT-10 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
