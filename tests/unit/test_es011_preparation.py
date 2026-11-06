"""Contrat des preuves de préparation ES-011, sans certification de traduction."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_es011_preparation_preserves_exact_selection_and_complete_preimages():
    lots = json.loads((ROOT / 'docs/analysis/es/lots.json').read_text())
    lot = next(row for row in lots if row['id'] == 'ES-011')
    report = json.loads((ROOT / 'docs/analysis/es/011_PREPARATION.json').read_text())

    assert [row['offset'] for row in report['entries']] == lot['offsets']
    assert len(set(lot['offsets'])) == 374
    for row in report['entries']:
        raw = bytes.fromhex(row['english_raw_hex'])
        assert len(raw) == row['encoded_size']
        assert raw.endswith(b'\xff')
        assert row['inventory']['lot'] == 'ES-011'
        assert row['inventory']['offset'] == row['offset']
        assert 'aucune injection' in row['decision']


def test_es011_alias_candidates_preserve_prefix_and_live_source():
    report = json.loads((ROOT / 'docs/analysis/es/011_PREPARATION.json').read_text())
    rows = {row['offset']: row for row in report['entries']}
    routes = json.loads((ROOT / 'docs/analysis/es/011_ROUTES.json').read_text())

    assert len(routes['aliases_candidates']) == 57
    for alias in routes['aliases_candidates']:
        row = rows[alias['contract_offset']]
        delta = int(alias['live_offset'], 16) - int(alias['contract_offset'], 16)
        assert 1 <= delta <= 3
        assert bytes.fromhex(alias['prefix_hex']) == bytes(delta)
        assert alias['prefix_hex'] + alias['english_raw_hex'] == row['english_raw_hex']
        assert not row['direct_pointer_occurrences']
        assert alias['pointer_offsets'] == row['nearby_live_candidates'][0]['pointer_offsets']
        assert alias['pointer_offsets']
