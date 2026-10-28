"""Gardes unitaires du patch des descriptions d'objets CT/CS."""

from __future__ import annotations

import struct

import pytest

from languages.fr.patches import tm_item_descriptions as mod
from src.core.text_codec import TextDecoder, TextEncoder

ROM_SIZE = 0xA50000
FREE_RUN_START = 0x600000
FREE_RUN_SIZE = 0x4000
CT108_INDEX = 0x1B1
CT108_DESCRIPTION_OFFSET = 0xA38FF2
CT112_INDEX = 0x1B5
CT112_DESCRIPTION_OFFSET = 0xA3A77D
CT108_DESCRIPTION = (
    "Aboie menaçant.\n"
    "Baisse aussi\n"
    "l'Att. Spé\n"
    "ennemie."
)


def _put_item(rom: bytearray, index: int, name: str, desc_offset: int) -> None:
    """Écrit une entrée objet minimale avec son pointeur de description."""
    base = mod.ITEM_TABLE_BASE + index * mod.ITEM_STRIDE
    encoded_name = TextEncoder.encode_pokemon(name)
    rom[base:base + len(encoded_name)] = encoded_name
    rom[base + mod.DESC_PTR_OFFSET:base + mod.DESC_PTR_OFFSET + 4] = struct.pack(
        "<I", desc_offset + mod.ROM_POINTER_BASE
    )


def _decode_live_description(rom: bytes, index: int) -> tuple[int, str]:
    """Suit puis décode le pointeur de description vivant d'un objet."""
    base = mod.ITEM_TABLE_BASE + index * mod.ITEM_STRIDE
    pointer = struct.unpack_from("<I", rom, base + mod.DESC_PTR_OFFSET)[0]
    offset = pointer - mod.ROM_POINTER_BASE
    end = rom.index(b"\xff", offset)
    return offset, TextDecoder.decode_pokemon(rom[offset:end])


def test_short_terminated_fragment_is_relocated_to_canonical_text() -> None:
    # Arrange : le fragment de CT108 est court et possède un terminateur,
    # mais il ne correspond pas à sa valeur canonique.
    rom = bytearray(b"\x00" * ROM_SIZE)
    rom[FREE_RUN_START:FREE_RUN_START + FREE_RUN_SIZE] = b"\xff" * FREE_RUN_SIZE
    fragment = TextEncoder.encode_pokemon("nsi sa\nstatistique de vitesse.\n")
    rom[
        CT108_DESCRIPTION_OFFSET:CT108_DESCRIPTION_OFFSET + len(fragment)
    ] = fragment
    _put_item(rom, CT108_INDEX, "CT108", CT108_DESCRIPTION_OFFSET)

    # Act
    stats = mod.apply(rom, {CT108_DESCRIPTION_OFFSET: CT108_DESCRIPTION})

    # Assert
    live_offset, live_text = _decode_live_description(rom, CT108_INDEX)
    assert stats["relocated"] == 1
    assert live_offset != CT108_DESCRIPTION_OFFSET
    assert FREE_RUN_START <= live_offset < FREE_RUN_START + FREE_RUN_SIZE
    assert live_text == CT108_DESCRIPTION


@pytest.mark.parametrize("use_source", [False, True])
def test_protected_gift_item_is_left_for_its_struct_guard(use_source: bool) -> None:
    # CT112 est un objet cadeau dont le pointeur doit rester identique à
    # l'anglais. Sa description partagée n'est jamais rendue par ce chemin.
    rom = bytearray(b"\x00" * ROM_SIZE)
    rom[FREE_RUN_START:FREE_RUN_START + FREE_RUN_SIZE] = b"\xff" * FREE_RUN_SIZE
    fragment = TextEncoder.encode_pokemon("Texte voisin débordé")
    rom[CT112_DESCRIPTION_OFFSET:CT112_DESCRIPTION_OFFSET + len(fragment)] = fragment
    _put_item(rom, CT112_INDEX, "CT112", CT112_DESCRIPTION_OFFSET)

    stats = mod.apply(
        rom,
        {CT112_DESCRIPTION_OFFSET: "Canonique mais non utilisé"},
        source=bytes(rom) if use_source else None,
    )

    base = mod.ITEM_TABLE_BASE + CT112_INDEX * mod.ITEM_STRIDE
    live_pointer = struct.unpack_from("<I", rom, base + mod.DESC_PTR_OFFSET)[0]
    assert stats["machines"] == 1
    assert stats["relocated"] == 0
    assert stats["skipped_protected"] == 1
    assert stats["failed"] == 0
    assert live_pointer == CT112_DESCRIPTION_OFFSET + mod.ROM_POINTER_BASE
    assert rom[FREE_RUN_START:FREE_RUN_START + FREE_RUN_SIZE] == (
        b"\xff" * FREE_RUN_SIZE
    )


def test_relocated_description_is_reflowed_from_source_pointer() -> None:
    from src.core.pokedex import line_width

    rom = bytearray(b"\x00" * ROM_SIZE)
    rom[FREE_RUN_START:FREE_RUN_START + FREE_RUN_SIZE] = b"\xff" * FREE_RUN_SIZE
    _put_item(rom, CT108_INDEX, "CT108", CT108_DESCRIPTION_OFFSET)
    source = bytes(rom)
    _put_item(rom, CT108_INDEX, "CT108", 0x500000)
    text = "Une attaque de base. Elle peut être utilisée pour abattre des arbres minces et de l'herbe."

    stats = mod.apply(rom, {CT108_DESCRIPTION_OFFSET: text}, source=source)

    _, result = _decode_live_description(rom, CT108_INDEX)
    assert ' '.join(result.split()) == text
    assert len(result.splitlines()) <= 4
    assert all(line_width(line) <= 144 for line in result.splitlines())
    assert stats['relocated'] == 1
    before = bytes(rom)
    assert mod.apply(rom, {CT108_DESCRIPTION_OFFSET: text}, source=source)['relocated'] == 0
    assert bytes(rom) == before


def test_curated_tm_descriptions_fit_the_case_window() -> None:
    import json

    from src.core.pokedex import wrap_lines

    overrides = json.loads(
        (mod.DEFAULT_COMBINED.parent / 'data/tm_item_descriptions_fr.json').read_text()
    )

    assert len(overrides) == 8
    for item, text in overrides.items():
        assert wrap_lines(text, 4, 144) is not None, (item, text)


def test_overlong_description_is_rejected_without_truncation() -> None:
    rom = bytearray(b"\x00" * ROM_SIZE)
    rom[FREE_RUN_START:FREE_RUN_START + FREE_RUN_SIZE] = b"\xff" * FREE_RUN_SIZE
    _put_item(rom, CT108_INDEX, "CT108", CT108_DESCRIPTION_OFFSET)
    original = bytes(rom)

    stats = mod.apply(rom, {CT108_DESCRIPTION_OFFSET: 'Très longue description ' * 30}, source=original)

    assert stats['failed'] == 1
    assert bytes(rom) == original
