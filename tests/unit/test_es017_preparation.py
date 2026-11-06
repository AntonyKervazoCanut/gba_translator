"""Gardes du relevé ES-017 ; aucune certification de traduction implicite."""
import json
from pathlib import Path

from scripts.audit_es016_preparation import snapshot

ROOT = Path(__file__).resolve().parents[2]


def test_es017_exact_contract_and_binary_preimages():
    lots = json.loads((ROOT / 'docs/analysis/es/lots.json').read_text())
    report = json.loads((ROOT / 'docs/analysis/es/017_PREPARATION.json').read_text())
    keys = next(lot['offsets'] for lot in lots if lot['id'] == 'ES-017')

    assert [row['offset'] for row in report['entries']] == keys
    assert len(set(keys)) == report['summary']['entries'] == 393
    assert report['summary']['inventory_states'] == {'identique_en': 355, 'different_en': 38}
    for row in report['entries']:
        image = row['english_snapshot']
        assert snapshot(bytes.fromhex(image['raw_hex']), 0) == image
        assert row['inventory']['offset'] == row['offset']
        assert row['zone'] is None
        assert not row['injection_certified']
        for ref in row['direct_references']:
            raw = bytes.fromhex(ref['context_hex'])
            assert int.from_bytes(raw[4:8], 'little') == int(row['offset'], 16) + 0x08000000


def test_es017_prefixes_duplicates_and_missing_routes():
    report = json.loads((ROOT / 'docs/analysis/es/017_PREPARATION.json').read_text())
    routes = json.loads((ROOT / 'docs/analysis/es/017_ROUTES.json').read_text())['routes']
    probe = json.loads((ROOT / 'docs/analysis/es/017_ACHEMINEMENT_REPRO.json').read_text())
    rows = {row['offset']: row for row in report['entries']}

    assert len(routes) == 25
    assert {r['contract_offset'] for r in routes if r['in_same_lot']} == {
        '0x007A3FD3', '0x007A4072', '0x007A7308', '0x007A7E6A',
        '0x007AAB5E', '0x007B4787'}
    assert {r['contract_offset'] for r in probe['entries']} == {
        r['contract_offset'] for r in routes if not r['in_same_lot']}
    assert len(probe['entries']) == 19
    assert all(not r['json_entries'] and not r['resolved_live'] for r in probe['entries'])
    for route in routes:
        row = rows[route['contract_offset']]
        assert not row['direct_references'] and not row['alias_configured']
        assert route['prefix_hex'] == 'aa'
        assert int(route['offset'], 16) == int(route['contract_offset'], 16) + 1
        assert route['prefix_hex'] + route['snapshot']['raw_hex'] == row['english_snapshot']['raw_hex']
        assert route['references']


def test_es017_reconstructs_long_sources_and_stale_french_inventory():
    report = json.loads((ROOT / 'docs/analysis/es/017_PREPARATION.json').read_text())
    rows = {row['offset']: row for row in report['entries']}

    assert rows['0x007A9A75']['english_snapshot']['bytes_including_ff'] == 1047
    assert rows['0x007AAECA']['english_snapshot']['bytes_including_ff'] == 648
    assert rows['0x007B3C6A']['english_snapshot']['decoded_control_aware'].startswith(
        'An item to be held by a Pokémon.')
    assert 'HP on each hit' in rows['0x007B3C6A']['english_snapshot']['decoded_control_aware']
    assert rows['0x007B3C6A']['inventory']['en'].startswith('Un spray')
    assert rows['0x007B3EB0']['english_snapshot']['decoded_control_aware'].startswith(
        'A unique Poké Ball')
