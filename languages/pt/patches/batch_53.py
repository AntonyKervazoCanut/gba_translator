"""Finalise les seules cellules fixes d’espèces du manifeste PT-53."""
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
    """Valide toutes les préimages et références avant toute écriture bornée."""
    audit = json.loads((ROOT / 'languages/pt/data/pt53_audit.json').read_text())
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-53')
    if [row['offset'] for row in audit['entries']] != manifest:
        raise ValueError('Couverture PT-53 différente du manifeste')
    base = int(audit['table_base'], 16)
    for ref in audit['table_references']:
        pointer = (base + 0x08000000).to_bytes(4, 'little')
        if source[ref:ref + 4] != pointer or rom[ref:ref + 4] != pointer:
            raise ValueError(f'Lecteur d’espèces PT-53 différent : {ref:#x}')
    writes = {}
    for row in audit['entries']:
        offset = int(row['offset'], 16)
        before = bytes.fromhex(row['source_hex'])
        after = bytes.fromhex(row['final_hex'])
        encoded = TextEncoder.encode_pokemon(texts[offset], strict=True)
        if (offset != base + row['species_id'] * 11
                or len(before) != 11 or len(after) != 11
                or source[offset:offset + 11] != before
                or offset + 11 > len(rom)
                or texts[offset] != row['portuguese']
                or len(encoded) > 11 or not after.startswith(encoded)):
            raise ValueError(f'Cellule PT-53 différente : {offset:#x}')
        writes[offset] = after
    for offset, cell in writes.items():
        rom[offset:offset + 11] = cell
    return len(writes)


def main() -> None:
    """Sauvegarde la ROM et injecte les 300 cellules sans relocalisation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    count = apply_patches(rom, source)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-53 : {count} cellules d’espèces vérifiées')


if __name__ == '__main__':
    main()
