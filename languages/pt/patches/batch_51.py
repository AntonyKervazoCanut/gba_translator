"""Finalise les 300 descriptions Pokédex de PT-51 aux pointeurs vivants."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from src.core.structured_text import StructuredTextPatch


def make_patch(source: bytes) -> StructuredTextPatch:
    """Charge les seules descriptions du manifeste PT-51 et leurs préimages."""
    audit = json.loads((ROOT / 'languages/pt/data/pt51_audit.json').read_text())
    return StructuredTextPatch(source, audit['entries'], ROOT / 'languages/pt/combined_pt.txt')


def main() -> int:
    """Sauvegarde puis injecte les textes, sans écraser les cellules voisines."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    original = args.rom.read_bytes()
    rom = bytearray(original)
    stats = make_patch(source).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(original)
    args.rom.write_bytes(rom)
    print(f'PT-51 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
