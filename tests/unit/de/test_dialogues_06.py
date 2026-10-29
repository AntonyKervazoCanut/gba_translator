"""B-678 : qualification du lot et contrôles des pointeurs après build DE."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.apply_inline_overrides_fr import (
    _apply_control_placeholders,
    _extract_control_sequences_from_raw,
    _load_combined,
    _normalize_text,
    _read_raw_entry,
)
from src.core.dialogue_linewrap import line_widths, rewrap
from src.core.text_codec import GERMAN_UMLAUT_CHARS, TextEncoder

ROOT = Path(__file__).resolve().parents[3]
REPORT = ROOT / "docs/analysis/678_DIALOGUES_06_DE.json"


def test_decisions_exhaustives_et_absences_binaires() -> None:
    """Les 300 décisions restent distinctes et les assets ne sont pas traduits."""
    rows = json.loads(REPORT.read_text())
    combined, _ = _load_combined(ROOT / "languages/de/combined_de.txt")

    assert len(rows) == len({row["offset"] for row in rows}) == 300
    fragments = [row for row in rows if row["decision"] == "fragment non vivant"]
    assert len(fragments) == 272
    for row in fragments:
        assert int(row["offset"], 16) not in combined
        assert row["pointeurs_en"] == []


@pytest.mark.rom
def test_dialogues_06_pointeurs_octets_commandes_et_boites() -> None:
    """Compare les 28 cibles vivantes aux sources et aux commandes EN complètes."""
    rows = json.loads(REPORT.read_text())
    english = (ROOT / "input/roms/englishrom.gba").read_bytes()
    german = (ROOT / "output/roms/GenedRom-de.gba").read_bytes()
    combined, _ = _load_combined(ROOT / "languages/de/combined_de.txt")

    for row in rows:
        offset = int(row["offset"], 16)
        if not row["pointeurs_en"]:
            continue
        original = _read_raw_entry(english, offset, "pokemon")
        assert original is not None
        raw = bytes.fromhex(original["raw_bytes"])
        expected = raw
        if offset in combined:
            text = _apply_control_placeholders(
                _normalize_text(combined[offset]), original["text"], original["raw_bytes"]
            )
            # Les messages courts à simple FE conservent leurs lignes ;
            # les boîtes défilantes FA/FB passent par le repli du build.
            if b"\xfa" in raw or b"\xfb" in raw:
                text = rewrap(text)
            assert "{" not in text, row["offset"]
            assert max(line_widths(text)) <= 192, row["offset"]
            expected = TextEncoder.encode_pokemon(text, skip_aliases=GERMAN_UMLAUT_CHARS)
        for pointer in row["pointeurs_en"]:
            site = int(pointer, 16)
            assert int.from_bytes(english[site:site + 4], "little") == offset + 0x08000000
            target = int.from_bytes(german[site:site + 4], "little") - 0x08000000
            assert 0 <= target < len(german), row["offset"]
            actual = _read_raw_entry(german, target, "pokemon")
            assert actual is not None, row["offset"]
            actual_bytes = bytes.fromhex(actual["raw_bytes"])
            assert actual_bytes == expected, (row["offset"], pointer, actual["text"])
            commands = lambda b: [  # FA/FB changent avec le repli des lignes.
                seq for seq in _extract_control_sequences_from_raw(b)
                if seq[0] not in (0xFA, 0xFB)
            ]
            assert commands(actual_bytes) == commands(raw), row["offset"]
            assert actual_bytes.count(b"\xfb") == raw.count(b"\xfb"), row["offset"]
