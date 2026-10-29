"""Vérifie la partition figée publiée par l’audit ES A-663."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import pytest

from src.core.fixed_tables import FIXED_TABLE_RANGES

AUDIT_DIR = Path(__file__).resolve().parents[2] / "docs/analysis/es"


@pytest.fixture(scope="module")
def inventory():
    with (AUDIT_DIR / "inventaire.csv").open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_batches_cover_every_candidate_once_and_exclude_font_bytes(inventory):
    batches = json.loads((AUDIT_DIR / "lots.json").read_text(encoding="utf-8"))
    offsets = [offset for batch in batches for offset in batch["offsets"]]
    candidates = {row["offset"] for row in inventory if row["lot"]}
    font_start, font_end, _ = next(
        entry for entry in FIXED_TABLE_RANGES if "font" in entry[2]
    )
    excluded = {row["offset"] for row in inventory if not row["lot"]}

    assert len(offsets) == len(set(offsets)) == 24158
    assert set(offsets) == candidates
    assert len(excluded) == 23
    assert all(font_start <= int(offset, 16) < font_end for offset in excluded)
    assert not any(font_start <= int(offset, 16) < font_end for offset in offsets)
    assert all(150 <= batch["count"] == len(batch["offsets"]) <= 400 for batch in batches)
    for batch in batches:
        rows = [row for row in inventory if row["lot"] == batch["id"]]
        assert [row["offset"] for row in rows] == batch["offsets"]
        assert dict(Counter(row["etat"] for row in rows)) == batch["states"]


def test_inventory_has_unique_offsets_and_tracks_the_audited_gaps(inventory):
    metrics = json.loads((AUDIT_DIR / "mesures.json").read_text(encoding="utf-8"))
    offsets = [row["offset"] for row in inventory]
    missing = {row["offset"] for row in inventory if row["etat"] == "absent_es"}

    assert len(offsets) == len(set(offsets)) == 24181
    assert missing == set(metrics["fr_absent_es"])
    assert len(missing) == 308
    assert dict(Counter(row["etat"] for row in inventory)) == metrics["etats"]


def test_frozen_inventory_and_batches_match_their_published_hashes():
    metrics = json.loads((AUDIT_DIR / "mesures.json").read_text(encoding="utf-8"))

    for name, expected in metrics["artefacts"].items():
        assert hashlib.sha256((AUDIT_DIR / name).read_bytes()).hexdigest() == expected
