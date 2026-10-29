#!/usr/bin/env python3
"""B-1013 : 49 descriptions et 18 boîtes DE vérifiées, après les passes de réparation."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from src.core.structured_text import StructuredTextPatch


def main() -> int:
    """Sauvegarde puis injecte uniquement le lot documenté dans le manifeste."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    patch = StructuredTextPatch(
        (ROOT / 'input/roms/englishrom.gba').read_bytes(),
        json.loads((ROOT / 'languages/de/data/combat_ui_03_structure.json').read_text()),
        ROOT / 'languages/de/combined_de.txt',
    )
    original = args.rom.read_bytes()
    rom = bytearray(original)
    stats = patch.apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(original)
    args.rom.write_bytes(rom)
    print(f'Textes structurés DE : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
