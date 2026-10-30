"""Finalise les seules cellules de noms d'espèces du manifeste PT-55."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts.apply_combined_fr import _load_combined
from src.core.text_codec import TextEncoder


def apply_patches(rom: bytearray, source: bytes) -> int:
    """Valide les lecteurs et préimages puis restaure les 299 cellules fixes."""
    audit = json.loads((ROOT / 'languages/pt/data/pt55_audit.json').read_text())
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    base = int(audit['table_base'], 16)
    pointer = (base + 0x08000000).to_bytes(4, 'little')
    for ref in audit['table_references']:
        if source[ref:ref + 4] != pointer or rom[ref:ref + 4] != pointer:
            raise ValueError(f'Lecteur de noms PT-55 différent : {ref:#x}')
    writes = {}
    for row in audit['entries']:
        offset = int(row['offset'], 16)
        cell = bytes.fromhex(row['source_hex'])
        encoded = TextEncoder.encode_pokemon(texts[offset], strict=True)
        if (offset != base + row['species_id'] * 11 or len(cell) != 11
                or source[offset:offset + 11] != cell
                or texts[offset] != row['english'] or len(encoded) > 11
                or cell[:len(encoded)] != encoded or offset + 11 > len(rom)):
            raise ValueError(f'Cellule canonique PT-55 différente : {offset:#x}')
        writes[offset] = cell
    for offset, cell in writes.items():
        rom[offset:offset + 11] = cell
    return len(writes)


def main() -> None:
    """Sauvegarde puis finalise la table après les passes génériques."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    count = apply_patches(rom, source)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-55 : {count} noms canoniques vérifiés')


if __name__ == '__main__':
    main()
