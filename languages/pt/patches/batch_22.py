"""Finalise les consommateurs audités du lot PT-22 après les passes génériques."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from src.core.structured_text import StructuredTextPatch


def make_patch(source: bytes) -> StructuredTextPatch:
    """Charge les seules chaînes référencées, y compris les noms conservés."""
    audit = json.loads((ROOT / 'languages/pt/data/pt22_audit.json').read_text())
    definitions = [row for row in audit['entries'] if row['status'] != 'exception']
    return StructuredTextPatch(source, definitions, ROOT / 'languages/pt/combined_pt.txt')


def main() -> int:
    """Sauvegarde puis injecte atomiquement les textes aux pointeurs vivants."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    original = args.rom.read_bytes()
    rom = bytearray(original)
    stats = make_patch(source).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(original)
    args.rom.write_bytes(rom)
    print(f'PT-22 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
