"""PT-56 : finalise les seuls noms d'espèces audités, sans toucher aux images."""
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
    """Valide les préimages/lecteurs avant une injection atomique bornée au lot."""
    audit = json.loads((ROOT / 'languages/pt/data/pt56_audit.json').read_text())
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    base = int(audit['table_base'], 16)
    for ref in audit['table_references']:
        pointer = (base + 0x08000000).to_bytes(4, 'little')
        if source[ref:ref + 4] != pointer or rom[ref:ref + 4] != pointer:
            raise ValueError(f'PT-56 : lecteur de table différent à {ref:#x}')
    selected = {}
    for row in audit['entries']:
        if row['status'] != 'retained_english':
            continue
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        text = texts[offset]
        encoded = TextEncoder.encode_pokemon(text, strict=True)
        if (offset != base + row['species_id'] * 11 or len(raw) != 11
                or source[offset:offset + 11] != raw or len(encoded) > 11
                or text != row['portuguese'] or not raw.startswith(encoded)):
            raise ValueError(f'PT-56 : préimage/nom canonique différent à {offset:#x}')
        selected[offset] = text
    working = bytearray(rom)
    _, warnings = apply_to_rom(working, selected)
    if warnings:
        raise ValueError('; '.join(warnings))
    for offset, text in selected.items():
        encoded = TextEncoder.encode_pokemon(text, strict=True)
        if working[offset:offset + len(encoded)] != encoded:
            raise ValueError(f'PT-56 : cellule non injectée à {offset:#x}')
    rom[:] = working
    return len(selected)


def main() -> None:
    """Sauvegarde puis vérifie les noms fixes après toutes les passes génériques."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    count = apply_patches(rom, source)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-56 : {count} noms fixes vérifiés')


if __name__ == '__main__':
    main()
