"""Gardes du relevé technique ES-016, sans prétendre certifier une traduction."""
import json
from pathlib import Path

from scripts.audit_es016_preparation import snapshot

ROOT = Path(__file__).resolve().parents[2]


def test_snapshot_consumes_command_arguments_before_terminator():
    raw = bytes.fromhex('fc04ff0102fdfffa fb bbff')

    result = snapshot(raw, 0)

    assert result['raw_hex'] == raw.hex()
    assert result['bytes_including_ff'] == len(raw)
    assert [c['hex'] for c in result['commands']] == ['fc04ff0102', 'fdff', 'fa', 'fb']
    assert result['decoded_control_aware'].endswith('A')


def test_es016_report_has_exact_ordered_contract_and_replayable_preimages():
    lots = json.loads((ROOT / 'docs/analysis/es/lots.json').read_text())
    report = json.loads((ROOT / 'docs/analysis/es/016_PREPARATION.json').read_text())
    contract = next(lot['offsets'] for lot in lots if lot['id'] == 'ES-016')

    assert [row['offset'] for row in report['entries']] == contract
    assert len(set(contract)) == report['summary']['entries'] == 393
    assert report['summary']['inventory_states'] == {
        'identique_en': 359, 'different_en': 31, 'absent_es': 3}
    for row in report['entries']:
        image = row['english_snapshot']
        assert snapshot(bytes.fromhex(image['raw_hex']), 0) == image
        assert row['inventory']['offset'] == row['offset']
        assert row['zone'] is None
        assert not row['injection_certified']
        assert all(ref['references'] for ref in row['interior_references'])
        for ref in row['direct_references']:
            context = bytes.fromhex(ref['context_hex'])
            assert int.from_bytes(context[4:8], 'little') == int(row['offset'], 16) + 0x08000000


def test_es016_routes_keep_prefixes_and_identify_contractual_duplicates():
    report = json.loads((ROOT / 'docs/analysis/es/016_PREPARATION.json').read_text())
    routes = json.loads((ROOT / 'docs/analysis/es/016_ROUTES.json').read_text())['routes']
    rows = {row['offset']: row for row in report['entries']}

    assert len(routes) == 10
    assert {r['contract_offset'] for r in routes if r['in_same_lot']} == {
        '0x007808DD', '0x00788537', '0x0078D43D'}
    for route in routes:
        row = rows[route['contract_offset']]
        assert not row['direct_references']
        assert not row['alias_configured']
        assert route['prefix_hex'] == 'aa'
        assert int(route['offset'], 16) == int(route['contract_offset'], 16) + 1
        assert route['prefix_hex'] + route['snapshot']['raw_hex'] == row['english_snapshot']['raw_hex']
        assert route['references']
        if route['in_same_lot']:
            assert route['snapshot'] == rows[route['offset']]['english_snapshot']
