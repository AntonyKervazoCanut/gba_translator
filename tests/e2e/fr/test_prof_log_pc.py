"""#191/#192 : textes réellement référencés par les scripts du PC du Prof. Log."""

import struct
from functools import lru_cache
from pathlib import Path

import pytest

from src.core.bps import apply_bps_patch
from src.core.text_codec import TextEncoder

ENGLISH_ROM = Path("input/roms/englishrom.gba")
BUILT_ROM = Path("output/roms/GenedRom-fr.gba")
FR_PATCH = Path("patches/pokemon_unbound_fr.bps")

LIVE_TEXTS = [
    (0x1A6A88, 0x1A5BC6,
     "Connexion au PC du Prof. Log...<0xFB>Évaluation du Pokédex..."),
    (0x1A740E, 0x1A6CA3,
     "Voici ton bilan Pokédex :<0xFB><0xFD><0x02> Pokémon vus et\n"
     "<0xFD><0x03> Pokémon capturés.<0xFB><0xFC><0x06><0x02>Avis du Prof. Log :"),
]


@lru_cache(maxsize=1)
def _released_rom() -> bytes:
    """ROM obtenue par le joueur : patch FR suivi appliqué à la ROM anglaise."""
    return apply_bps_patch(ENGLISH_ROM.read_bytes(), FR_PATCH.read_bytes())


def _assert_live_text(built: bytes, slot: int, source: int, text: str) -> None:
    original = ENGLISH_ROM.read_bytes()
    assert struct.unpack_from("<I", original, slot)[0] == 0x08000000 + source
    target = struct.unpack_from("<I", built, slot)[0] - 0x08000000
    assert 0 <= target < len(built)
    actual = built[target:built.index(b"\xff", target) + 1]
    assert actual == TextEncoder.encode_pokemon(text)
    # Le scanner incluait auparavant cet octet de script dans le texte.
    assert built[source - 1] == original[source - 1] == 0xAA


@pytest.mark.rom
@pytest.mark.parametrize("slot,source,text", LIVE_TEXTS)
def test_prof_log_live_text(slot: int, source: int, text: str) -> None:
    _assert_live_text(BUILT_ROM.read_bytes(), slot, source, text)


@pytest.mark.rom
@pytest.mark.parametrize("slot,source,text", LIVE_TEXTS)
def test_prof_log_live_text_in_released_patch(
    slot: int, source: int, text: str
) -> None:
    """#192 : le patch publié ne doit plus afficher la connexion en anglais."""
    _assert_live_text(_released_rom(), slot, source, text)
