"""Protège les preuves figées de B-684, sans figer les oublis dans le jeu."""

import hashlib
import json
from collections import Counter
from pathlib import Path

from src.core.dialogue_linewrap import GLYPH_WIDTHS
from src.core.text_codec import GERMAN_UMLAUT_CHARS, TextEncoder
from src.text.charmap_data import BYTE_TO_CHAR

REPORT = json.loads(
    (Path(__file__).resolve().parents[3] / "docs/analysis/684_OBJETS_02_DE.json")
    .read_text(encoding="utf-8")
)


def test_exclusive_ticket_scope_is_complete() -> None:
    """Aucun oubli, doublon ni offset étranger dans les décisions du lot."""
    rows = REPORT["records"]
    scope = [row["offset"] for row in rows]

    assert len(scope) == len(set(scope)) == 300
    assert hashlib.sha256("\n".join(scope).encode()).hexdigest() == (
        "02129c1396fecf2f0af3a94414870c9aaac53e295ffe65f969213161559b5318"
    )
    assert Counter(row["decision"] for row in rows) == {
        "terme_legitime": 95, "deja_patche": 101, "patch_separe": 104,
    }


def test_binary_evidence_matches_names_and_cell_budgets() -> None:
    """Les cellules réellement relevées décodent les noms annoncés sans contrôle."""
    for row in REPORT["records"]:
        assert int(row["offset"], 16) == 0x876200 + 44 * row["item_index"]
        for lang in ("en", "de"):
            cell = bytes.fromhex(row[f"{lang}_cell_hex"])
            assert len(cell) == 14 and 0xFF in cell
            name = cell[:cell.index(0xFF)]
            assert not set(name).intersection(range(0xF7, 0xFF))
            assert "".join(BYTE_TO_CHAR[b] for b in name) == row[f"{lang}_rom"]
            if lang == "de":
                assert len(name) + 1 == row["de_bytes_with_terminator"]
                assert sum(GLYPH_WIDTHS[b] for b in name) == row["de_normal_font_pixels"]
                assert row["de_normal_font_pixels"] <= 74
        assert row["combined_en"] == row["en_rom"]
        assert row["combined_de"] is None and row["combined_fr"] is None
        assert not row["in_extraction"] and not row["in_translation_ready"]
        assert row["metadata_except_description_unchanged"]
        assert not row["name_controls"] and not row["name_placeholders"]
        for lang in ("en", "de"):
            assert 0 <= int(row[f"{lang}_description_target"], 16) < 0x2000000


def test_separate_patch_decisions_do_not_claim_corrections() -> None:
    """Distingue les preuves actuelles des propositions encore non injectées."""
    oversized = []
    for row in REPORT["records"]:
        proposal = TextEncoder.encode_pokemon(
            row["proposed_de"], skip_aliases=GERMAN_UMLAUT_CHARS,
        )
        assert len(proposal) == row["proposed_bytes_with_terminator"]
        assert (len(proposal) <= 14) == row["proposed_fits_14_bytes"]
        assert row["reason"] and row["register_gender_scene"]
        if row["decision"] == "patch_separe":
            assert row["de_rom"] != row["proposed_de"]
        else:
            assert row["de_rom"] == row["proposed_de"]
        if len(proposal) > 14:
            oversized.append(row["proposed_de"])
    assert oversized == [
        "Ultranecronium Z", "Aerodactylonit", "Illumina-Galette",
        "Feldbeschichtung", "Silberkronkorken", "Purpurner Nektar",
    ]
