"""Finalise uniquement les cellules fixes des mouvements PT-41."""
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
    """Valide les lecteurs et restaure les noms canoniques sans toucher aux voisins."""
    audit = json.loads((ROOT / 'languages/pt/data/pt41_audit.json').read_text())
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    base = int(audit['table_base'], 16)
    for ref in audit['table_references']:
        expected = (base + 0x08000000).to_bytes(4, 'little')
        if source[ref:ref + 4] != expected or rom[ref:ref + 4] != expected:
            raise ValueError(f'Lecteur de mouvements PT-41 différent : {ref:#x}')
    writes = {}
    for row in audit['entries']:
        offset = int(row['offset'], 16)
        cell = bytes.fromhex(row['source_hex'])
        encoded = TextEncoder.encode_pokemon(texts[offset], strict=True)
        if (offset != base + row['move_id'] * 13 or len(cell) != 13
                or source[offset:offset + 13] != cell
                or texts[offset] != row['english']
                or len(encoded) > 13 or cell[:len(encoded)] != encoded):
            raise ValueError(f'Cellule canonique PT-41 différente : {offset:#x}')
        writes[offset] = cell
    for offset, cell in writes.items():
        rom[offset:offset + 13] = cell
    return len(writes)


def main() -> None:
    """Sauvegarde la ROM puis finalise les 282 cellules du manifeste."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    count = apply_patches(rom, source)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-41 : {count} noms canoniques vérifiés')


if __name__ == '__main__':
    main()
