"""PT-18 : finalise les menus sans fil et les descriptions aux cellules vivantes."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from src.core.structured_text import StructuredTextPatch


def make_patch(source: bytes) -> StructuredTextPatch:
    """Relie les clés du manifeste aux débuts réels, en ignorant les doublons morts."""
    audit = json.loads((ROOT / 'languages/pt/data/pt18_audit.json').read_text())
    delivered = [r for r in audit['entries'] if r['status'] in ('translated', 'retained')]
    definitions = []
    for row in delivered:
        definition = dict(row)
        definition['offset'] = row['target']
        if row['target'] != row['offset']:
            definition['source_hex'] = row['replacement']['source_hex']
        definitions.append(definition)
    patch = StructuredTextPatch(source, definitions, ROOT / 'languages/pt/combined_pt.txt')
    # Seules les clés du combined appartenant à PT-18 sont lues. Un offset
    # de remplissage n'est jamais injecté en place dans le texte voisin.
    for row in delivered:
        patch.texts[int(row['target'], 16)] = patch.texts[int(row['offset'], 16)]
    return patch


def main() -> int:
    """Valide, sauvegarde puis injecte atomiquement le lot audité."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    original = args.rom.read_bytes()
    rom = bytearray(original)
    stats = make_patch(source).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(original)
    args.rom.write_bytes(rom)
    print(f'PT-18 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
