"""Finalise les 77 textes à pointeurs PT-43 après les passes génériques."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_20 import BorriusTextPatch


def make_patch(source: bytes) -> BorriusTextPatch:
    """Réutilise le repointage atomique et la validation des commandes binaires."""
    audit = json.loads((ROOT / 'languages/pt/data/pt43_audit.json').read_text())
    rows = [dict(r, offset=r['live_offset']) for r in audit['entries']
            if r['status'] == 'translated']
    patch = BorriusTextPatch(source, rows, ROOT / 'languages/pt/combined_pt.txt')
    # Les clés restent celles du manifeste, même lorsque celui-ci inclut un padding.
    for row in audit['entries']:
        if row['status'] == 'translated':
            patch.texts[int(row['live_offset'], 16)] = patch.texts[int(row['offset'], 16)]
    return patch


def main() -> int:
    """Sauvegarde puis finalise les consommateurs de combat et de descriptions."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    original = args.rom.read_bytes()
    rom = bytearray(original)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(original)
    args.rom.write_bytes(rom)
    print(f'PT-43 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
