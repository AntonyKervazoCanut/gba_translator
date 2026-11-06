"""Gardes du relevé ES-019, sans certification des traductions."""
import json
from pathlib import Path

from scripts.audit_es016_preparation import snapshot

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / 'docs/analysis/es'


def test_exact_contract_and_binary_preimages():
    lots = json.loads((REPORTS / 'lots.json').read_text())
    report = json.loads((REPORTS / '019_PREPARATION.json').read_text())
    keys = next(lot['offsets'] for lot in lots if lot['id'] == 'ES-019')

    assert [row['offset'] for row in report['entries']] == keys
    assert len(set(keys)) == report['summary']['entries'] == 393
    assert report['summary']['inventory_states'] == {
        'identique_en': 385, 'different_en': 7, 'absent_es': 1}
    for row in report['entries']:
        image = row['english_snapshot']
        assert snapshot(bytes.fromhex(image['raw_hex']), 0) == image
        assert row['inventory']['offset'] == row['offset']
        assert row['zone'] is None
        assert not row['injection_certified']
        for ref in row['direct_references']:
            raw = bytes.fromhex(ref['context_hex'])
            assert int.from_bytes(raw[4:8], 'little') == int(row['offset'], 16) + 0x08000000


def test_unconfigured_prefixes_and_duplicate_keys():
    report = json.loads((REPORTS / '019_PREPARATION.json').read_text())
    routes = json.loads((REPORTS / '019_ROUTES.json').read_text())['routes']
    probe = json.loads((REPORTS / '019_ACHEMINEMENT_REPRO.json').read_text())
    rows = {row['offset']: row for row in report['entries']}

    assert len(routes) == 6
    assert {r['contract_offset'] for r in routes if r['in_same_lot']} == {
        '0x007DE55F', '0x007E6B88'}
    assert {r['contract_offset'] for r in probe['entries']} == {
        '0x007CE3D9', '0x007CE573', '0x007D35E9', '0x007E6C2E'}
    assert all(not r['json_entries'] and not r['resolved_live'] for r in probe['entries'])
    for route in routes:
        row = rows[route['contract_offset']]
        assert not row['direct_references'] and not row['alias_configured']
        assert route['prefix_hex'] == 'aa'
        assert int(route['offset'], 16) == int(route['contract_offset'], 16) + 1
        assert route['prefix_hex'] + route['snapshot']['raw_hex'] == row['english_snapshot']['raw_hex']
        assert route['references'] and route['offset_map_matches']


def test_long_sources_and_missing_spanish_entry_reconstructed():
    report = json.loads((REPORTS / '019_PREPARATION.json').read_text())
    rows = {row['offset']: row for row in report['entries']}

    assert {key: row['english_snapshot']['bytes_including_ff']
            for key, row in rows.items()
            if row['english_snapshot']['bytes_including_ff'] > 512} == {
                '0x007CFD04': 596, '0x007D4ABB': 569,
                '0x007DDA44': 520, '0x007DDC4C': 529}
    missing = rows['0x007E6816']
    assert missing['inventory']['etat'] == 'absent_es'
    assert missing['direct_references']
    assert 'Snivy' in missing['english_snapshot']['decoded_control_aware']
    assert [c['hex'] for c in missing['english_snapshot']['commands']] == [
        'fc0106', 'fc0102', 'fc0104', 'fc0102', 'fc0108', 'fc0102']
