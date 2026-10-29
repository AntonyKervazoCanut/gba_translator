"""Préserver l'exhaustivité du plan d'audit IT figé, indépendamment des futurs fixes."""

import csv
import json
from pathlib import Path


AUDIT = Path(__file__).resolve().parents[3] / "docs" / "analysis"


def test_every_snapshot_offset_belongs_to_exactly_one_bounded_lot():
    """Aucun offset du snapshot ne peut être oublié ou traité par deux lots."""
    with (AUDIT / "audit_traduction_it_offsets.csv").open() as handle:
        rows = list(csv.DictReader(handle))
    lots = json.loads((AUDIT / "audit_traduction_it_lots.json").read_text())
    measures = json.loads((AUDIT / "audit_traduction_it_mesures.json").read_text())

    offsets = [offset for lot in lots for offset in lot["offsets"]]
    assignments = {row["offset"]: row["lot"] for row in rows}

    assert len(offsets) == len(set(offsets)) == measures["counts"]["rows"]
    assert set(offsets) == set(assignments)
    assert sum(row["etat"] == "manquant" for row in rows) == measures["counts"]["missing_fr"]
    assert sum(row["etat"] == "existant" for row in rows) == measures["counts"]["it"]
    for lot in lots:
        assert 0 < lot["nombre"] == len(lot["offsets"]) <= 350
        assert all(assignments[offset] == lot["lot"] for offset in lot["offsets"])


def test_every_reported_defect_is_owned_by_a_ticket_lot():
    """Les défauts linguistiques et techniques restent rattachés à un lot de fix."""
    with (AUDIT / "audit_traduction_it_alertes.csv").open() as handle:
        alerts = list(csv.DictReader(handle))
    plan = json.loads((AUDIT / "audit_traduction_it_tickets.json").read_text())
    lots = json.loads((AUDIT / "audit_traduction_it_lots.json").read_text())

    ticket_aliases = {ticket["alias"] for ticket in plan["tickets"]}
    owned = {offset for lot in lots if lot["lot"] in ticket_aliases for offset in lot["offsets"]}

    assert alerts
    assert {alert["offset"] for alert in alerts} <= owned
    assert all(lot["lot"] in ticket_aliases for lot in lots)


def test_required_dependencies_form_an_acyclic_complete_certification_gate():
    """Le plan ne permet ni cycle ni certification omettant un préalable."""
    plan = json.loads((AUDIT / "audit_traduction_it_tickets.json").read_text())
    tickets = {ticket["alias"]: ticket for ticket in plan["tickets"]}

    def visit(alias, ancestors):
        assert alias not in ancestors
        for dependency in tickets[alias]["dependsOnAliases"]:
            assert dependency in tickets
            visit(dependency, ancestors | {alias})

    for alias in tickets:
        visit(alias, set())

    assert set(tickets["CERTIFICATION"]["dependsOnAliases"]) == tickets.keys() - {"CERTIFICATION"}
    for alias, ticket in tickets.items():
        if alias.startswith(("IT-", "DATA-")):
            assert {"GLOSSAIRE", "OUTILLAGE", "PARITE"} <= set(ticket["dependsOnAliases"])


def test_curated_data_keys_are_partitioned_without_duplicates():
    """Les cinq lots de curation restent disjoints et sous leur budget."""
    lots = json.loads((AUDIT / "audit_traduction_it_curation.json").read_text())

    for filename in {lot["fichier"] for lot in lots}:
        keys = [key for lot in lots if lot["fichier"] == filename for key in lot["cles"]]
        assert len(keys) == len(set(keys))
    assert sum(len(lot["cles"]) for lot in lots) == 903 + 653
    assert all(0 < len(lot["cles"]) <= 400 for lot in lots)


def test_every_planned_ticket_has_a_unique_created_card_and_resolved_dependencies():
    """Les cartes réelles couvrent le plan et les liens requis ne se perdent pas."""
    plan = json.loads((AUDIT / "audit_traduction_it_tickets.json").read_text())
    tickets = {ticket["alias"]: ticket for ticket in plan["tickets"]}

    assert plan["creation_verified"]
    assert len(tickets) == len({t["ticketId"] for t in tickets.values()}) == 98
    assert len({t["ticketLabel"] for t in tickets.values()}) == 98
    for ticket in tickets.values():
        assert ticket["requiredDependsOnTicketIds"] == [
            tickets[alias]["ticketId"] for alias in ticket["dependsOnAliases"]
        ]
    if not plan["structural_dependencies_applied"]:
        assert plan["dependency_blocker"] == tickets["RACCORDEMENT"]["ticketLabel"]
