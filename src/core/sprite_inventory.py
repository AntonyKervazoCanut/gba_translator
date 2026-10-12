"""Registry inventory and conservative, source-bound sprite editing pilot."""
from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path

from languages.fr.sprites import SpriteDef
from src.graphics.sprite_image import (
    DEFAULT_PALETTE,
    read_indexed_image,
    write_indexed_image,
)
from src.graphics.sprite_rom import (
    extract_block,
    insert_block,
    read_gba_palette,
    resolve_live_offset,
)

PILOT = ('battle_kp_labels', 'type_icons_summary', 'summary_stat_labels')


def sha256(data: bytes) -> str:
    """Return a stable fingerprint without distributing ROM bytes."""
    return hashlib.sha256(data).hexdigest()


def image_palette(path: Path) -> list[tuple[int, int, int]]:
    """Read the ordered RGB palette after validating the indexed image."""
    read_indexed_image(path)
    data = path.read_bytes()
    if path.suffix.lower() == '.png':
        cursor = 8
        while cursor + 12 <= len(data):
            size = int.from_bytes(data[cursor:cursor + 4], 'big')
            if data[cursor + 4:cursor + 8] == b'PLTE':
                raw = data[cursor + 8:cursor + 8 + size]
                return [tuple(raw[i:i + 3]) for i in range(0, len(raw), 3)]
            cursor += size + 12
    else:
        header_size = int.from_bytes(data[14:18], 'little')
        if header_size != 40:
            raise ValueError('pilot requires a Windows BITMAPINFOHEADER BMP')
        count = int.from_bytes(data[46:50], 'little')
        count = count or (1 << int.from_bytes(data[28:30], 'little'))
        start = 14 + header_size
        end = start + count * 4
        if end > int.from_bytes(data[10:14], 'little') or end > len(data):
            raise ValueError('truncated BMP palette')
        return [(r, g, b) for b, g, r, _ in struct.iter_unpack('<BBBB', data[start:end])]
    raise ValueError('missing image palette')


class SpriteInventory:
    """Expose registered metadata and a deliberately bounded editing workflow.

    Args:
        registry: Named SpriteDef records; offsets are never discovered by scanning.
    """

    def __init__(self, registry: dict[str, SpriteDef]) -> None:
        self.registry = dict(registry)

    def manifest(self) -> dict:
        """Return deterministic metadata, explicitly excluding full-ROM coverage."""
        assets = []
        for name, sprite in sorted(self.registry.items()):
            blocks = []
            for i, offset in enumerate(sprite.blocks):
                blocks.append({
                    'index': i,
                    'offset': f'0x{offset:08X}',
                    'pointer_locations': [f'0x{p:08X}' for p in (
                        sprite.block_pointers[i] if sprite.block_pointers else ())],
                    'start_tile': sprite.start_tiles[i] if sprite.start_tiles else 0,
                    'tilemap_offset': f'0x{sprite.tilemaps[i]:08X}' if sprite.tilemaps else None,
                    'tilemap_pointer_locations': [f'0x{p:08X}' for p in (
                        sprite.tilemap_pointers[i] if sprite.tilemap_pointers else ())],
                    'declared_compressed_capacity': (
                        sprite.max_compressed_sizes[i] if sprite.max_compressed_sizes else None),
                })
            category = ('battle-summary' if name in PILOT or name.startswith(
                ('battle_', 'summary_', 'party_', 'type_', 'status_', 'level_'))
                else 'screen' if name.startswith(('trainer_card', 'title_')) else 'menu-world')
            assets.append({
                'asset_id': name, 'category': category,
                'width': sprite.tiles_wide * 8, 'height': sprite.tiles_tall * 8,
                'dimensions_meaning': 'editable-window',
                'bits_per_pixel': sprite.bits_per_pixel,
                'compression': 'gba-lz77-0x10' if sprite.compressed else 'raw',
                'vram_safe_compression': sprite.vram_safe,
                'palette': {
                    'offset': f'0x{sprite.palette:08X}' if sprite.palette is not None else None,
                    'status': 'registered-rom-palette' if sprite.palette is not None else 'unknown-display-only',
                    'colours': 1 << sprite.bits_per_pixel,
                },
                'tilemap_compression': 'gba-lz77-0x10' if sprite.tilemaps else None,
                'tilemap_status': 'registered' if sprite.tilemaps else 'not-registered',
                'extractability': 'registered-unverified',
                'pilot': name in PILOT,
                'blocks': blocks,
            })
        return {
            'schema_version': 1,
            'target': 'Pokemon Unbound 2.1.1.1',
            'rom_version_verified': False,
            'coverage': {'registry': 'complete', 'rom': 'partial',
                         'unknown_asset_count': None,
                         'pointer_references': 'known-only'},
            'assets': assets,
        }

    def _read(self, rom: bytes, sprite: SpriteDef, index: int) -> tuple:
        if sprite.tilemaps:
            raise ValueError('mapped screens are outside the pilot; use the mapped workflow')
        pointers = sprite.block_pointers[index] if sprite.block_pointers else ()
        offset = resolve_live_offset(rom, sprite.blocks[index], pointers)
        if not 0 <= offset < len(rom):
            raise ValueError('sprite offset outside ROM')
        start = sprite.start_tiles[index] if sprite.start_tiles else 0
        grid, decoded, stored = extract_block(
            rom, offset, sprite.tiles_wide, sprite.tiles_tall,
            compressed=sprite.compressed, bits_per_pixel=sprite.bits_per_pixel,
            start_tile=start,
        )
        palette = (read_gba_palette(rom, sprite.palette, colours=1 << sprite.bits_per_pixel)
                   if sprite.palette is not None else DEFAULT_PALETTE)
        if len(palette) != 1 << sprite.bits_per_pixel:
            raise ValueError('8bpp export requires a registered palette')
        return offset, start, grid, decoded, stored, palette

    def export_pilot(self, rom: bytes, directory: Path, names: tuple[str, ...] = PILOT,
                     extension: str = 'png') -> dict:
        """Export all selected copies plus source identity; refuse existing bundles."""
        if extension not in ('png', 'bmp'):
            raise ValueError('expected png or bmp')
        prepared = []
        for name in names:
            sprite = self.registry[name]
            for index in range(len(sprite.blocks)):
                prepared.append((name, index, self._read(rom, sprite, index)))
        directory.mkdir(parents=True, exist_ok=False)
        records = []
        for name, index, (offset, start, grid, decoded, stored, palette) in prepared:
            sprite = self.registry[name]
            filename = f'{name}-{index}.{extension}'
            write_indexed_image(directory / filename, sprite.tiles_wide * 8,
                                sprite.tiles_tall * 8, grid, palette)
            records.append({'asset_id': name, 'block_index': index, 'image': filename,
                            'resolved_offset': f'0x{offset:08X}', 'start_tile': start,
                            'decoded_bytes': decoded, 'stored_bytes': stored,
                            'pilot_byte_budget': stored,
                            'extractability': 'verified-on-source'})
        metadata = {'schema_version': 1, 'source_sha256': sha256(rom),
                    'source_size': len(rom), 'rom_version_verified': False,
                    'registry_sha256': sha256(json.dumps(self.manifest(), sort_keys=True).encode()),
                    'names': list(names), 'format': extension, 'assets': records}
        (directory / 'bundle.json').write_text(json.dumps(metadata, indent=2) + '\n')
        return metadata

    def insert_pilot(self, rom: bytes, directory: Path,
                     names: tuple[str, ...] = PILOT) -> bytes:
        """Validate every image, then return a bounded ROM edit without file writes.

        Palette order, source identity, dimensions and pixel indices must match
        the export contract. Compressed blocks may not grow beyond their original
        stream lengths. Unchanged images preserve the original compressed bytes.
        """
        metadata = json.loads((directory / 'bundle.json').read_text())
        if metadata.get('source_sha256') != sha256(rom):
            raise ValueError('source SHA-256 differs from export')
        if metadata.get('schema_version') != 1 or metadata.get('names') != list(names):
            raise ValueError('unsupported bundle schema or asset selection')
        if metadata.get('registry_sha256') != sha256(
                json.dumps(self.manifest(), sort_keys=True).encode()):
            raise ValueError('registry changed since export')
        extension = metadata.get('format')
        if extension not in ('png', 'bmp'):
            raise ValueError('unsupported bundle format')
        output = bytearray(rom)
        for name in names:
            sprite = self.registry[name]
            for index in range(len(sprite.blocks)):
                offset, start, original, _, stored, palette = self._read(rom, sprite, index)
                image = directory / f'{name}-{index}.{extension}'
                width, height, grid = read_indexed_image(image)
                if (width, height) != (sprite.tiles_wide * 8, sprite.tiles_tall * 8):
                    raise ValueError(f'{image.name}: dimensions changed')
                if image_palette(image) != palette:
                    raise ValueError(f'{image.name}: palette changed or reordered')
                if any(p < 0 or p >= 1 << sprite.bits_per_pixel for row in grid for p in row):
                    raise ValueError(f'{image.name}: palette index out of range')
                if grid == original:
                    continue
                insert_block(output, offset, grid, sprite.tiles_wide, sprite.tiles_tall,
                             compressed=sprite.compressed, vram_safe=sprite.vram_safe,
                             bits_per_pixel=sprite.bits_per_pixel, start_tile=start,
                             max_compressed_size=stored)
                restored = self._read(bytes(output), sprite, index)[2]
                if restored != grid:
                    raise ValueError(f'{image.name}: re-extraction mismatch')
        return bytes(output)
