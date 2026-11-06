"""Contrats ES-014 : préimages propres et surfaces capacité/objet."""
import json
from pathlib import Path

import pytest

from src.core.item_description_routes import SystemTextRoutes
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder
from src.core.text_reinserter import SmartReinserter

ROOT = Path(__file__).resolve().parents[2]


def test_all_active_move_descriptions_use_clean_preimages():
    production = json.loads((ROOT / 'languages/es-maint/system_texts.json').read_text())
    entries = {int(e['offset'], 16): e for e in production['entries']}
    assert 0x482AA0 in entries
    entry = entries[0x482AA0]
    assert entry['layout']['max_lines'] == 5
    assert entry['layout']['max_width'] == 122
    assert entry['pointer_offsets'] == [0x48870C, 0x904024, 0x99F1B8]
    shared = entries[0x482BD5]
    assert shared['layout']['max_lines'] == 3
    assert shared['layout']['max_width'] == 122


CONTRACT = ROOT / 'tests/unit/fixtures/es014_contract.json'


def source_rom() -> bytearray:
    fixture = json.loads((ROOT / 'tests/unit/fixtures/es014_rom.json').read_text())
    rom = bytearray(fixture['rom_size'])
    for part in fixture['slices']:
        raw = bytes.fromhex(part['hex'])
        rom[part['offset']:part['offset']+len(raw)] = raw
    rom[-65536:] = b'\xff' * 65536
    return rom


def test_every_selected_consumer_and_every_other_byte(tmp_path):
    source = source_rom()
    routes = SystemTextRoutes.load(CONTRACT, source)
    combined = {key: '\n'.join([f'{n:03d}'+'i'*25]+['i'*28]*(e.get('layout', {'max_lines': 1})['max_lines']-1))
                for n, (key, e) in enumerate(routes.entries.items())}
    from importlib import import_module
    builder = import_module('src.translators.19_build_translated_rom_generic').TranslatedROMBuilder
    for key, entry in routes.entries.items():
        if 'layout' not in entry:
            commands = builder._extract_control_sequences_from_raw(bytes.fromhex(entry['source_hex']), include_breaks=True)
            combined[key] = 'PRUEBA ' + ''.join(''.join(f'<0x{b:02X}>' for b in cmd)+'i' for cmd in commands)
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': [{'offset': 0x482A53, 'original_text': 'Un coup de poing électrique', 'raw_bytes': 'ff'}]}))
    routes.enrich_json(path, combined)
    payload = json.loads(path.read_text())
    assert len(payload['translations']) == 357
    rom = bytearray(source)
    inserter = SmartReinserter(rom, allow_relocate=True, skip_encode_aliases=SPANISH_GLYPH_CHARS)
    for item in payload['translations']:
        assert item['english_raw_bytes'] == routes.entries[item['offset']]['source_hex']
        assert 'raw_bytes' not in item
        assert item['allow_fallback'] is False and item['allow_truncate'] is False
        assert inserter.reinsert_text(routes.normalize(item))
    inserter.flush_relocations()
    routes.verify(rom, path, combined)
    expected = bytearray(source)
    relocated = 0
    for key, entry in routes.entries.items():
        raw = TextEncoder.encode_pokemon(combined[key], skip_aliases=SPANISH_GLYPH_CHARS)
        for ref in entry['pointer_offsets']:
            target = int.from_bytes(rom[ref:ref+4], 'little')-0x08000000
            relocated += target != key
            expected[ref:ref+4] = rom[ref:ref+4]
            expected[target:target+len(raw)] = raw
    assert relocated > 300
    assert rom == expected


@pytest.mark.parametrize('text', ['A\nB\nC\nD\nE\nF', 'W'*30, 'A<0xFA>B', 'A<0xFF>B'])
def test_move_window_refuses_overflow_and_hidden_controls(tmp_path, text):
    routes = SystemTextRoutes.load(CONTRACT, source_rom())
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': []}))
    with pytest.raises(ValueError):
        routes.enrich_json(path, {0x482AA0: text})


def test_shared_item_window_refuses_four_lines(tmp_path):
    routes = SystemTextRoutes.load(CONTRACT, source_rom())
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': []}))
    with pytest.raises(ValueError, match='fenêtre'):
        routes.enrich_json(path, {0x482BD5: 'A\nB\nC\nD'})


@pytest.mark.parametrize('site', [0xE5440, 0x137BC8, 0x9F3B64, 0x99F194])
def test_engine_roots_and_unselected_cells_fail_closed(tmp_path, site):
    rom = source_rom()
    routes = SystemTextRoutes.load(CONTRACT, rom)
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': []}))
    rom[site] ^= 1
    with pytest.raises(ValueError):
        routes.verify(rom, path)


def test_exact_selection_and_production_contract():
    report = json.loads((ROOT / 'docs/analysis/es/014_ROUTES.json').read_text())
    lots = json.loads((ROOT / 'docs/analysis/es/lots.json').read_text())
    keys = next(lot['offsets'] for lot in lots if lot['id'] == 'ES-014')
    assert [e['offset'] for e in report['entries']] == keys
    fixture = json.loads(CONTRACT.read_text())
    production = json.loads((ROOT / 'languages/es-maint/system_texts.json').read_text())
    assert [e for e in production['entries'] if e['offset'] in keys] == fixture['entries']
    assert len(fixture['entries']) == 357
    assert len(fixture['excluded']) == 17
    assert {e['offset'] for e in fixture['entries'] + fixture['excluded']} == set(keys)
    assert all(g in production['guards'] for g in fixture['guards'])


def test_commands_arguments_and_buffer_order_are_exact():
    controls = '<0xFC><0x01><0x02><0xFD><0x03><0xF8><0x05><0xF9><0x06><0xF7><0x07>'
    text = controls+'A\nB\nC\nD\nE'
    raw = TextEncoder.encode_pokemon(text, skip_aliases=SPANISH_GLYPH_CHARS)
    item = {'offset': 0x482AA0, 'translation': text, 'english_raw_bytes': raw.hex(),
                'strict_encoded_layout': True, 'layout': {'max_lines': 5,'max_width': 122,'max_bytes': 512,'preserve_line_count': False}}
    assert TextEncoder.encode_pokemon(SystemTextRoutes.normalize(item)['translation']) == raw
    for before, after in [('<0x03>', '<0x04>'), ('<0x05>', '<0x06>'), ('<0x07>', '<0x08>'), ('<0x02>', '<0x03>')]:
        with pytest.raises(ValueError):
            SystemTextRoutes.normalize(dict(item, translation=text.replace(before, after)))


def test_rejected_exclusions_and_missing_delivery(tmp_path):
    routes = SystemTextRoutes.load(CONTRACT, source_rom())
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': []}))
    for key in routes.excluded:
        with pytest.raises(ValueError, match='sans injection'):
            routes.enrich_json(path, {key: 'INVALID'})
    routes.enrich_json(path, {0x482AA0: 'PRUEBA'})
    with pytest.raises(ValueError, match='non injectée'):
        routes.verify(source_rom(), path, {0x482AA0: 'PRUEBA'})
    payload = json.loads(path.read_text())
    payload['translations'] = []
    path.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match='disparue'):
        routes.verify(source_rom(), path, {0x482AA0: 'PRUEBA'})


def test_dynamic_tm_consumers_and_font_metrics_match_the_contract():
    from src.core.dialogue_linewrap import GLYPH_WIDTHS
    source = source_rom()
    routes = json.loads(CONTRACT.read_text())['entries']
    moves = {move: int(e['offset'], 16) for e in routes for move in e.get('move_ids', [])}
    dynamic = set()
    for n in range(128):
        site = 0x1A42B2A + 2*n
        move = int.from_bytes(source[site:site+2], 'little')
        if move in moves:
            dynamic.add(moves[move])
    shared = {int(e['offset'], 16) for e in routes if e.get('item_ids_cfru')}
    assert dynamic == shared
    assert len(shared) == 69
    assert source[0x207300:0x207400] == bytes(GLYPH_WIDTHS)
