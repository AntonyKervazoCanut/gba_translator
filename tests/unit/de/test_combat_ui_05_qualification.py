"""Garde l'exhaustivité et le périmètre du rapport combat_ui-05 (B-671)."""

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def test_combat_ui_05_qualifies_exactly_the_ticket_offsets() -> None:
    """Chaque offset exclusif du ticket possède une décision et une cible ROM."""
    # Arrange : empreinte de la liste du ticket, triée et encodée en uint32 LE.
    expected_digest = "66f9ac0350a6a8a33cb8f9c84373b4d38e4d56719f351f162a40ce981f37b56e"
    report = (ROOT / "docs/analysis/671_COMBAT_UI_05.md").read_text(encoding="utf-8")

    # Act
    rows = [line.split(" | ") for line in report.splitlines()
            if re.match(r"^\| 0x[0-9A-F]+ \|", line)]
    offsets = [int(row[0].removeprefix("| "), 16) for row in rows]
    digest = hashlib.sha256(
        b"".join(offset.to_bytes(4, "little") for offset in sorted(offsets))
    ).hexdigest()

    # Assert
    assert len(offsets) == len(set(offsets)) == 300
    assert digest == expected_digest
    corrected = []
    for offset, row in zip(offsets, rows):
        assert len(row) == 11
        assert row[4] not in ("", "∅", "vide")  # EN canonique ROM
        assert row[5] not in ("", "∅", "vide")  # DE final
        assert re.fullmatch(r"0x[0-9A-F]+(?: / 0x[0-9A-F]+)*", row[7])
        assert int(row[8]) > 0 and int(row[9]) > 0
        assert row[10].startswith(("Déjà patché", "Déjà correct", "Nom propre légitime",
                                   "Fragment non vivant", "Corrigé"))
        if row[10].startswith("Corrigé"):
            corrected.append(offset)
    assert corrected == [0xA438F0]
