"""Contrat du relevé ES-015 ; ne certifie aucune traduction en jeu."""
import json
from pathlib import Path

from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw

ROOT = Path(__file__).resolve().parents[2]


def test_es015_preparation_keeps_contract_and_complete_commands():
    lots = json.loads((ROOT / 'docs/analysis/es/lots.json').read_text())
    report = json.loads((ROOT / 'docs/analysis/es/015_PREPARATION.json').read_text())
    lot = next(row for row in lots if row['id'] == 'ES-015')

    assert [row['offset'] for row in report['entries']] == lot['offsets']
    assert len(set(lot['offsets'])) == 393
    assert report['summary']['entries'] == 393
    for row in report['entries']:
        source = row['english_snapshot']
        raw = bytes.fromhex(source['raw_hex'])
        commands = [bytes.fromhex(c['hex']) for c in source['commands']]
        assert raw.endswith(b'\xff')
        assert len(raw) == source['bytes_including_ff']
        assert commands == [bytes(c) for c in _extract_control_sequences_from_raw(raw)]
        for command in source['commands']:
            start = command['relative_offset']
            code = bytes.fromhex(command['hex'])
            assert raw[start:start + len(code)] == code
        assert row['inventory']['offset'] == row['offset']
        assert row['inventory']['lot'] == 'ES-015'
        assert row['zone'] is None
        assert row['translation_status'].startswith('non traité')


def test_es015_routes_preserve_prefixes_and_duplicate_contracts():
    report = json.loads((ROOT / 'docs/analysis/es/015_PREPARATION.json').read_text())
    routes = json.loads((ROOT / 'docs/analysis/es/015_ROUTES.json').read_text())
    rows = {row['offset']: row for row in report['entries']}

    assert len(routes['routes']) == 11
    assert {r['contract_offset'] for r in routes['routes'] if r['in_same_lot']} == {
        '0x00721437', '0x0074BF85',
    }
    for route in routes['routes']:
        row = rows[route['contract_offset']]
        assert not row['direct_references']
        assert int(route['offset'], 16) == int(route['contract_offset'], 16) + 1
        assert route['prefix_hex'] in ('00', '20', 'aa')
        assert route['prefix_hex'] + route['snapshot']['raw_hex'] == row['english_snapshot']['raw_hex']
        assert route['references']
        assert route in [{'contract_offset': row['offset'], **c} for c in row['nearby_candidates']]
        if route['in_same_lot']:
            assert route['snapshot'] == rows[route['offset']]['english_snapshot']


def test_es015_dangerous_script_keys_remain_unqualified():
    report = json.loads((ROOT / 'docs/analysis/es/015_PREPARATION.json').read_text())
    rows = {row['offset']: row for row in report['entries']}

    assert not rows['0x00721340']['direct_references']
    assert rows['0x0072134C']['english_snapshot']['decoded_control_aware'] == 'Parent and child attack together.'
    assert not rows['0x0072134C']['direct_references']
    assert rows['0x0074037D']['english_snapshot']['raw_hex'].startswith('11fe')
    assert rows['0x00745132']['english_snapshot']['raw_hex'].startswith('0f00ca567c08090602')
    assert {r['offset'] for r in rows['0x00741625']['interior_references']} == {
        '0x00741693', '0x007416B5', '0x007416D6',
    }
