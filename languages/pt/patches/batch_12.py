#!/usr/bin/env python3
"""Livre les menus PT-12 aux seuls consommateurs prouvés par la ROM EN."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from src.core.structured_text import StructuredTextPatch


def definitions() -> list[dict]:
    """Déclare les pointeurs de menus et de scripts, sans écrire leurs voisins."""
    rows = json.loads((ROOT / 'languages/pt/data/pt12_audit.json').read_text())['entries']
    return [{
        'offset': row['offset'], 'source_hex': row['source_hex'],
        'references': [int(site, 16) for site in row['live_sites']],
        'move_ids': [],
        'layout': {'max_lines': 2, 'max_width': 192, 'preserve_line_count': True},
    } for row in rows if row['status'] == 'translated']


def apply(rom: bytearray, source: bytes) -> dict[str, int]:
    """Livre les textes puis restaure les cinq faux pointeurs graphiques.

    Le scanner générique peut prendre quatre octets compressés pour une adresse.
    Ces cinq séquences sont des données graphiques, pas des consommateurs de texte.
    La copie locale garde l'opération atomique si une préimage est invalide.
    """
    patch = StructuredTextPatch(source, definitions(), ROOT / 'languages/pt/combined_pt.txt')
    candidate = bytearray(rom)
    stats = patch.apply(candidate)
    audit = json.loads((ROOT / 'languages/pt/data/pt12_audit.json').read_text())
    for site in audit['rejected_sites']:
        start = int(site, 16)
        candidate[start:start + 4] = source[start:start + 4]
    rom[:] = candidate
    return stats


def main() -> None:
    """Applique le contrat final avec validation atomique et sauvegarde ROM."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = apply(rom, source)
    if rom != before:
        Path(f'{args.rom}.bak').write_bytes(before)
        args.rom.write_bytes(rom)
    print(f'PT-12 : {stats}')


if __name__ == '__main__':
    main()
