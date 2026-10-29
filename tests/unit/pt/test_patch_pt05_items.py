"""PT-05 : patch atomique testé sur les vrais extraits EN, sans mock ROM."""
from pathlib import Path

import pytest

from languages.pt.patches.pt05_items import COMBINED, apply_patches
from scripts.apply_combined_fr import _load_combined
from src.core.text_codec import TextEncoder

FIXTURES = Path(__file__).resolve().parents[1] / 'fixtures/pt05'


@pytest.fixture
def rom() -> bytearray:
    data = bytearray(0x87A000)
    for name, at in [('descriptions', 0x3D4F26), ('items', 0x876200), ('reader', 0x9A96C)]:
        raw = (FIXTURES / f'{name}.bin').read_bytes()
        data[at:at + len(raw)] = raw
    return data


def test_real_cells_patch_idempotently_and_preserve_pointers(rom: bytearray) -> None:
    original = bytes(rom)
    assert apply_patches(rom) == 180
    assert apply_patches(rom) == 0
    assert rom[:0x3D4F26] == original[:0x3D4F26]
    assert rom[0x3D93C9:] == original[0x3D93C9:]
    text, _ = _load_combined(COMBINED)
    expected = TextEncoder.encode_pokemon(text[0x3D52B2], strict=True)
    assert rom[0x3D52B2:0x3D52B2 + len(expected)] == expected


@pytest.mark.parametrize('bad_address', [0x9A98C, 0x879394, 0x3D936F])
def test_rejects_unknown_reader_pointer_or_preimage_atomically(
    rom: bytearray, bad_address: int,
) -> None:
    rom[bad_address] ^= 0x80
    before = bytes(rom)
    with pytest.raises(ValueError):
        apply_patches(rom)
    assert rom == before


def test_overflow_is_rejected_before_any_write(rom: bytearray) -> None:
    translations, _ = _load_combined(COMBINED)
    translations[0x3D936F] = 'X' * 200
    before = bytes(rom)
    with pytest.raises(ValueError, match='Budget/structure'):
        apply_patches(rom, translations)
    assert rom == before


def test_known_builder_rewrap_is_restored(rom: bytearray) -> None:
    translations, _ = _load_combined(COMBINED)
    expected = TextEncoder.encode_pokemon(translations[0x3D52B2], strict=True)
    intermediate = expected.replace(b'\xfe', b'\x00')
    rom[0x3D52B2:0x3D52B2 + len(intermediate)] = intermediate
    apply_patches(rom)
    assert rom[0x3D52B2:0x3D52B2 + len(expected)] == expected
