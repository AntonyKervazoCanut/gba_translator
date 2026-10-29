"""Garde les lacunes ES auditées sans autoriser de nouvelles pertes.

A-663 fige les 308 absences connues dans son inventaire. Une simple limite
numérique masquerait une nouvelle perte compensée par une autre correction.
La référence communautaire reste immuable ; la cible maintenue sera es-maint.
"""

import json
from pathlib import Path

import pytest

AUDIT_PATH = Path(__file__).resolve().parents[3] / "docs/analysis/es/mesures.json"
MAX_EXTRA_IN_ES = 25
MIN_ES_ENTRIES = 20000


class TestExtractionCoverage:
    def test_es_has_a_meaningful_number_of_entries(self, es_combined_entries):
        assert len(es_combined_entries) >= MIN_ES_ENTRIES, (
            f"combined_es.txt only has {len(es_combined_entries)} entries — "
            f"expected at least {MIN_ES_ENTRIES}"
        )

    def test_es_coverage_close_to_fr_offsets(
        self, es_combined_entries, fr_combined_entries
    ):
        missing = set(fr_combined_entries) - set(es_combined_entries)
        audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
        known_missing = {int(offset, 16) for offset in audit["fr_absent_es"]}
        unexpected = missing - known_missing
        assert not unexpected, (
            "Nouvelles absences FR→ES non auditées : "
            f"{', '.join(hex(offset) for offset in sorted(unexpected))}. "
            "Examiner les offsets et actualiser l'audit explicitement ; "
            "ne jamais régénérer combined_es.txt pour masquer cette dérive."
        )

    def test_new_gap_is_rejected_even_when_an_old_gap_is_filled(
        self, es_combined_entries, fr_combined_entries
    ):
        reference = dict(es_combined_entries)
        old_gap = next(iter(set(fr_combined_entries) - set(reference)))
        new_gap = next(iter(set(fr_combined_entries) & set(reference)))
        reference[old_gap] = fr_combined_entries[old_gap]
        del reference[new_gap]

        with pytest.raises(AssertionError, match="Nouvelles absences"):
            self.test_es_coverage_close_to_fr_offsets(reference, fr_combined_entries)

    def test_es_has_few_offsets_absent_from_fr(
        self, es_combined_entries, fr_combined_entries
    ):
        extra = set(es_combined_entries) - set(fr_combined_entries)
        assert len(extra) <= MAX_EXTRA_IN_ES, (
            f"{len(extra)} combined_es.txt offsets are not present in "
            f"combined_fr.txt (baseline ~2, threshold {MAX_EXTRA_IN_ES})"
        )
