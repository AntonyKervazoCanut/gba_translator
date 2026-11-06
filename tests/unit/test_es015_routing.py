"""Préservation ES-015 sur les préimages réelles du relevé gelé."""
import json
from pathlib import Path

import pytest

from src.core.text_codec import TextEncoder
from src.core.text_reinserter import SmartReinserter

ROOT = Path(__file__).resolve().parents[2]
REPORT = json.loads((ROOT / 'docs/analysis/es/015_PREPARATION.json').read_text())


def interior_fixture():
    entry = next(e for e in REPORT['entries'] if e['offset'] == '0x00741625')
    rom = bytearray(0x800000)
    raw = bytes.fromhex(entry['english_snapshot']['raw_hex'])
    rom[0x741625:0x741625+len(raw)] = raw
    for ref in entry['direct_references'] + [r for target in entry['interior_references'] for r in target['references']]:
        start = int(ref['context_start'], 16)
        context = bytes.fromhex(ref['context_hex'])
        rom[start:start+len(context)] = context
    rom[-4096:] = b'\xff' * 4096
    return rom, raw


def test_short_translation_preserves_interior_texts_and_branch():
    rom, raw = interior_fixture()
    before = bytes(rom)
    inserter = SmartReinserter(rom, allow_relocate=True)
    item = {'offset': 0x741625, 'translation': 'TEST', 'encoding': 'pokemon',
                'original_length': len(raw)-1, 'max_length': len(raw),
                'pointer_offsets': [0x740136], 'force_relocation': True,
                'english_raw_bytes': raw.hex(), 'allow_fallback': False, 'allow_truncate': False}

    assert inserter.reinsert_text(item)
    inserter.flush_relocations()

    target = int.from_bytes(rom[0x740136:0x74013A], 'little')-0x08000000
    assert target != 0x741625
    assert rom[target:target+5] == TextEncoder.encode_pokemon('TEST')
    assert rom[0x741625:0x741625+len(raw)] == raw
    allowed = set(range(0x740136, 0x74013A)) | set(range(target, target+5))
    assert all(i in allowed for i, (a, b) in enumerate(zip(before, rom)) if a != b)
    for pointer in (0x741548, 0x741565, 0x74155A):
        assert rom[pointer-2:pointer+4] == before[pointer-2:pointer+4]


@pytest.mark.parametrize('change', ['no_relocate', 'no_pointer', 'preimage'])
def test_preservation_fails_closed(change):
    rom, raw = interior_fixture()
    before = bytes(rom)
    item = {'offset': 0x741625, 'translation': 'TEST', 'encoding': 'pokemon',
                'original_length': len(raw)-1, 'max_length': len(raw),
                'pointer_offsets': [0x740136], 'force_relocation': True,
                'english_raw_bytes': raw.hex(), 'allow_fallback': True, 'allow_truncate': True}
    if change == 'no_pointer':
        item['pointer_offsets'] = []
    if change == 'preimage':
        item['english_raw_bytes'] = 'bbff'
    inserter = SmartReinserter(rom, allow_relocate=change != 'no_relocate')

    assert not inserter.reinsert_text(item)
    inserter.flush_relocations()

    assert rom == before


def test_es015_contract_routes_and_preservation_are_enabled():
    contract = json.loads((ROOT / 'languages/es-maint/text_aliases.json').read_text())
    expected = json.loads((ROOT / 'docs/analysis/es/015_ROUTES.json').read_text())['routes']
    entries = {r['contract_offset']: r for r in contract['aliases']}

    assert {r['contract_offset'] for r in expected} <= entries.keys()
    assert len(contract['preserved_sources']) == 67
    assert {r['offset'] for r in contract['preserved_sources'] if r.get('nontext')} == {
        '0x00721340', '0x0074037D', '0x00745132', '0x0074B293',
    }
    for route in expected:
        actual = entries[route['contract_offset']]
        assert actual['live_offset'] == route['offset']
        assert actual['english_raw_hex'] == route['snapshot']['raw_hex']
        assert actual['spanish_raw_hex'] == route['spanish_snapshot']['raw_hex']
        assert not actual.get('english_only')
        assert actual['pointer_offsets'] == [r['offset'] for r in route['references']]


def test_preservation_contract_rejects_lost_routes_and_changed_consumers(tmp_path):
    from src.core.text_source_preservation import TextSourcePreservation
    record = next(e for e in json.loads((ROOT / 'languages/es-maint/text_aliases.json').read_text())['preserved_sources'] if e['offset'] == '0x00741625')
    rom, _raw = interior_fixture()
    routes = TextSourcePreservation([record], {}, bytes(rom))
    item = {'offset': 0x741625, 'translation': next(e for e in REPORT['entries'] if e['offset'] == '0x00741625')['english_snapshot']['decoded_control_aware'].replace('\\n', '\n')}
    with pytest.raises(ValueError, match='disparue'):
        routes.enrich([], {0x741625}, {})
    routes.enrich([item], {0x741625}, {})
    assert item['force_relocation']
    assert not item['allow_fallback'] and not item['allow_truncate']
    path = tmp_path/'ready.json'
    path.write_text(json.dumps({'translations': [item]}))
    inserter = SmartReinserter(rom, allow_relocate=True)
    assert inserter.reinsert_text(item)
    inserter.flush_relocations()
    routes.verify(rom, path, {0x741625: item['translation']}, {})
    path.write_text(json.dumps({'translations': [item, item]}))
    with pytest.raises(ValueError, match='dupliquée'):
        routes.verify(rom, path, {0x741625: item['translation']}, {})
    path.write_text(json.dumps({'translations': [item]}))
    rom[0x74155A] ^= 1
    with pytest.raises(ValueError, match='consommateur'):
        routes.verify(rom, path, {0x741625: item['translation']}, {})


def test_dialogue_pages_use_engine_widths_and_preserve_scroll():
    import importlib
    builder = importlib.import_module('src.translators.19_build_translated_rom_generic').TranslatedROMBuilder
    data = json.loads((ROOT/'languages/es-maint/text_aliases.json').read_text())
    layout = {'glyph_widths_hex': data['fonts']['normal']['hex'], 'paged_dialogue': True,
                  'max_lines': 2, 'max_width': 208, 'buffer_widths': {'1': 70}}
    raw = TextEncoder.encode_pokemon('AB\nC<0xFA>D<0xFB>E<0xFC><0x01><0x06><0xFD><0x01>')

    widths = builder._encoded_layout_widths(raw, layout)

    assert widths == [12, 6, 6, 76]
    with pytest.raises(ValueError, match='lignes'):
        builder._encoded_layout_widths(TextEncoder.encode_pokemon('A\nB\nC'), layout)


def test_nontext_script_does_not_block_its_selected_panel(tmp_path):
    from src.core.text_source_preservation import TextSourcePreservation
    data = json.loads((ROOT/'languages/es-maint/text_aliases.json').read_text())
    record = next(e for e in data['preserved_sources'] if e['offset'] == '0x0074B293')
    raw = bytes.fromhex(record['english_raw_hex'])
    rom = bytearray(0x800000)
    rom[0x74B293:0x74B293+len(raw)] = raw
    for ref in record['interior_references']:
        start = int(ref['context_start'],16)
        context = bytes.fromhex(ref['context_hex'])
        rom[start:start+len(context)] = context
    routes = TextSourcePreservation([record], {}, bytes(rom))
    text = 'TEST<0xFB>TEST\nTEST'
    encoded = TextEncoder.encode_pokemon(text)
    rom[0x7F0000:0x7F0000+len(encoded)] = encoded
    rom[0x74B296:0x74B29A] = (0x087F0000).to_bytes(4,'little')
    path = tmp_path/'ready.json'
    path.write_text(json.dumps({'translations':[{'offset':0x74B29E,'translation':text}]}))

    routes.verify(rom, path, {0x74B29E:text}, {})

    rom[0x74B293] ^= 1
    with pytest.raises(ValueError):
        routes.verify(rom, path, {0x74B29E:text}, {})


@pytest.mark.parametrize('key', [0x721340, 0x74037D, 0x745132, 0x74B293,
                               0x71A3D2, 0x71A73A, 0x71A814, 0x7213FC, 0x745973, 0x7502A5])
def test_no_nontext_or_unqualified_start_is_written(key):
    from src.core.text_source_preservation import TextSourcePreservation
    data = json.loads((ROOT/'languages/es-maint/text_aliases.json').read_text())
    record = next(e for e in data['preserved_sources'] if int(e['offset'],16) == key)
    rom = bytearray(0x2000000)
    raw = bytes.fromhex(record['english_raw_hex'])
    rom[key:key+len(raw)] = raw
    for ref in record['direct_references'] + record['interior_references']:
        start = int(ref['context_start'],16)
        context = bytes.fromhex(ref['context_hex'])
        rom[start:start+len(context)] = context
    routes = TextSourcePreservation([record], {}, bytes(rom))

    with pytest.raises(ValueError, match='hors écriture|qualifier'):
        routes.enrich([{'offset':key,'translation':'TEST'}], {key}, {})


@pytest.mark.parametrize('prefix,live', [(0x721437,0x721438),(0x74BF85,0x74BF86)])
def test_canonical_pair_never_injects_twice(prefix, live):
    from src.core.text_aliases import TextAliases
    aliases = TextAliases({prefix: {'live_offset':live}})

    aliases.check_keys({live})
    aliases.check_keys({prefix})
    with pytest.raises(ValueError, match='collision'):
        aliases.check_keys({prefix,live})


def test_final_guard_rejects_unqualified_route_even_with_a_json_item(tmp_path):
    from src.core.text_source_preservation import TextSourcePreservation
    data = json.loads((ROOT/'languages/es-maint/text_aliases.json').read_text())
    record = next(e for e in data['preserved_sources'] if e['offset'] == '0x0071A3D2')
    rom = bytearray(0x2000000)
    raw = bytes.fromhex(record['english_raw_hex'])
    rom[0x71A3D2:0x71A3D2+len(raw)] = raw
    for ref in record['interior_references']:
        start = int(ref['context_start'],16)
        context = bytes.fromhex(ref['context_hex'])
        rom[start:start+len(context)] = context
    routes = TextSourcePreservation([record], {}, bytes(rom))
    # Même les commandes sont correctes : seule la preuve d'injection manque.
    text = ''.join(f'<0x{v:02X}>' for v in raw[:-1])
    path = tmp_path/'ready.json'
    path.write_text(json.dumps({'translations':[{'offset':0x71A3D2,'translation':text}]}))

    with pytest.raises(ValueError, match='qualifié'):
        routes.verify(rom, path, {0x71A3D2:text}, {})


@pytest.mark.parametrize('key', [0x721427,0x745A54,0x74BE3C,0x74ED62,0x75100E,
                               0x75350F,0x755532,0x75B4BB,0x75B6F4])
def test_alias_window_overflow_is_rejected_without_fallback(key):
    from src.core.item_description_routes import ItemDescriptionRoutes
    data = json.loads((ROOT/'languages/es-maint/text_aliases.json').read_text())
    record = next(e for e in data['aliases'] if int(e['contract_offset'],16) == key)
    raw = bytes.fromhex(record['english_raw_hex'])
    layout = dict(record['layout'], glyph_widths_hex=data['fonts']['normal']['hex'])
    text = ''.join(f'<0x{v:02X}>' for v in raw[:-1]) + 'W'*40
    item = {'offset':int(record['live_offset'],16), 'translation':text,
            'english_raw_bytes':raw.hex(), 'preserve_control_flow':True,
            'layout':layout, 'strict_encoded_layout':True}

    with pytest.raises(ValueError, match='budget'):
        ItemDescriptionRoutes.normalize(item)


def test_all_67_preimages_and_110_sites_are_accounted_for_exactly():
    data = json.loads((ROOT/'languages/es-maint/text_aliases.json').read_text())
    expected = {e['offset']:e for e in REPORT['entries'] if e['interior_references']}
    records = data['preserved_sources']

    assert len(records) == len(expected) == 67
    assert {e['offset'] for e in records} == expected.keys()
    assert sum(len(e['interior_references']) for e in records) == 110
    assert sum(r['qualification']=='unproven_binary' for e in records for r in e['interior_references']) == 65
    for record in records:
        original = expected[record['offset']]
        assert record['english_raw_hex'] == original['english_snapshot']['raw_hex']
        assert {(r['target'],r['offset']) for r in record['interior_references']} == {
            (target['offset'],ref['offset']) for target in original['interior_references'] for ref in target['references']}
        assert {r['offset'] for r in record['direct_references']} == {r['offset'] for r in original['direct_references']}
        assert set(record['pointer_offsets']) == {r['offset'] for r in record['direct_references'] if r['text_reader']}
