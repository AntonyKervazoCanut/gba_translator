"""Finalise uniquement les catégories Pokédex indexées du lot PT-57."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts.apply_combined_fr import _load_combined
from src.core.text_codec import TextEncoder

TABLE_BASE = 0x1A357CC
STRIDE = 36
CELL_SIZE = 12


def apply_patches(rom: bytearray, source: bytes) -> int:
    """Valide les lecteurs et préimages avant les écritures atomiques bornées."""
    audit = json.loads((ROOT / 'languages/pt/data/pt57_audit.json').read_text())
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-57')
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    if [r['offset'] for r in audit['entries']] != manifest:
        raise ValueError('PT-57 : manifeste différent')
    pointer = (TABLE_BASE + 0x08000000).to_bytes(4, 'little')
    for ref in audit['table_references']:
        if source[ref:ref + 4] != pointer or rom[ref:ref + 4] != pointer:
            raise ValueError(f'PT-57 : lecteur différent à {ref:#x}')
    writes = {}
    for row in audit['entries']:
        if row['status'] == 'exception':
            continue
        offset = int(row['offset'], 16)
        cell = int(row['cell_offset'], 16)
        encoded = TextEncoder.encode_pokemon(texts[offset], strict=True)
        prefix = bytes.fromhex(row['prefix_hex'])
        if (cell != TABLE_BASE + row['dex_index'] * STRIDE
                or cell - offset != row['source_delta']
                or source[offset:cell] != prefix or rom[offset:cell] != prefix
                or source[cell:cell + CELL_SIZE].hex() != row['source_hex']
                or cell + CELL_SIZE > len(rom)
                or texts[offset] != row['portuguese'] or len(encoded) > CELL_SIZE):
            raise ValueError(f'PT-57 : cellule différente à {offset:#x}')
        final = encoded + bytes(CELL_SIZE - len(encoded))
        if final.hex() != row['final_hex']:
            raise ValueError(f'PT-57 : encodage différent à {offset:#x}')
        writes[cell] = final
    for cell, encoded in writes.items():
        rom[cell:cell + CELL_SIZE] = encoded
    return len(writes)


def main() -> None:
    """Sauvegarde puis finalise les 166 cellules de la ROM PT construite."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    count = apply_patches(rom, (ROOT / 'input/roms/englishrom.gba').read_bytes())
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-57 : {count} catégories Pokédex vérifiées')


if __name__ == '__main__':
    main()
