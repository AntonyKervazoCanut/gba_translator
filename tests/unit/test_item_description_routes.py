"""Routage des descriptions ES sur des tranches réelles de la ROM EN."""
import importlib
import json
from pathlib import Path

import pytest

from src.core.item_description_routes import ItemDescriptionRoutes
from src.core.text_codec import TextEncoder
from src.core.text_reinserter import SmartReinserter

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / 'languages/es-maint/item_descriptions.json'
SENTINEL = '\n'.join(['i' * 32] * 3)


def source_rom():
    fixture = json.loads((ROOT / 'tests/unit/fixtures/item_descriptions_es.json').read_text())
    rom = bytearray(fixture['rom_size'])
    for part in fixture['slices']:
        raw = bytes.fromhex(part['hex'])
        rom[part['offset']:part['offset'] + len(raw)] = raw
    rom[-65536:] = b'\xff' * 65536
    return rom


def test_routes_recover_missing_json_and_keep_all_consumers(tmp_path):
    source = source_rom()
    routes = ItemDescriptionRoutes.load(CONTRACT, source)
    keys = set(routes.entries)
    combined = {key: f'{n:02d}' + SENTINEL[2:] for n, key in enumerate(sorted(keys))}
    # Four entries reached CSV before the fix; thirteen were silently dropped.
    existing = [{'offset': key, 'translation': SENTINEL, 'category': 'dialogue'}
                for key in [0x3D52B2, 0x3D546F, 0x3D54B5, 0x3D5503]]
    path = tmp_path / 'translation_ready.json'
    path.write_text(json.dumps({'translations': existing, 'total_translations': 4}))

    routes.enrich_json(path, combined)
    payload = json.loads(path.read_text())
    builder_type = importlib.import_module('src.translators.19_build_translated_rom_generic').TranslatedROMBuilder
    builder = builder_type.__new__(builder_type)
    builder.english_texts = None
    rom = bytearray(source)
    inserter = SmartReinserter(rom, allow_relocate=True)
    for item in payload['translations']:
        normalized = builder._normalize_translation_item(item['offset'], item)
        assert normalized['translation'] == combined[item['offset']]
        assert inserter.reinsert_text(normalized)
    inserter.flush_relocations()
    routes.verify(rom, path)

    assert {item['offset'] for item in payload['translations']} == keys
    assert payload['total_translations'] == 184
    targets = set()
    expected_rom = bytearray(source)
    for key, entry in routes.entries.items():
        expected = TextEncoder.encode_pokemon(combined[key])
        for pointer in entry['pointer_offsets']:
            target = int.from_bytes(rom[pointer:pointer+4], 'little') - 0x08000000
            assert rom[target:target+len(expected)] == expected
            targets.add(target)
            expected_rom[pointer:pointer+4] = rom[pointer:pointer+4]
            expected_rom[target:target+len(expected)] = expected
    assert rom == expected_rom
    assert len(targets) == 184
    assert b'\xfa' not in expected and b'\xfb' not in expected


@pytest.mark.parametrize('mutation', ['preimage', 'pointer', 'extra_pointer', 'consumer', 'duplicate'])
def test_routes_fail_closed_on_ambiguity(tmp_path, mutation):
    rom = source_rom()
    data = json.loads(CONTRACT.read_text())
    entry = data['entries'][0]
    offset = int(entry['offset'], 16)
    if mutation == 'preimage':
        rom[offset] ^= 1
    elif mutation == 'pointer':
        rom[entry['pointer_offsets'][0]] ^= 1
    elif mutation == 'extra_pointer':
        rom[100:104] = (offset + 0x08000000).to_bytes(4, 'little')
    elif mutation == 'consumer':
        entry['item_ids'] = [12]
    else:
        data['entries'].append(entry)
    contract = tmp_path / 'routes.json'
    contract.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        ItemDescriptionRoutes.load(contract, rom)


def test_fixed_window_preserves_full_commands_and_arguments():
    controls = '<0xFC><0x01><0x02><0xFD><0x03><0xF8><0x05><0xF9><0x06><0xF7><0x07>'
    text = controls + 'ONE\nTWO\nTHREE'
    raw = TextEncoder.encode_pokemon(text)
    item = {'offset': 0x3D52B2, 'translation': text, 'english_raw_bytes': raw.hex(),
                'layout': {'max_lines': 3, 'max_width': 176, 'preserve_line_count': False}}
    normalized = ItemDescriptionRoutes.normalize(item)
    assert TextEncoder.encode_pokemon(normalized['translation']) == raw
    for bad in [text.replace('<0x03>', '<0x04>'), text+'\nFOUR', text.replace('\n', '<0xFA>', 1), 'W'*50+'\nTWO\nTHREE']:
        with pytest.raises(ValueError):
            ItemDescriptionRoutes.normalize(dict(item, translation=bad))


def test_final_verification_rejects_silent_fallback(tmp_path):
    rom = source_rom()
    routes = ItemDescriptionRoutes.load(CONTRACT, rom)
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': []}))
    routes.enrich_json(path, {0x3D52B2: 'FIRST\nSECOND\nTHIRD'})
    with pytest.raises(ValueError, match='non injectée'):
        routes.verify(rom, path)


def test_generic_driver_consumes_routes_in_its_real_json(tmp_path, monkeypatch):
    import csv
    from dataclasses import replace

    from scripts import build_language as driver
    from src.core.text_codec import TextDecoder

    source = source_rom()
    routes = ItemDescriptionRoutes.load(CONTRACT, source)
    rom_path = tmp_path / 'source.gba'
    rom_path.write_bytes(source)
    combined = tmp_path / 'combined.txt'
    combined.write_text(''.join(f'0x{k:08X}: FIRST\\nSECOND\\nTHIRD\n' for k in routes.entries))
    base = tmp_path / 'base.csv'
    fields = ['offset', 'original_text', 'spanish_text', 'original_length',
              'padding_available', 'real_max_length', 'encoding', 'category', 'translation', 'notes']
    extracts = []
    with base.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for key in [0x3D52B2, 0x3D546F, 0x3D54B5, 0x3D5503, 0x3D5706]:
            raw = bytes.fromhex(routes.entries[key]['source_hex'])
            if key == 0x3D5706:
                raw = TextEncoder.encode_pokemon('Un lait très nourrissant.')
            text = TextDecoder.decode_pokemon(raw)
            extracts.append({'offset': key, 'decoded_text': text, 'raw_bytes': raw.hex(), 'byte_length': len(raw)})
            writer.writerow({'offset': f'0x{key:08X}', 'original_text': text,
                             'original_length': len(raw)-1, 'real_max_length': len(raw),
                             'padding_available': 0, 'encoding': 'pokemon', 'category': 'dialogue'})
    extracted = tmp_path / 'extraction.json'
    extracted.write_text(json.dumps({'text_count': len(extracts), 'texts': extracts}))
    for name, value in {'ENGLISH_ROM': rom_path, 'ENGLISH_EXTRACT': extracted,
                        'SPANISH_EXTRACT': extracted, 'GENERIC_BASE_CSV': base,
                        'TRANSLATION_DIR': tmp_path}.items():
        monkeypatch.setattr(driver, name, value)
    # Only output paths are redirected; the real CSV subprocess and converter run.
    config = replace(driver.load_registry().get('es-maint'), combined=str(combined), text_aliases=None, system_texts=None)
    monkeypatch.setattr(type(config), 'translation_json_path', lambda self, root: tmp_path / 'ready.json')

    result = driver.generate_translation_json(config)

    entries = json.loads(result.read_text())['translations']
    assert len(entries) == 184
    assert {e['offset'] for e in entries} == set(routes.entries)
    assert all(e['translation'] == 'FIRST\nSECOND\nTHIRD' for e in entries)
    assert all(e['pointer_offsets'] == routes.entries[e['offset']]['pointer_offsets'] for e in entries)
    assert all(e['layout']['max_lines'] == 3 for e in entries)
    assert all(e['english_raw_bytes'] == routes.entries[e['offset']]['source_hex'] for e in entries)
    assert {0x3D5934, 0x3D5968, 0x3D5AB8} <= {e['offset'] for e in entries}


def test_existing_layout_contract_keeps_strict_line_count():
    item = {'offset': 0x3D52B2, 'translation': 'ONE\nTWO\nTHREE',
            'english_raw_bytes': TextEncoder.encode_pokemon('ONE\nTWO').hex(),
            'layout': {'max_lines': 3, 'max_width': 176}}
    with pytest.raises(ValueError, match='ruptures'):
        ItemDescriptionRoutes.normalize(item)


def test_descriptor_routes_are_only_enabled_for_es_maint():
    from src.i18n import load_registry
    registry = load_registry()
    assert registry.get('es-maint').item_descriptions == 'languages/es-maint/item_descriptions.json'
    assert all(not config.item_descriptions for config in registry if config.code != 'es-maint')


def test_es004_active_descriptions_are_all_declared():
    report = json.loads((ROOT / 'docs/analysis/es/004_PREPARATION.json').read_text())
    expected = {e['offset'] for e in report['entries'] if e['item_ids_cfru_base_876200']}
    declared = {e['offset'] for e in json.loads(CONTRACT.read_text())['entries']}
    assert len(expected) == 167
    assert expected <= declared


def test_final_verification_rejects_entry_lost_after_conversion(tmp_path):
    routes = ItemDescriptionRoutes.load(CONTRACT, source_rom())
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': []}))
    routes.enrich_json(path, {0x3D52B2: 'FIRST\nSECOND\nTHIRD'})
    payload = json.loads(path.read_text())
    payload['translations'] = []
    path.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match='disparue'):
        routes.verify(source_rom(), path)


def test_explicit_layout_enforces_encoded_buffer_and_spanish_glyphs():
    item = {'offset': 0x3E7F35, 'translation': 'áéíóúüñ¡¿ÁÉÍÓ',
            'english_raw_bytes': TextEncoder.encode_pokemon('WORD').hex(),
            'layout': {'max_lines': 1, 'max_width': 104, 'max_bytes': 13}}
    with pytest.raises(ValueError, match='octets'):
        ItemDescriptionRoutes.normalize(item)


def test_excluded_legacy_key_cannot_be_injected(tmp_path):
    routes = ItemDescriptionRoutes.load(CONTRACT, source_rom())
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': []}))
    with pytest.raises(ValueError, match='sans injection'):
        routes.enrich_json(path, {0x3DA477: 'OLD TM'})


@pytest.mark.parametrize('text', ['A<0xFE>B<0xFE>C<0xFE>D', '<0xD1>'*30, ' '*30, 'A<0xFF>HIDDEN'])
def test_encoded_layout_cannot_hide_breaks_glyphs_or_spaces(text):
    item = {'offset': 1, 'translation': text,
            'english_raw_bytes': TextEncoder.encode_pokemon('WORD').hex(),
            **ItemDescriptionRoutes.layout_metadata()}
    with pytest.raises(ValueError, match='fenêtre'):
        ItemDescriptionRoutes.normalize(item)
