"""Régressions des classes de dresseurs françaises (issues #161 et #184)."""

from __future__ import annotations

import struct
from pathlib import Path

import pytest

from languages.fr.patches.trainer_class_names import (
    CELL_STRIDE,
    CLASS_COUNT,
    TABLE_BASE,
    _load_combined,
    patch,
)
from src.core.text_codec import TextDecoder, TextEncoder

COMBINED_FR = Path("languages/fr/combined_fr.txt")
FR_ROM = Path("output/roms/GenedRom-fr.gba")

SWIMMER_MALE_OFFSET = 0x23E8E6
SWIMMER_FEMALE_OFFSET = 0x23E91A
TUBER_OFFSET = 0x23EA6C
COLLECTOR_OFFSET = 0x23E787

EXPECTED_CLASSES = {
    COLLECTOR_OFFSET: "Collec",
    SWIMMER_MALE_OFFSET: "Nageur♂",
    SWIMMER_FEMALE_OFFSET: "Nageuse♀",
    TUBER_OFFSET: "Flotteur",
}


def _decode_cell(rom: bytes | bytearray, offset: int) -> str:
    """Décode une cellule complète de ``gTrainerClassNames``."""
    return TextDecoder.decode_pokemon(bytes(rom[offset : offset + CELL_STRIDE]))


def test_patch_writes_expected_trainer_class_labels_in_french() -> None:
    """Le patch doit écrire les libellés français exacts des classes protégées."""
    rom = bytearray(TABLE_BASE + CLASS_COUNT * CELL_STRIDE)
    combined = _load_combined(COMBINED_FR)

    patch(rom, combined)

    for offset, expected in EXPECTED_CLASSES.items():
        assert _decode_cell(rom, offset) == expected


@pytest.mark.rom
def test_built_rom_contains_expected_trainer_class_labels() -> None:
    """La ROM livrée doit contenir les libellés réellement consommés."""
    rom = FR_ROM.read_bytes()

    for offset, expected in EXPECTED_CLASSES.items():
        assert 0xFF in rom[offset : offset + CELL_STRIDE]
        assert _decode_cell(rom, offset) == expected


def test_shared_trainer_class_keeps_first_translated_character() -> None:
    """Un alias sautant l'espace anglais ne doit pas sauter le T français."""
    rom = bytearray(TABLE_BASE + CLASS_COUNT * CELL_STRIDE + 64)
    name_offset = TABLE_BASE + CLASS_COUNT * CELL_STRIDE
    cell = TABLE_BASE + 14 * CELL_STRIDE
    encoded = TextEncoder.encode_pokemon("Terreur Granbull")
    rom[name_offset:name_offset + len(encoded)] = encoded
    struct.pack_into("<I", rom, cell, 0x08000000 + name_offset + 1)
    before = bytes(rom)

    patch(rom, {name_offset: "Terreur Granbull"})

    pointer = struct.unpack_from("<I", rom, cell)[0] - 0x08000000
    assert TextDecoder.decode_pokemon(bytes(rom[pointer:pointer + 32])) == "Terreur Granbull"
    assert rom[:cell] == before[:cell]
    assert rom[cell + 4:] == before[cell + 4:]
    once = bytes(rom)
    patch(rom, {name_offset: "Terreur Granbull"})
    assert bytes(rom) == once


def test_shared_trainer_class_does_not_repoint_an_unverified_translation() -> None:
    """Un nom différent de la traduction attendue laisse le pointeur intact."""
    rom = bytearray(TABLE_BASE + CLASS_COUNT * CELL_STRIDE + 64)
    name_offset = TABLE_BASE + CLASS_COUNT * CELL_STRIDE
    cell = TABLE_BASE + 14 * CELL_STRIDE
    encoded = TextEncoder.encode_pokemon("Terror Granbull")
    rom[name_offset:name_offset + len(encoded)] = encoded
    struct.pack_into("<I", rom, cell, 0x08000000 + name_offset + 1)
    before = bytes(rom)

    patch(rom, {name_offset: "Terreur Granbull"})

    assert bytes(rom) == before


@pytest.mark.rom
def test_built_rom_shared_trainer_class_reads_complete_name() -> None:
    """Vérifie le pointeur vivant, pas seulement les octets du titre de mission."""
    rom = FR_ROM.read_bytes()
    pointer = struct.unpack_from("<I", rom, TABLE_BASE + 14 * CELL_STRIDE)[0] - 0x08000000

    assert TextDecoder.decode_pokemon(rom[pointer:pointer + 32]) == "Terreur Granbull"
