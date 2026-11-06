"""PT-78 : finalise Seaport City, Shadow Base et les panneaux de Borrius."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_63 import ScenarioTextPatch


def make_patch(source: bytes) -> ScenarioTextPatch:
    """Charge les seuls lecteurs prouvés ; exclut réplique morte, bourrage et PCM."""
    audit = json.loads((ROOT / 'languages/pt/data/pt78_audit.json').read_text())
    if hashlib.sha256(source).hexdigest() != audit['source_sha256']:
        raise ValueError('PT-78 : préimage ROM source différente')
    rows = [row for row in audit['entries'] if row['status'] != 'exception']
    return ScenarioTextPatch(source, rows, ROOT / 'languages/pt/combined_pt.txt')


def main() -> int:
    """Sauvegarde puis réinjecte verbatim aux seuls pointeurs audités du lot."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-78 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
