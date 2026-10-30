"""Finalise les seuls noms d'espèces PT-54 selon le glossaire F-759."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.fr.patches.species_names import apply_to_rom
from scripts.apply_combined_fr import _load_combined
from src.core.text_codec import TextEncoder


def apply_patches(rom: bytearray, source: bytes) -> int:
    """Valide atomiquement les lecteurs puis les 300 cellules indexées du lot."""
    audit = json.loads((ROOT / 'languages/pt/data/pt54_audit.json').read_text())
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    base = int(audit['table_base'], 16)
    pointer = (base + 0x08000000).to_bytes(4, 'little')
    for ref in audit['table_references']:
        if source[ref:ref + 4] != pointer or rom[ref:ref + 4] != pointer:
            raise ValueError(f'Lecteur PT-54 différent : {ref:#x}')
    selected = {}
    for row in audit['entries']:
        off = int(row['offset'], 16)
        cell = bytes.fromhex(row['source_hex'])
        name = texts[off]
        encoded = TextEncoder.encode_pokemon(name, strict=True)
        if (off != base + row['species_id'] * 11 or len(cell) != 11
                or source[off:off + 11] != cell or off + 11 > len(rom)
                or name != row['portuguese'] or not cell.startswith(encoded)):
            raise ValueError(f'Préimage ou nom canonique PT-54 différent : {off:#x}')
        selected[off] = name
    working = bytearray(rom)
    _, warnings = apply_to_rom(working, selected)
    if warnings:
        raise ValueError(str(warnings))
    # Conserver aussi le remplissage FF exact, sans changer les cellules voisines.
    for row in audit['entries']:
        off = int(row['offset'], 16)
        working[off:off + 11] = bytes.fromhex(row['source_hex'])
    rom[:] = working
    return len(selected)


def main() -> None:
    """Sauvegarde puis applique le contrat des noms fixes PT-54."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    count = apply_patches(rom, (ROOT / 'input/roms/englishrom.gba').read_bytes())
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-54 : {count} noms canoniques vérifiés')


if __name__ == '__main__':
    main()
