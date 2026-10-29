#!/usr/bin/env python3
"""PT-15 : finalise les crédits, échanges, Cadeau Mystère et fiches Pokédex."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from src.core.structured_text import StructuredTextPatch


def make_patch(source: bytes) -> StructuredTextPatch:
    """Résout le padding des crédits sans inventer d'offset de traduction."""
    rows = json.loads((ROOT / 'languages/pt/data/pt15_audit.json').read_text())['entries']
    definitions = [dict(row) for row in rows if row['status'] == 'translated']
    patch = StructuredTextPatch(source, definitions, ROOT / 'languages/pt/combined_pt.txt')
    for row in definitions:
        delta = row['source_delta']
        if not delta:
            continue
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        text = patch.texts[offset]
        if raw[:delta] != bytes(delta) or text[:delta] != ' ' * delta:
            raise ValueError(f'{offset:#x}: padding des crédits différent')
        # Les extractions historiques démarrent avant le pointeur consommateur.
        # Le combined reste indexé par le seul offset autorisé du manifeste.
        row['offset'] = hex(offset + delta)
        row['source_hex'] = raw[delta:].hex()
        patch.texts[offset + delta] = text[delta:]
    return patch


def main() -> int:
    """Sauvegarde puis injecte les textes et contrôle tous leurs consommateurs."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch(source).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-15 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
