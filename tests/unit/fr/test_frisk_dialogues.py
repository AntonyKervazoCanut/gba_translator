"""Les cinq gestes de fouille restent traduits, y compris après relocation (#214)."""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
OFFSETS = (0x7939BC, 0x1EEE606, 0x1EF8247, 0x1F07621, 0x1F7D406)


@pytest.mark.parametrize("offset", OFFSETS)
def test_search_gesture_is_french(offset: int) -> None:
    """La dernière valeur de chaque dialogue utilise la même onomatopée."""
    entries = {}
    for line in (ROOT / "languages/fr/combined_fr.txt").read_text().splitlines():
        if line.startswith("0x") and ": " in line:
            address, text = line.split(": ", 1)
            entries[int(address, 16)] = text

    text = entries[offset]

    assert text.endswith(r"\p×Fouille× ×Fouille×")
    assert "Frisk" not in text
