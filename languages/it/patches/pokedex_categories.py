#!/usr/bin/env python3
"""Translate Pokédex species-category strings (table 0x1A357CC) to Italian.

The Pokédex info screen renders ``<category> Pokémon`` where ``<category>`` is
read from a table at ROM offset **0x1A357CC**, stride 36 bytes, indexed by
National Dex number (entry 0 = #1 Bulbasaur).  Each entry reserves **12 bytes**
for the category: up to 11 CFRU-encoded characters followed by a 0xFF
terminator.  The numeric height/weight/scale fields start at record+12, so the
patch must never write past that boundary.

Without this patch every category displays in English (e.g. ``Poison Pin
Pokémon``, ``Licking Pokémon``).  With the patch they display in Italian
(e.g. ``SpinaVelen-Pokémon``, ``Leccatore-Pokémon``).

The mapping is loaded from ``languages/it/data/pokedex_categories_it.json`` (653 EN→IT
pairs).  Entries not found in the mapping are left unchanged.  The patch is
idempotent: running it twice produces the same ROM bytes.

Usage (run by ``make build-it`` after the base injection):
    python3 languages/it/patches/pokedex_categories.py --rom output/roms/GenedRom-it.gba
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Table geometry
# ---------------------------------------------------------------------------
TABLE_ADDR = 0x1A357CC   # first record = Dex #1
STRIDE = 36              # bytes per record
MAX_ENTRIES = 908        # up to Dex #907 (0-indexed: entries 0..906)
CELL_SIZE = 12           # bytes reserved for category (11 chars + 0xFF)
MAX_CHARS = CELL_SIZE - 1  # 11

# Table partagée : évite les anciennes allocations DE 0x60–0x65.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.text.charmap_data import BYTE_TO_CHAR, CHAR_TO_BYTE


def _decode_cell(data: bytes | bytearray, offset: int) -> str:
    """Decode up to CELL_SIZE-1 bytes from *offset*, stopping at 0xFF."""
    result: list[str] = []
    for i in range(MAX_CHARS):
        b = data[offset + i]
        if b == 0xFF:
            break
        result.append(BYTE_TO_CHAR.get(b, f'[{b:02X}]'))
    return ''.join(result)


def _encode(text: str) -> bytes:
    """Encode *text* to CFRU bytes + 0xFF terminator."""
    if len(text) > MAX_CHARS:
        raise ValueError(f'Category too long ({len(text)} > {MAX_CHARS}): {text!r}')
    raw = bytearray()
    for ch in text:
        if ch not in CHAR_TO_BYTE:
            raise ValueError(f'Unencodable character {ch!r} in {text!r}')
        raw.append(CHAR_TO_BYTE[ch])
    raw.append(0xFF)
    return bytes(raw)


def load_mapping(data_dir: Path) -> dict[str, str]:
    path = data_dir / 'pokedex_categories_it.json'
    with path.open(encoding='utf-8') as fh:
        return json.load(fh)


def apply_patch(data: bytearray, mapping: dict[str, str]) -> tuple[int, int]:
    """Write IT categories into *data* in-place.

    Returns (patched, skipped) counts.
    """
    patched = 0
    skipped = 0
    for idx in range(MAX_ENTRIES):
        cell_offset = TABLE_ADDR + idx * STRIDE
        if cell_offset + CELL_SIZE > len(data):
            break
        en_cat = _decode_cell(data, cell_offset)
        if not en_cat or '[' in en_cat:
            # empty or contains undecodable bytes — leave alone
            skipped += 1
            continue
        it_cat = mapping.get(en_cat)
        if it_cat is None:
            skipped += 1
            continue
        it_bytes = _encode(it_cat)
        # Pad remaining space with 0xFF to clear old bytes
        padded = it_bytes + b'\xFF' * (CELL_SIZE - len(it_bytes))
        current = bytes(data[cell_offset:cell_offset + CELL_SIZE])
        if current == padded:
            continue  # already patched — idempotent
        data[cell_offset:cell_offset + CELL_SIZE] = padded
        patched += 1
    return patched, skipped


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--rom', type=Path, default=Path('output/roms/GenedRom-it.gba'),
        help='IT ROM to patch in place',
    )
    parser.add_argument(
        '--data-dir', type=Path, default=Path('languages/it/data'),
        help='Directory containing pokedex_categories_it.json',
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Report what would be patched without writing',
    )
    args = parser.parse_args(argv)

    mapping = load_mapping(args.data_dir)
    data = bytearray(args.rom.read_bytes())
    patched, skipped = apply_patch(data, mapping)
    if not args.dry_run and patched:
        args.rom.write_bytes(data)
    print(
        f'Pokédex categories IT patch: {patched} translated, '
        f'{skipped} skipped (no mapping / undecodable)'
    )
    return 0


if __name__ == '__main__':
    sys.exit(main())
