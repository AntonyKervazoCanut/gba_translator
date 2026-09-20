"""#191 : textes réellement référencés par les scripts du PC du Prof. Log."""

import struct
from pathlib import Path

import pytest

from src.core.text_codec import TextEncoder


@pytest.mark.rom
@pytest.mark.parametrize(
    "slot,source,text",
    [
        (0x1A6A88, 0x1A5BC6,
         "Connexion au PC du Prof. Log...<0xFB>Évaluation du Pokédex..."),
        (0x1A740E, 0x1A6CA3,
         "Voici ton bilan Pokédex :<0xFB><0xFD><0x02> Pokémon vus et\n"
         "<0xFD><0x03> Pokémon capturés.<0xFB><0xFC><0x06><0x02>Avis du Prof. Log :"),
    ],
)
def test_prof_log_live_text(slot: int, source: int, text: str) -> None:
    original = Path("input/roms/englishrom.gba").read_bytes()
    built = Path("output/roms/GenedRom-fr.gba").read_bytes()
    assert struct.unpack_from("<I", original, slot)[0] == 0x08000000 + source
    target = struct.unpack_from("<I", built, slot)[0] - 0x08000000
    assert 0 <= target < len(built)
    actual = built[target:built.index(b"\xff", target) + 1]
    assert actual == TextEncoder.encode_pokemon(text)
    # Le scanner incluait auparavant cet octet de script dans le texte.
    assert built[source - 1] == original[source - 1] == 0xAA
