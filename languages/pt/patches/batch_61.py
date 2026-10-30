"""Finalise les consommateurs PT-61 sans traiter les pixels comme du texte."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_29 import Batch29TextPatch


def make_patch(source: bytes) -> Batch29TextPatch:
    """Résout les clés commençant dans le bourrage vers leur consommateur réel."""
    audit = json.loads((ROOT / 'languages/pt/data/pt61_audit.json').read_text())
    definitions, aliases = [], {}
    for row in audit['entries']:
        if row['status'] == 'exception' or not row['references'] and 'consumer_offset' not in row:
            continue
        definition = dict(row)
        if 'consumer_offset' in row:
            offset = int(row['offset'], 16)
            consumer = int(row['consumer_offset'], 16)
            raw = bytes.fromhex(row['source_hex'])
            prefix = row['prefix_bytes']
            if consumer != offset + prefix or raw[:prefix] != bytes(prefix):
                raise ValueError('Préfixe de bourrage différent')
            if source[offset:offset + len(raw)] != raw:
                raise ValueError('Préimage de la clé avec bourrage différente')
            definition.update(offset=row['consumer_offset'], source_hex=raw[prefix:].hex(),
                              prefix_start=offset,
                              references=row['consumer_references'])
            aliases[consumer] = offset
        definitions.append(definition)
    patch = Batch29TextPatch(source, definitions, ROOT / 'languages/pt/combined_pt.txt')
    for consumer, key in aliases.items():
        patch.texts[consumer] = patch.texts[key]
    return patch


def main() -> int:
    """Sauvegarde et finalise les seuls pointeurs texte audités de PT-61."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-61 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
