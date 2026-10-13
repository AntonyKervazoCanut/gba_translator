#!/usr/bin/env python3
"""Export every registered Unbound UI sprite into language asset folders."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from languages.de.sprites import SPRITES
from src.graphics.sprite_image import DEFAULT_PALETTE, variant_path, write_indexed_image
from src.graphics.sprite_rom import (
    extract_block,
    extract_mapped_block,
    read_gba_palette,
    resolve_live_offset,
)


def _asset_path(directory: Path, name: str, block_count: int, index: int, extension: str) -> Path:
    path = directory / f'{name}.{extension}'
    return variant_path(path, index) if block_count > 1 else path


def _export_one(
    rom: bytes,
    directory: Path,
    name: str,
    extension: str,
    *,
    overwrite: bool,
) -> list[Path]:
    sprite = SPRITES[name]
    width = sprite.tiles_wide * 8
    height = sprite.tiles_tall * 8
    if sprite.palette is not None:
        palette = read_gba_palette(rom, sprite.palette, colours=1 << sprite.bits_per_pixel)
    elif sprite.bits_per_pixel == 4:
        palette = DEFAULT_PALETTE
    else:
        raise ValueError(f'{name}: an 8bpp sprite requires a registered palette')

    written = []
    for index, declared_offset in enumerate(sprite.blocks):
        offset = resolve_live_offset(
            rom,
            declared_offset,
            sprite.block_pointers[index] if sprite.block_pointers else (),
        )
        if sprite.tilemaps:
            tilemap_offset = resolve_live_offset(
                rom,
                sprite.tilemaps[index],
                sprite.tilemap_pointers[index] if sprite.tilemap_pointers else (),
            )
            grid, _, _ = extract_mapped_block(
                rom,
                offset,
                tilemap_offset,
                sprite.tiles_wide,
                sprite.tiles_tall,
                compressed=sprite.compressed,
                bits_per_pixel=sprite.bits_per_pixel,
            )
        else:
            start_tile = sprite.start_tiles[index] if sprite.start_tiles else 0
            grid, _, _ = extract_block(
                rom,
                offset,
                sprite.tiles_wide,
                sprite.tiles_tall,
                compressed=sprite.compressed,
                bits_per_pixel=sprite.bits_per_pixel,
                start_tile=start_tile,
            )
        path = _asset_path(directory, name, len(sprite.blocks), index, extension)
        if path.exists() and not overwrite:
            continue
        write_indexed_image(path, width, height, grid, palette)
        written.append(path)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    parser.add_argument('--lang', required=True, choices=('fr', 'it', 'de'))
    parser.add_argument(
        '--format',
        action='append',
        choices=('png', 'bmp'),
        default=None,
        help='image format to write; repeatable, defaults to png and bmp',
    )
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='replace existing assets; default only fills missing files',
    )
    args = parser.parse_args()

    directory = ROOT / 'languages' / args.lang / 'sprites'
    directory.mkdir(parents=True, exist_ok=True)
    rom = args.rom.read_bytes()
    formats = tuple(dict.fromkeys(args.format or ('png', 'bmp')))
    written = []
    for name in sorted(SPRITES):
        for extension in formats:
            written.extend(
                _export_one(
                    rom,
                    directory,
                    name,
                    extension,
                    overwrite=args.overwrite,
                )
            )

    for path in written:
        print(path.relative_to(ROOT))
    print(f'export_registered_sprites: {len(written)} file(s) written for {args.lang}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
