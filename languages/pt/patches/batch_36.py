"""Finalise les pointeurs de descriptions et les cellules de talents PT-36."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts.apply_combined_fr import _load_combined
from src.core.dialogue_linewrap import line_widths
from src.core.structured_text import StructuredTextPatch
from src.core.text_codec import TextEncoder


def make_patch(source: bytes) -> StructuredTextPatch:
    """Charge les seuls pointeurs prouvés du manifeste PT-36."""
    audit = json.loads((ROOT / 'languages/pt/data/pt36_audit.json').read_text())
    rows = [r for r in audit['entries']
            if r['kind'] == 'description' and r['status'] == 'translated']
    return StructuredTextPatch(source, rows, ROOT / 'languages/pt/combined_pt.txt')


def apply_patches(rom: bytearray, source: bytes) -> dict[str, int]:
    """Valide les lecteurs et budgets puis écrit atomiquement les seuls talents du lot."""
    audit = json.loads((ROOT / 'languages/pt/data/pt36_audit.json').read_text())
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    for prefix in ('name', 'custom'):
        start = int(audit[f'{prefix}_accessor_offset'], 16)
        code = bytes.fromhex(audit[f'{prefix}_accessor_hex'])
        if source[start:start + len(code)] != code or rom[start:start + len(code)] != code:
            raise ValueError(f'Lecteur {prefix} PT-36 inattendu')
    writes = {}
    for row in audit['entries']:
        if row['status'] == 'exception':
            continue
        offset = int(row['offset'], 16)
        text = texts[offset]
        encoded = TextEncoder.encode_pokemon(text, strict=True)
        if any(c >= 0xF7 for c in encoded[:-1]) or max(line_widths(text)) > 192:
            raise ValueError(f'Contrôle ou largeur PT-36 invalide : {offset:#x}')
        if row['kind'] == 'name':
            if offset != 0xA36398 + row['ability_ids'][0] * 17 or len(encoded) > 17:
                raise ValueError(f'Cellule PT-36 invalide : {offset:#x}')
            if max(line_widths(text)) > 120:
                raise ValueError(f'Nom PT-36 trop large : {offset:#x}')
            writes[offset] = encoded
    working = bytearray(rom)
    stats = make_patch(source).apply(working)
    for offset, encoded in writes.items():
        working[offset:offset + len(encoded)] = encoded
    rom[:] = working
    return dict(stats, names=len(writes))


def main() -> None:
    """Sauvegarde la ROM avant de finaliser les chaînes du lot."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = apply_patches(rom, source)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-36 : {stats}')


if __name__ == '__main__':
    main()
