#!/usr/bin/env python3
"""Injecte les cellules fixes PT-04 sans déplacer leurs adresses indexées.

Les offsets du corpus commencent parfois dans le padding du nom précédent.
Restaurer d’abord ces préfixes, puis écrire toutes les cellules évite de mutiler
Incêndio lors du traitement de l’alias suivant de Dilúvio. Aucune autre cellule
ni aucun pointeur n’est traduit par ce patch.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from src.core.text_codec import TextEncoder


def apply(rom: bytearray, source: bytes) -> int:
    """Écrit les cellules autorisées, avec préimages et budgets vérifiés."""
    audit = json.loads((ROOT / 'languages/pt/data/pt04_audit.json').read_text())
    fixed = [e for e in audit['entries'] if e.get('delivery') == 'fixed_cell']
    translations = {}
    for line in (ROOT / 'languages/pt/combined_pt.txt').read_text().splitlines():
        match = re.match(r'0x([\da-fA-F]+):\s?(.*)', line)
        if match:
            translations[int(match[1], 16)] = match[2].replace('\\n', '\n')
    candidate = bytearray(rom)
    targets = []
    for entry in fixed:
        start = int(entry['offset'], 16)
        cell = int(entry['cell_offset'], 16)
        size = entry['cell_bytes']
        expected = bytes.fromhex(entry['source_cell_hex'])
        if source[cell:cell + size] != expected:
            raise ValueError(f'préimage PT-04 invalide à {cell:#x}')
        encoded = TextEncoder.encode_pokemon(translations[start].lstrip(), strict=True)
        encoded = encoded[entry.get('prefix_bytes', 0):]
        if len(encoded) > size:
            raise ValueError(f'cellule PT-04 trop longue à {cell:#x}')
        if not 0 <= start <= cell < cell + size <= len(rom) or len(rom) != len(source):
            raise ValueError(f'cellule PT-04 hors ROM à {cell:#x}')
        candidate[start:cell + size] = source[start:cell + size]
        targets.append((cell, encoded.ljust(size, b'\0')))
    for cell, encoded in targets:
        candidate[cell:cell + len(encoded)] = encoded
    changed = sum(rom[cell:cell + len(raw)] != raw for cell, raw in targets)
    if candidate != rom:
        rom[:] = candidate
    return changed


def main() -> None:
    """Applique le patch après le build générique en conservant une sauvegarde."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    changed = apply(rom, (ROOT / 'input/roms/englishrom.gba').read_bytes())
    if rom != before:
        Path(f'{args.rom}.bak').write_bytes(before)
        args.rom.write_bytes(rom)
    print(f'PT-04 : {changed} cellules fixes mises à jour')


if __name__ == '__main__':
    main()
