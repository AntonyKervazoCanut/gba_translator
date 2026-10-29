"""B-679 : sources, commandes atomiques et pointeurs de dialogues-07."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

import pytest

from src.core.dialogue_linewrap import GLYPH_WIDTHS, VARIABLE_WIDTH, line_widths, rewrap
from src.core.text_codec import GERMAN_UMLAUT_CHARS, TextEncoder

ROOT = Path(__file__).resolve().parents[2]
ROWS = json.loads((ROOT / "docs/analysis/679_DIALOGUES_07_DE.json").read_text())
SPEC = importlib.util.spec_from_file_location(
    "dialogues07_builder",
    ROOT / "src/translators/19_build_translated_rom_generic.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
BUILDER = MODULE.TranslatedROMBuilder


def expanded(text: str) -> str:
    """Développe les retours sans toucher aux commandes brutes."""
    return text.replace(r"\n", "\n").replace(r"\l", "<0xFA>").replace(r"\p", "<0xFB>")


def encode(text: str) -> bytes:
    """Encode le profil allemand, umlauts compris."""
    return TextEncoder.encode_pokemon(expanded(text), skip_aliases=GERMAN_UMLAUT_CHARS)


def controls(data: bytes) -> list[list[int]]:
    """Réutilise les arités du moteur pour comparer les commandes ordonnées."""
    return [
        s
        for s in BUILDER._extract_control_sequences_from_raw(data)
        if s[0] not in (0xFA, 0xFB)
    ]


def without_wrap(data: bytes) -> bytes:
    """Neutralise uniquement les retours mécaniques FE/FA."""
    return re.sub(
        b"\x00+", b"\x00", data.replace(b"\xfe", b"\x00").replace(b"\xfa", b"\x00")
    )


def encoded_widths(raw):
    lines = [0]
    i = 0
    while i < len(raw):
        b = raw[i]
        if b == 255:
            break
        if b == 252:
            cmd = raw[i + 1]
            if cmd == 0x13:
                lines[-1] = max(lines[-1], raw[i + 2])
            i += 2 + BUILDER.FC_ARG_COUNTS.get(cmd, 0)
            continue
        if b in (247, 248, 249, 253):
            lines[-1] += VARIABLE_WIDTH if b == 253 else 12
            i += 2
            continue
        if b in (250, 251, 254):
            lines.append(0)
        else:
            lines[-1] += GLYPH_WIDTHS[b]
        i += 1
    return lines


def test_complete_exclusive_scope():
    offsets = [int(row["offset"], 16) for row in ROWS]
    assert len(offsets) == len(set(offsets)) == 300
    assert offsets[0] == 0x1EE6B5A and offsets[-1] == 0x1F2FDBE
    assert all(row["decision"] and row["motif"] and row["scene"] for row in ROWS)
    assert sum(row["decision"] == "corrigé" for row in ROWS) == 128
    assert sum(row["decision"] == "besoin de patch séparé" for row in ROWS) == 1


@pytest.fixture(scope="module")
def winning_texts():
    return {
        int(offset, 16): text
        for offset, text in re.findall(
            r"^(0x[0-9a-f]+): (.*)$",
            (ROOT / "languages/de/combined_de.txt").read_text(),
            re.MULTILINE | re.IGNORECASE,
        )
    }


@pytest.mark.parametrize("row", ROWS, ids=lambda row: row["offset"])
def test_winning_text_and_controls(row, winning_texts):
    assert winning_texts.get(int(row["offset"], 16)) == row["de"]
    if row["decision"] != "corrigé":
        return
    expected = bytes.fromhex(row["expected_hex"])
    original = bytes.fromhex(row["source_hex"])
    assert encode(row["de"]) == expected
    assert controls(expected) == controls(original)
    assert expected.count(b"\xfb") == original.count(b"\xfb")
    assert max(line_widths(expanded(row["de"]))) <= 192
    rendered = TextEncoder.encode_pokemon(
        rewrap(expanded(row["de"])),
        skip_aliases=GERMAN_UMLAUT_CHARS,
    )
    assert max(encoded_widths(rendered)) <= 192
    assert not re.search(r"\{[^}]*\}", row["de"])


@pytest.fixture(scope="module")
def rom_pair():
    source = (ROOT / "input/roms/englishrom.gba").read_bytes()
    assert hashlib.sha256(source).hexdigest() == ROWS[0]["canonical_sha256"]
    return source, (ROOT / "output/roms/GenedRom-de.gba").read_bytes()


@pytest.mark.rom
@pytest.mark.parametrize("row", ROWS, ids=lambda row: row["offset"])
def test_live_pointers_and_injected_bytes(row, rom_pair):
    source, built = rom_pair
    offset = int(row["offset"], 16)
    original = bytes.fromhex(row["source_hex"])
    assert source[offset : offset + len(original)] == original
    for site_hex in row["refs"]:
        site = int(site_hex, 16)
        assert int.from_bytes(source[site : site + 4], "little") == offset + 0x08000000
    if row["decision"] == "fragment non vivant":
        assert row["rom_checks"] == []
        return
    assert len(row["rom_checks"]) == len(row["refs"])
    for check in row["rom_checks"]:
        site = int(check["site"], 16)
        target = int.from_bytes(built[site : site + 4], "little") - 0x08000000
        expected = bytes.fromhex(check["expected_hex"])
        assert 0 <= target < len(built)
        assert built[target : target + len(expected)] == expected
        if row["decision"] == "corrigé":
            assert without_wrap(expected) == without_wrap(
                bytes.fromhex(row["expected_hex"])
            )
            assert controls(expected) == controls(original)
            assert max(encoded_widths(expected)) <= 192
