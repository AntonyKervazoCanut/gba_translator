#!/usr/bin/env python3
"""PT-09 : conserve les ruptures contractuelles et les terminateurs des tampons.

Réutilise l'injecteur structuré partagé : aucune écriture sur les cellules
voisines, aucune heuristique de pointeur graphique, vérification des préimages
EN et des consommateurs concernés avant livraison.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from src.core.structured_text import StructuredTextPatch


def definitions() -> list[dict]:
    """Déclare uniquement les entrées vivantes et leurs fenêtres documentées."""
    rows = json.loads((ROOT / 'languages/pt/data/pt09_audit.json').read_text())['entries']
    return [{
        'offset': row['offset'],
        'source_hex': row['source_hex'],
        'references': [int(site, 16) for site in row['live_sites']],
        'move_ids': [],
        'layout': {
            'max_lines': 2,
            'max_width': 102 if int(row['offset'], 16) < 0x3EED08 else 192,
            'preserve_line_count': True,
        },
    } for row in rows if row.get('delivery') == 'structured']


def main() -> None:
    """Applique le contrat PT-09 après les réparations, avec sauvegarde ROM."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    patch = StructuredTextPatch(source, definitions(), ROOT / 'languages/pt/combined_pt.txt')
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = patch.apply(rom)
    if rom != before:
        Path(f'{args.rom}.bak').write_bytes(before)
        args.rom.write_bytes(rom)
    print(f'PT-09 : {stats}')


if __name__ == '__main__':
    main()
