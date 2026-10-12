#!/usr/bin/env python3
"""Stabilise les libellés d'action partagés (#111 / #131 / #178).

Le bandeau partagé dépasse d'un octet sa cellule originale : le point final
d'« Annul. » écrase la chaîne vide à 0x418E8B, affichée comme une action
indépendante sur la carte (#194). Il est relogé dans une cellule libre après
les libellés PC ; la chaîne vide est restaurée pour les deux variantes carte.
Les libellés « Annul. » propres à la carte gardent leurs cellules et pointeurs.
"""

from __future__ import annotations

import argparse
import struct
from pathlib import Path

ROM_BASE = 0x08000000
WORLD_MAP_HINT_POINTER = 0x9FB64
WORLD_MAP_HINT_RELOCATED_OFFSET = 0x15FBD30
WORLD_MAP_HINT_CPU_ADDR = ROM_BASE + WORLD_MAP_HINT_RELOCATED_OFFSET
WORLD_MAP_EMPTY_ACTION_OFFSET = 0x418E8B
WORLD_MAP_EMPTY_ACTION_BYTES = bytes.fromhex("00ff")

# {DPAD_ANY}Dépl. {SE_SHOP}OK {B_BUTTON}Annul. + terminateur CFRU.
WORLD_MAP_HINT_BYTES = bytes.fromhex(
    "f80cbe1be4e0ad00f800c9c500f801bbe2e2e9e0adff"
)

# {SE_SHOP}Annul. + terminateur CFRU, même largeur que {SE_SHOP}Cancel.
WORLD_MAP_CANCEL_BYTES = bytes.fromhex("f800bbe2e2e9e0adff")
WORLD_MAP_CANCEL_OFFSETS = (0x418E95, 0x418E9E)
WORLD_MAP_CANCEL_POINTER_TARGETS = (
    (0xC06FC, 0x418E95),
    (0xC1B28, 0x418E9E),
    (0xC50C0, 0x418E95),
)


def apply(rom: bytearray) -> int:
    """Restaure les cellules courtes et leurs pointeurs vivants.

    Returns:
        Nombre d'éléments modifiés (cellule et/ou pointeur).
    """
    minimum_size = max(
        WORLD_MAP_HINT_POINTER + 4,
        WORLD_MAP_HINT_RELOCATED_OFFSET + len(WORLD_MAP_HINT_BYTES),
        *(
            offset + len(WORLD_MAP_CANCEL_BYTES)
            for offset in WORLD_MAP_CANCEL_OFFSETS
        ),
        *(
            pointer + 4
            for pointer, _target in WORLD_MAP_CANCEL_POINTER_TARGETS
        ),
    )
    if len(rom) < minimum_size:
        raise ValueError(
            f"ROM trop courte ({len(rom)} octets, minimum {minimum_size})"
        )

    slot = bytes(rom[
        WORLD_MAP_HINT_RELOCATED_OFFSET:
        WORLD_MAP_HINT_RELOCATED_OFFSET + len(WORLD_MAP_HINT_BYTES)
    ])
    if slot not in (b"\xff" * len(WORLD_MAP_HINT_BYTES), WORLD_MAP_HINT_BYTES):
        raise ValueError("Cellule de relocalisation du bandeau carte occupée")

    patched = 0
    hint_end = WORLD_MAP_HINT_RELOCATED_OFFSET + len(WORLD_MAP_HINT_BYTES)
    if bytes(rom[WORLD_MAP_HINT_RELOCATED_OFFSET:hint_end]) != WORLD_MAP_HINT_BYTES:
        rom[WORLD_MAP_HINT_RELOCATED_OFFSET:hint_end] = WORLD_MAP_HINT_BYTES
        patched += 1

    if struct.unpack_from("<I", rom, WORLD_MAP_HINT_POINTER)[0] != (
        WORLD_MAP_HINT_CPU_ADDR
    ):
        struct.pack_into(
            "<I", rom, WORLD_MAP_HINT_POINTER, WORLD_MAP_HINT_CPU_ADDR
        )
        patched += 1

    empty_end = WORLD_MAP_EMPTY_ACTION_OFFSET + len(WORLD_MAP_EMPTY_ACTION_BYTES)
    if (
        bytes(rom[WORLD_MAP_EMPTY_ACTION_OFFSET:empty_end])
        != WORLD_MAP_EMPTY_ACTION_BYTES
    ):
        rom[WORLD_MAP_EMPTY_ACTION_OFFSET:empty_end] = WORLD_MAP_EMPTY_ACTION_BYTES
        patched += 1

    for offset in WORLD_MAP_CANCEL_OFFSETS:
        end = offset + len(WORLD_MAP_CANCEL_BYTES)
        if bytes(rom[offset:end]) != WORLD_MAP_CANCEL_BYTES:
            rom[offset:end] = WORLD_MAP_CANCEL_BYTES
            patched += 1

    for pointer, target in WORLD_MAP_CANCEL_POINTER_TARGETS:
        target_cpu_addr = ROM_BASE + target
        if struct.unpack_from("<I", rom, pointer)[0] != target_cpu_addr:
            struct.pack_into("<I", rom, pointer, target_cpu_addr)
            patched += 1

    return patched


def main() -> int:
    """Applique le patch à la ROM française construite."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--rom",
        type=Path,
        default=Path("output/roms/GenedRom-fr.gba"),
    )
    args = parser.parse_args()

    if not args.rom.exists():
        raise SystemExit(f"ROM introuvable : {args.rom}")

    original = args.rom.read_bytes()
    if len(original) <= 0xB2 or original[0xB2] != 0x96:
        raise SystemExit(f"ROM GBA invalide : {args.rom}")

    rom = bytearray(original)
    patched = apply(rom)
    if patched:
        Path(f"{args.rom}.bak").write_bytes(original)
        args.rom.write_bytes(rom)

    print(
        "patch_world_map_action_labels_fr: "
        f"{patched} élément(s) restauré(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
