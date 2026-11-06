"""Contrats mécaniques ES-017 : préimages réelles, doublons et budgets."""
import json
from pathlib import Path

import pytest

from src.core.text_aliases import TextAliases

ROOT = Path(__file__).resolve().parents[2]
ROUTES = json.loads((ROOT/'docs/analysis/es/017_ROUTES.json').read_text())['routes']


def test_all_es017_routes_have_exact_preimages_and_consumers():
    data = json.loads((ROOT/'languages/es-maint/text_aliases.json').read_text())
    aliases = {r['contract_offset']: r for r in data['aliases']}
    for route in ROUTES:
        actual = aliases[route['contract_offset']]
        assert actual['live_offset'] == route['offset']
        assert actual['prefix_hex'] == 'aa'
        assert actual['english_raw_hex'] == route['snapshot']['raw_hex']
        match, = route['offset_map_matches']
        assert int(actual['spanish_offset'], 16) == match['mapping']['spanish_offset']
        assert actual['spanish_raw_hex'] == match['spanish_snapshot']['raw_hex']
        assert actual['pointer_offsets'] == [r['offset'] for r in route['references']]
        assert actual['layout']['max_width'] == (176 if route['contract_offset']=='0x007B3BE9' else 208)


@pytest.mark.parametrize('route', [r for r in ROUTES if r['in_same_lot']])
def test_canonical_live_key_rejects_double_injection(route):
    data = json.loads((ROOT/'languages/es-maint/text_aliases.json').read_text())
    record = next(r for r in data['aliases'] if r['contract_offset'] == route['contract_offset'])
    key, live = int(record['contract_offset'],16), int(record['live_offset'],16)
    aliases = TextAliases({key: dict(record, live_offset=live)})
    aliases.check_keys({live})
    with pytest.raises(ValueError, match='collision'):
        aliases.check_keys({key,live})


@pytest.mark.parametrize('route', ROUTES)
def test_relocation_failure_is_atomic_on_real_preimage(route):
    from src.core.text_reinserter import SmartReinserter
    live = int(route['offset'], 16)
    raw = bytes.fromhex(route['snapshot']['raw_hex'])
    rom = bytearray(0x900000)
    rom[live:live+len(raw)] = raw
    refs = []
    for ref in route['references']:
        start = int(ref['context_start'], 16)
        context = bytes.fromhex(ref['context_hex'])
        rom[start:start+len(context)] = context
        refs.append(int(ref['offset'], 16))
    before = bytes(rom)
    item = {'offset': live, 'translation': 'TEST', 'encoding': 'pokemon',
                'english_raw_bytes': raw.hex(), 'original_length': len(raw)-1,
                'max_length': len(raw), 'pointer_offsets': refs, 'force_relocation': True,
                'allow_fallback': False, 'allow_truncate': False}
    inserter = SmartReinserter(rom, allow_relocate=False)

    assert not inserter.reinsert_text(item)
    inserter.flush_relocations()

    assert rom == before


@pytest.mark.parametrize('route', ROUTES)
def test_window_overflow_never_falls_back(route):
    from src.core.item_description_routes import ItemDescriptionRoutes
    data = json.loads((ROOT/'languages/es-maint/text_aliases.json').read_text())
    record = next(r for r in data['aliases'] if r['contract_offset'] == route['contract_offset'])
    layout = dict(record['layout'], glyph_widths_hex=data['fonts']['normal']['hex'])
    raw = bytes.fromhex(record['english_raw_hex'])
    text = 'W'*40 + ''.join(f'<0x{v:02X}>' for v in raw[:-1])
    item = {'offset': int(record['live_offset'],16), 'translation': text,
                'english_raw_bytes': raw.hex(), 'preserve_control_flow': True,
                'layout': layout, 'strict_encoded_layout': True}

    with pytest.raises(ValueError, match='budget|plafond'):
        ItemDescriptionRoutes.normalize(item)


def test_es017_preservation_accounts_for_every_interior_occurrence():
    data = json.loads((ROOT/'languages/es-maint/text_aliases.json').read_text())
    report = json.loads((ROOT/'docs/analysis/es/017_PREPARATION.json').read_text())
    rows = {r['offset']:r for r in report['entries']}
    records = [r for r in data['preserved_sources'] if r.get('lot') == 'ES-017']
    assert len(records) == 25
    for record in records:
        original = rows[record['offset']]
        assert record['english_raw_hex'] == original['english_snapshot']['raw_hex']
        assert {(r['target'],r['offset']) for r in record['interior_references']} == {
            (target['offset'],ref['offset']) for target in original['interior_references'] for ref in target['references']}
        assert set(record['pointer_offsets']) == {
            r['offset'] for r in record['interior_references'] if r['text_reader']}


def test_item_53_uses_its_live_cfru_description_and_three_line_budget():
    data = json.loads((ROOT/'languages/es-maint/text_aliases.json').read_text())
    record = next(r for r in data['aliases'] if r['contract_offset']=='0x007B3BE9')
    assert int(record['pointer_offsets'][0],16) == 0x876200 + 53*44 + 0x14
    assert record['layout'] == {'font': 'normal', 'max_lines': 3, 'max_width': 176, 'preserve_line_count': False}


@pytest.mark.parametrize('route', ROUTES)
def test_relocation_is_deterministic_and_flush_is_idempotent(route):
    from src.core.text_codec import TextEncoder
    from src.core.text_reinserter import SmartReinserter
    live = int(route['offset'], 16)
    raw = bytes.fromhex(route['snapshot']['raw_hex'])
    source = bytearray(0x900000)
    source[live:live+len(raw)] = raw
    refs = [int(r['offset'], 16) for r in route['references']]
    for ref in route['references']:
        start = int(ref['context_start'], 16)
        context = bytes.fromhex(ref['context_hex'])
        source[start:start+len(context)] = context
    fixture = json.loads((ROOT/'tests/unit/fixtures/text_aliases/es017.json').read_text())
    for part in fixture['slices']:
        start = part['offset']
        context = bytes.fromhex(part['hex'])
        source[start:start+len(context)] = context
    source[-4096:] = b'\xff'*4096
    item = {'offset': live, 'translation': 'TEST', 'encoding': 'pokemon',
            'english_raw_bytes': raw.hex(), 'original_length': len(raw)-1,
            'max_length': len(raw), 'pointer_offsets': refs, 'force_relocation': True,
            'allow_fallback': False, 'allow_truncate': False}
    results = []

    for _ in range(2):
        rom = bytearray(source)
        inserter = SmartReinserter(rom, allow_relocate=True)
        assert inserter.reinsert_text(dict(item))
        inserter.flush_relocations()
        result = bytes(rom)
        inserter.flush_relocations()
        assert bytes(rom) == result
        results.append(result)

    assert results[0] == results[1]
    for site in refs:
        target = int.from_bytes(results[0][site:site+4], 'little')-0x08000000
        assert target != live
        assert results[0][target:target+5] == TextEncoder.encode_pokemon('TEST')
    assert results[0][live:live+len(raw)] == raw
