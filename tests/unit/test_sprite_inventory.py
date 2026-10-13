"""Public synthetic fixtures for the registry inventory and editing pilot."""
import json
from dataclasses import replace

import pytest

from languages.fr.patches.font import lz77_compress
from languages.fr.sprites import SpriteDef
from src.core.sprite_inventory import SpriteInventory
from src.graphics.sprite_image import read_indexed_image, write_indexed_image
from scripts.sprite_inventory import selected_assets


@pytest.fixture
def pilot():
    raw = bytes(range(32)) * 4
    packed = lz77_compress(raw, vram_safe=False)
    rom = bytearray(b'\xA5' * 1024)
    rom[64:64 + len(packed)] = packed
    rom[256:288] = bytes(range(32))
    registry = {
        'compressed': SpriteDef(blocks=(64,), tiles_wide=1, tiles_tall=1,
                                start_tiles=(1,), vram_safe=False),
        'raw': SpriteDef(blocks=(256,), tiles_wide=1, tiles_tall=1,
                         compressed=False),
    }
    return SpriteInventory(registry), bytes(rom)


def test_manifest_is_complete_only_for_registry(pilot):
    inventory, _ = pilot
    manifest = inventory.manifest()
    assert manifest['coverage']['rom'] == 'partial'
    assert manifest['coverage']['registry'] == 'complete'
    assert len(manifest['assets']) == 2
    assert manifest['assets'][0]['blocks'][0]['start_tile'] == 1
    assert manifest['assets'][0]['palette']['status'] == 'unknown-display-only'
    assert manifest['assets'][0]['extractability'] == 'registered-unverified'


@pytest.mark.parametrize('extension', ['png', 'bmp'])
def test_noop_is_byte_identical_and_deterministic(pilot, tmp_path, extension):
    inventory, rom = pilot
    bundle = tmp_path / 'bundle'
    inventory.export_pilot(rom, bundle, tuple(inventory.registry), extension)
    first = inventory.insert_pilot(rom, bundle, tuple(inventory.registry))
    second = inventory.insert_pilot(rom, bundle, tuple(inventory.registry))
    assert first == second == rom


def test_raw_edit_changes_only_window(pilot, tmp_path):
    inventory, rom = pilot
    bundle = tmp_path / 'bundle'
    names = tuple(inventory.registry)
    inventory.export_pilot(rom, bundle, names, 'png')
    path = bundle / 'raw-0.png'
    width, height, grid = read_indexed_image(path)
    grid[0][0] = 7
    write_indexed_image(path, width, height, grid)
    result = inventory.insert_pilot(rom, bundle, names)
    assert result[256] == 7
    assert result[:256] == rom[:256]
    assert result[257:] == rom[257:]


def test_reordered_palette_is_rejected(pilot, tmp_path):
    from src.graphics.sprite_image import DEFAULT_PALETTE
    inventory, rom = pilot
    bundle = tmp_path / 'bundle'
    names = tuple(inventory.registry)
    inventory.export_pilot(rom, bundle, names, 'png')
    path = bundle / 'raw-0.png'
    width, height, grid = read_indexed_image(path)
    write_indexed_image(path, width, height, grid, list(reversed(DEFAULT_PALETTE)))
    with pytest.raises(ValueError, match='palette'):
        inventory.insert_pilot(rom, bundle, names)


def test_wrong_rom_is_rejected(pilot, tmp_path):
    inventory, rom = pilot
    bundle = tmp_path / 'bundle'
    names = tuple(inventory.registry)
    inventory.export_pilot(rom, bundle, names, 'bmp')
    with pytest.raises(ValueError, match='SHA-256'):
        inventory.insert_pilot(rom[:-1] + b'X', bundle, names)


def test_over_budget_edit_fails_without_mutating_source(pilot, tmp_path):
    inventory, rom = pilot
    bundle = tmp_path / 'bundle'
    names = tuple(inventory.registry)
    inventory.export_pilot(rom, bundle, names, 'png')
    path = bundle / 'compressed-0.png'
    width, height, grid = read_indexed_image(path)
    grid = [[(x * 3 + y * 7) % 16 for x in range(width)] for y in range(height)]
    write_indexed_image(path, width, height, grid)
    with pytest.raises(ValueError, match='capacity'):
        inventory.insert_pilot(rom, bundle, names)
    assert isinstance(rom, bytes)


def test_invalid_pointer_rejected_on_export(pilot, tmp_path):
    inventory, rom = pilot
    inventory.registry['raw'] = replace(inventory.registry['raw'], block_pointers=((0,),))
    with pytest.raises(ValueError, match='outside ROM'):
        inventory.export_pilot(rom, tmp_path / 'bundle', ('raw',), 'png')


def test_inventory_snapshot_matches_registry():
    from pathlib import Path

    from languages.de.sprites import SPRITES
    expected = json.loads(Path('languages/de/sprite_inventory.json').read_text())
    assert SpriteInventory(SPRITES).manifest() == expected


@pytest.mark.parametrize('extension', ['png', 'bmp'])
def test_compressed_edit_preserves_other_tiles(pilot, tmp_path, extension):
    from languages.fr.patches.font import lz77_decompress
    inventory, rom = pilot
    names = tuple(inventory.registry)
    bundle = tmp_path / 'bundle'
    inventory.export_pilot(rom, bundle, names, extension)
    path = bundle / f'compressed-0.{extension}'
    width, height, _grid = read_indexed_image(path)
    write_indexed_image(path, width, height, [[0] * width for _ in range(height)])
    # This edit may need more than a tightly packed stream. Give the synthetic
    # original a valid literal-only encoding to exercise successful recompression.
    payload = bytes(range(32)) * 4
    literal = b'\x10\x80\x00\x00' + b''.join(
        b'\0' + payload[i:i + 8] for i in range(0, len(payload), 8))
    source = bytearray(rom)
    source[64:64 + len(literal)] = literal
    rom = bytes(source)
    bundle2 = tmp_path / 'literal-bundle'
    inventory.export_pilot(rom, bundle2, names, extension)
    write_indexed_image(bundle2 / path.name, width, height, [[0] * width for _ in range(height)])
    result = inventory.insert_pilot(rom, bundle2, names)
    decoded, _ = lz77_decompress(result, 64)
    assert decoded == payload[:32] + bytes(32) + payload[64:]
    assert result[:64] == rom[:64]
    assert result[64 + len(literal):] == rom[64 + len(literal):]
    assert inventory.insert_pilot(rom, bundle2, names) == result


def test_mapped_assets_excluded_from_pilot(pilot, tmp_path):
    inventory, rom = pilot
    inventory.registry['raw'] = replace(inventory.registry['raw'], tilemaps=(300,))
    with pytest.raises(ValueError, match='mapped screens'):
        inventory.export_pilot(rom, tmp_path / 'bundle', ('raw',))


@pytest.mark.parametrize('extension', ['png', 'bmp'])
def test_wrong_dimensions_rejected(pilot, tmp_path, extension):
    inventory, rom = pilot
    bundle = tmp_path / 'bundle'
    inventory.export_pilot(rom, bundle, ('raw',), extension)
    write_indexed_image(bundle / f'raw-0.{extension}', 16, 8, [[0] * 16 for _ in range(8)])
    with pytest.raises(ValueError, match='dimensions'):
        inventory.insert_pilot(rom, bundle, ('raw',))


def test_changed_registry_rejected(pilot, tmp_path):
    inventory, rom = pilot
    bundle = tmp_path / 'bundle'
    inventory.export_pilot(rom, bundle, ('raw',))
    inventory.registry['raw'] = replace(inventory.registry['raw'], blocks=(288,))
    with pytest.raises(ValueError, match='registry changed'):
        inventory.insert_pilot(rom, bundle, ('raw',))


@pytest.mark.parametrize('extension', ['png', 'bmp'])
def test_8bpp_indices_and_palette_roundtrip(tmp_path, extension):
    registry = {'eight': SpriteDef(blocks=(512,), tiles_wide=1, tiles_tall=1,
                                   compressed=False, bits_per_pixel=8, palette=0)}
    rom = bytes(512) + bytes(range(192, 256))
    inventory = SpriteInventory(registry)
    bundle = tmp_path / 'bundle'
    inventory.export_pilot(rom, bundle, ('eight',), extension)
    assert inventory.insert_pilot(rom, bundle, ('eight',)) == rom


def test_missing_copy_fails(pilot, tmp_path):
    inventory, rom = pilot
    bundle = tmp_path / 'bundle'
    names = tuple(inventory.registry)
    inventory.export_pilot(rom, bundle, names)
    (bundle / 'raw-0.png').unlink()
    with pytest.raises(FileNotFoundError):
        inventory.insert_pilot(rom, bundle, names)


def test_cli_selection_defaults_to_pilot():
    from src.core.sprite_inventory import PILOT

    assert selected_assets({'raw': object()}, None) == PILOT


def test_cli_selection_preserves_order_and_removes_duplicates(pilot):
    inventory, _ = pilot

    assert selected_assets(inventory.registry, ['raw', 'compressed', 'raw']) == (
        'raw', 'compressed'
    )


def test_cli_selection_rejects_unknown_assets(pilot):
    inventory, _ = pilot

    with pytest.raises(ValueError, match='unknown asset'):
        selected_assets(inventory.registry, ['raw', 'missing'])


def test_cli_selection_rejects_mapped_assets(pilot):
    from dataclasses import replace

    inventory, _ = pilot
    inventory.registry['mapped'] = replace(inventory.registry['raw'], tilemaps=(400,))

    with pytest.raises(ValueError, match='mapped asset'):
        selected_assets(inventory.registry, ['mapped'])
