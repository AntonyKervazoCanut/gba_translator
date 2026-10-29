"""Périmètre figé B-1026, partagé par l'exclusion et le patch DE."""
import json
from pathlib import Path

MANIFEST = json.loads((Path(__file__).parent / 'data/item_names_objets_01.json').read_text())
PREIMAGES = {int(row['offset'], 16): bytes.fromhex(row['source_hex'])
             for row in MANIFEST['entries']}
OFFSETS = frozenset(PREIMAGES)
