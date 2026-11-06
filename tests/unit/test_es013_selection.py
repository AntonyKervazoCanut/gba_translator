"""ES-013 : sélection explicite, exclusive et complète, sans traduction livrée."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_all_374_contractual_keys_have_exactly_one_technical_decision():
    preparation = json.loads((ROOT / 'docs/analysis/es/013_PREPARATION.json').read_text())
    keys = {entry['offset'] for entry in preparation['entries']}
    lots = json.loads((ROOT / 'docs/analysis/es/lots.json').read_text())
    assert keys == set(next(lot['offsets'] for lot in lots if lot['id'] == 'ES-013'))
    assert len(keys) == 374
    routes = json.loads((ROOT / 'languages/es-maint/system_texts.json').read_text())
    aliases = json.loads((ROOT / 'languages/es-maint/text_aliases.json').read_text())
    decisions = [entry['offset'] for section in ('entries', 'excluded') for entry in routes[section] if entry['offset'] in keys]
    decisions += [entry['contract_offset'] for entry in aliases['aliases'] if entry['contract_offset'] in keys]
    assert len(decisions) == len(set(decisions)) == 374
    assert set(decisions) == keys
    assert len([e for e in routes['entries'] if e['offset'] in keys]) == 155
    assert len([e for e in routes['excluded'] if e['offset'] in keys]) == 199
    assert len([e for e in aliases['aliases'] if e['contract_offset'] in keys]) == 20


def test_alias_targets_do_not_create_a_second_route_or_selected_key():
    preparation = json.loads((ROOT / 'docs/analysis/es/013_PREPARATION.json').read_text())
    keys = {entry['offset'] for entry in preparation['entries']}
    routes = json.loads((ROOT / 'languages/es-maint/system_texts.json').read_text())
    route_keys = {entry['offset'] for entry in routes['entries']}
    aliases = json.loads((ROOT / 'languages/es-maint/text_aliases.json').read_text())
    for entry in aliases['aliases']:
        if entry['contract_offset'] in keys:
            assert entry['live_offset'] not in keys | route_keys
            assert set(bytes.fromhex(entry['prefix_hex'])) == {0}
