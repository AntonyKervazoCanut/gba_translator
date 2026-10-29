"""Contrôles de complétude du relevé limité au ticket B-683."""

import hashlib
import json
from collections import Counter
from pathlib import Path

import pytest

from languages.de.patches.item_names import decode_name, encode

ROOT = Path(__file__).resolve().parents[3]
REPORT = json.loads((ROOT / 'docs/analysis/683_OBJETS_01_DE.json').read_text())
ENTRIES = REPORT['entries']


def test_objets_01_scope_matches_the_exclusive_ticket_list() -> None:
    """Une omission, un doublon ou un offset étranger invalide le relevé."""
    offsets = [row['offset'] for row in ENTRIES]
    digest = hashlib.sha256('\n'.join(offsets).encode()).hexdigest()

    assert len(offsets) == len(set(offsets)) == 300
    assert digest == '11b21f63a2d5291d9a8e54c9826ce65832682ab663d3aeafa90dbe766e1ecd2b'
    assert dict(Counter(row['decision'] for row in ENTRIES)) == {
        'déjà patché': 145,
        'terme légitime': 33,
        'patch séparé requis': 122,
    }


@pytest.mark.parametrize('row', ENTRIES, ids=lambda row: row['offset'])
def test_objets_01_records_bounded_live_cells_without_claiming_missing_fixes(row: dict) -> None:
    """Le rapport distingue les octets observés des traductions proposées."""
    offset = int(row['offset'], 16)
    raw = bytes.fromhex(row['octets_de'])

    assert offset == 0x876200 + row['table_index'] * 44
    assert row['corpus_en']['text']
    assert row['corpus_de'] is None and row['corpus_fr'] is None
    assert len(raw) == 14
    assert row['octets_avec_terminateur'] == raw.index(0xFF) + 1 <= 14
    assert decode_name(raw, 0) == row['rom_de']
    assert encode(row['rom_de']) + b'\xff' == raw[:raw.index(0xFF) + 1]
    assert not any(byte in range(0xF7, 0xFF) for byte in raw[:raw.index(0xFF)])
    assert row['controles'] == row['placeholders'] == []
    assert row['motif'] and row['acces_vivant'] and row['cible_de']
    if row['decision'] == 'patch séparé requis':
        assert row['cible_de'] != row['rom_de']
    else:
        assert row['cible_de'] == row['rom_de']


def test_hard_stone_is_reported_as_a_patch_defect_and_not_a_valid_german_name() -> None:
    row = next(row for row in ENTRIES if row['offset'] == '0x878510')

    assert row['rom_de'] == 'Harter Stein'
    assert row['cible_de'] == 'Granitstein'
    assert row['decision'] == 'patch séparé requis'
