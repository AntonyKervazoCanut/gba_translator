"""Vérifie que les lots publiés couvrent le corpus hindi sans chevauchement."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]


def test_indie_audit_batches_cover_every_non_seed_english_offset() -> None:
    """Les tickets doivent partager exactement les offsets EN restant à traduire."""
    # Arrange
    source = (ROOT / "languages/en/combined_en.txt").read_text(encoding="utf-8")
    offsets = {
        int(match.group(1), 16)
        for match in re.finditer(r"^\s*(0x[0-9a-fA-F]+):", source, re.MULTILINE)
    }
    seeds = {0x1773FD, 0x177489, 0x183509}
    audit = (ROOT / "docs/analysis/audit_langue_indie.md").read_text(encoding="utf-8")
    rows = re.findall(
        r"\| HI-(\d+) \| `(0x[0-9A-F]+)` \| `(0x[0-9A-F]+)` \| (\d+) \|",
        audit,
    )

    # Act
    covered = set()
    previous_end = -1
    for index, (number, first, last, count) in enumerate(rows, start=1):
        start, end = int(first, 16), int(last, 16)
        selected = {offset for offset in offsets - seeds if start <= offset <= end}

        # Assert
        assert int(number) == index
        assert previous_end < start <= end
        assert 150 <= len(selected) == int(count) <= 400
        assert not covered.intersection(selected)
        covered.update(selected)
        previous_end = end

    assert rows, "Aucun lot de traduction dans l'audit"
    assert covered == offsets - seeds
