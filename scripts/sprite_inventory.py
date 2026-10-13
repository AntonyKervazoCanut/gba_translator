#!/usr/bin/env python3
"""Inventory known DE sprites; export, validate and reinsert guarded assets."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from languages.de.sprites import SPRITES
from scripts.insert_sprite import _write_rom_safely
from src.core.sprite_inventory import PILOT, SpriteInventory, sha256


def output_path(value: str) -> Path:
    """Restrict generated artifacts to the current checkout's output directory."""
    path = Path(value).resolve()
    if not path.is_relative_to((ROOT / 'output').resolve()):
        raise argparse.ArgumentTypeError('generated artifacts must be under output/')
    return path


def selected_assets(registry: dict, requested: list[str] | None) -> tuple[str, ...]:
    """Return the requested registered assets, or the conservative pilot default."""
    if not requested:
        return PILOT
    unknown = sorted(set(requested) - set(registry))
    if unknown:
        raise ValueError(f"unknown asset(s): {', '.join(unknown)}")
    mapped = sorted(name for name in set(requested) if registry[name].tilemaps)
    if mapped:
        raise ValueError(
            'mapped asset(s) require the mapped sprite workflow: ' + ', '.join(mapped)
        )
    return tuple(dict.fromkeys(requested))


def main() -> int:
    """Run the read-only inventory or a fail-closed editing pilot."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('manifest', help='print deterministic registry JSON; no ROM needed')
    export = commands.add_parser(
        'export',
        help='export the default pilot, or selected registered non-mapped assets',
    )
    export.add_argument('--rom', type=Path, required=True)
    export.add_argument('--directory', type=output_path, required=True)
    export.add_argument('--format', choices=('png', 'bmp'), default='png')
    for name in ('verify', 'insert'):
        command = commands.add_parser(name)
        command.add_argument('--rom', type=Path, required=True)
        command.add_argument('--directory', type=Path, required=True)
        if name == 'insert':
            command.add_argument('--out', type=output_path, required=True)
    for command in (export, *[commands.choices[name] for name in ('verify', 'insert')]):
        command.add_argument(
            '--asset',
            action='append',
            choices=tuple(sorted(SPRITES)),
            help=(
                'registered non-mapped asset to process; repeat for batches. '
                'Defaults to the three-asset pilot.'
            ),
        )
    args = parser.parse_args()
    inventory = SpriteInventory(SPRITES)
    try:
        if args.command == 'manifest':
            result = inventory.manifest()
        else:
            names = selected_assets(SPRITES, args.asset)
            rom = args.rom.read_bytes()
            if args.command == 'export':
                result = inventory.export_pilot(
                    rom, args.directory, names=names, extension=args.format
                )
            else:
                first = inventory.insert_pilot(rom, args.directory, names=names)
                second = inventory.insert_pilot(rom, args.directory, names=names)
                if first != second:
                    raise ValueError('non-deterministic insertion')
                if args.command == 'verify' and first != rom:
                    raise ValueError('no-op verification failed: image indices differ from source')
                result = {'source_sha256': sha256(rom), 'result_sha256': sha256(first),
                          'byte_identical': first == rom, 'deterministic': True,
                          'size_unchanged': len(first) == len(rom)}
                if args.command == 'insert':
                    if args.out.resolve() == args.rom.resolve():
                        raise ValueError('output must differ from source ROM')
                    if args.out.exists() or Path(f'{args.out}.bak').exists():
                        raise ValueError('output already exists; choose a fresh output path')
                    args.out.parent.mkdir(parents=True, exist_ok=True)
                    # All checks passed before creating output. The existing safe
                    # writer backs up these source bytes and atomically replaces them.
                    args.out.write_bytes(rom)
                    _write_rom_safely(args.out, first)
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, f'sprite_inventory: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
