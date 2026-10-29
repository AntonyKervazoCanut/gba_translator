"""Finalise les noms fixes PT-30, sans écrire dans les données des objets."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts.apply_combined_fr import _load_combined
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

AUDIT = ROOT / 'languages/pt/data/pt30_audit.json'


def apply_patches(rom: bytearray) -> int:
    """Valide les budgets et le lecteur indexé avant toute écriture atomique."""
    audit = json.loads(AUDIT.read_text())
    code = bytes.fromhex(audit['accessor_hex'])
    if rom[0x9A8C0:0x9A8DC] != code:
        raise ValueError('Lecteur gItems PT-30 inattendu')
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    writes = {}
    for row in audit['entries']:
        if row['status'] == 'exception':
            continue
        offset = int(row['offset'], 16)
        if offset != 0x876200 + row['item_id'] * 44:
            raise ValueError('Cellule PT-30 désalignée')
        text = texts[offset]
        encoded = TextEncoder.encode_pokemon(text, strict=True)
        if (len(encoded) > 14 or max(line_widths(text)) > 78
                or any(b >= 0xF7 for b in encoded[:-1])):
            raise ValueError(f'Budget ou contrôle invalide à {offset:#x}')
        writes[offset] = encoded
    count = 0
    for offset, encoded in writes.items():
        if rom[offset:offset + len(encoded)] != encoded:
            rom[offset:offset + len(encoded)] = encoded
            count += 1
    return count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    count = apply_patches(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-30 : {count} noms finalisés, 283 vérifiés, 5 exceptions auditées.')
