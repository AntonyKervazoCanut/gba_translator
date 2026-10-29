"""Écrit les seules cellules de classes PT-03, avec préimages vérifiées."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts.apply_combined_fr import _load_combined
from src.core.text_codec import TextEncoder

TABLE_BASE = 0x23E558
STRIDE = 13


def apply(rom: bytearray, source: bytes) -> int:
    """Valide toutes les cellules avant une écriture atomique et bornée."""
    if len(rom) != len(source):
        raise ValueError('Tailles ROM incompatibles')
    entries = json.loads((ROOT / 'languages/pt/data/pt03_audit.json').read_text())['entries']
    translations, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    writes = []
    for entry in entries:
        offset = int(entry['offset'], 16)
        if entry['status'] != 'translated' or 'cell_start' not in entry:
            continue
        if (offset - TABLE_BASE) % STRIDE:
            raise ValueError(f'Cellule non alignée : {offset:#x}')
        encoded = TextEncoder.encode_pokemon(translations[offset], strict=True)
        if len(encoded) > STRIDE:
            raise ValueError(f'Classe trop longue : {offset:#x}')
        original = source[offset:offset + STRIDE]
        expected = bytes.fromhex(entry['source_hex'])
        if not original.startswith(expected):
            raise ValueError(f'Préimage source incorrecte : {offset:#x}')
        target = encoded.ljust(STRIDE, b'\x00')
        current = bytes(rom[offset:offset + STRIDE])
        if current not in (original, target):
            raise ValueError(f'Cellule cible inattendue : {offset:#x}')
        if current != target:
            writes.append((offset, target))
    for offset, target in writes:
        rom[offset:offset + STRIDE] = target
    return len(writes)


def main() -> None:
    """Sauvegarde puis patche une ROM PT construite."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    original = args.rom.read_bytes()
    rom = bytearray(original)
    count = apply(rom, (ROOT / 'input/roms/englishrom.gba').read_bytes())
    if count:
        Path(f'{args.rom}.bak').write_bytes(original)
        args.rom.write_bytes(rom)
    print(f'Classes PT-03 : {count} cellules écrites')


if __name__ == '__main__':
    main()
