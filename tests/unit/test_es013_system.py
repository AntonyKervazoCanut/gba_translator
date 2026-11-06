"""Sentinelles système ES-013 : contrats, contrôles et écritures bornées."""
import importlib
import json
from pathlib import Path

import pytest

from src.core.item_description_routes import SystemTextRoutes
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder
from src.core.text_reinserter import SmartReinserter

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / 'tests/unit/fixtures/es013_system_contract.json'
Builder = importlib.import_module('src.translators.19_build_translated_rom_generic').TranslatedROMBuilder


def source_rom():
    fixture = json.loads((ROOT / 'tests/unit/fixtures/es013_system_rom.json').read_text())
    rom = bytearray(fixture['rom_size'])
    for part in fixture['slices']:
        raw = bytes.fromhex(part['hex'])
        rom[part['offset']:part['offset'] + len(raw)] = raw
    rom[-65536:] = b'\xff' * 65536
    return rom


def sentinel(entry):
    commands = Builder._extract_control_sequences_from_raw(bytes.fromhex(entry['source_hex']), include_breaks=True)
    return 'PRUEBA ' + ''.join(''.join(f'<0x{b:02X}>' for b in command) + 'i' for command in commands)


def test_all_system_routes_preserve_commands_and_every_other_byte(tmp_path):
    source = source_rom()
    routes = SystemTextRoutes.load(CONTRACT, source)
    combined = {key: sentinel(entry) for key, entry in routes.entries.items()}
    path = tmp_path / 'ready.json'
    path.write_text('{"translations": []}')
    routes.enrich_json(path, combined)
    payload = json.loads(path.read_text())
    assert len(payload['translations']) == 124
    rom = bytearray(source)
    inserter = SmartReinserter(rom, allow_relocate=True, skip_encode_aliases=SPANISH_GLYPH_CHARS)
    for item in payload['translations']:
        assert not item['allow_fallback'] and not item['allow_truncate']
        assert inserter.reinsert_text(routes.normalize(item))
    inserter.flush_relocations()
    routes.verify(rom, path, combined)
    expected = bytearray(source)
    for key, entry in routes.entries.items():
        raw = TextEncoder.encode_pokemon(combined[key], skip_aliases=SPANISH_GLYPH_CHARS)
        for site in entry['pointer_offsets']:
            target = int.from_bytes(rom[site:site + 4], 'little') - 0x08000000
            expected[site:site + 4] = rom[site:site + 4]
            expected[target:target + len(raw)] = raw
    assert rom == expected


@pytest.mark.parametrize('key', [0x457860, 0x45787C, 0x457B2C, 0x457B4C, 0x458F2C, 0x458F60, 0x458314, 0x45817E])
def test_unqualified_tables_and_graphic_match_are_refused(tmp_path, key):
    routes = SystemTextRoutes.load(CONTRACT, source_rom())
    path = tmp_path / 'ready.json'
    path.write_text('{"translations": []}')
    with pytest.raises(ValueError, match='sans injection'):
        routes.enrich_json(path, {key: 'PRUEBA'})


def test_all_82_padding_duplicates_are_refused(tmp_path):
    prep = json.loads((ROOT / 'docs/analysis/es/013_PREPARATION.json').read_text())
    routes = SystemTextRoutes.load(CONTRACT, source_rom())
    keys = {int(e['offset'], 16) for e in prep['entries'] if e['qualification'] == 'doublon de remplissage'}
    assert len(keys) == 82 and keys <= routes.excluded
    path = tmp_path / 'ready.json'
    path.write_text('{"translations": []}')
    with pytest.raises(ValueError, match='sans injection'):
        routes.enrich_json(path, dict.fromkeys(keys, 'PRUEBA'))


def test_offer_source_and_long_buffers_fit_qualified_window(tmp_path):
    routes = SystemTextRoutes.load(CONTRACT, source_rom())
    entry = routes.entries[0x457D44]
    text = ''.join(f'<0x{b:02X}>' for b in bytes.fromhex(entry['source_hex'])[:-1])
    path = tmp_path / 'ready.json'
    path.write_text('{"translations": []}')
    routes.enrich_json(path, {0x457D44: text})
    assert entry['layout']['buffers'] == {'0': {'max_width': 18, 'max_bytes': 3}, '1': {'max_width': 60, 'max_bytes': 10}, '2': {'max_width': 18, 'max_bytes': 3}, '3': {'max_width': 60, 'max_bytes': 10}}
    with pytest.raises(ValueError, match='fenêtre'):
        routes.enrich_json(path, {0x457D44: 'W' * 40 + text})
    with pytest.raises(ValueError, match='commandes'):
        routes.enrich_json(path, {0x457D44: text.replace('<0xF7><0x00>', '<0xF7><0x03>')})


def test_header_fc13_arguments_and_column_budget(tmp_path):
    routes = SystemTextRoutes.load(CONTRACT, source_rom())
    entry = routes.entries[0x459378]
    path = tmp_path / 'ready.json'
    path.write_text('{"translations": []}')
    raw = bytes.fromhex(entry['source_hex'])
    text = ''.join(f'<0x{b:02X}>' for b in raw[:-1])
    routes.enrich_json(path, {0x459378: text})
    with pytest.raises(ValueError, match='colonne'):
        routes.enrich_json(path, {0x459378: 'W' * 20 + text})
    with pytest.raises(ValueError, match='commandes'):
        routes.enrich_json(path, {0x459378: text.replace('<0x13><0xC6>', '<0x13><0xC5>')})


def test_every_system_source_enforces_512_and_control_arguments(tmp_path):
    routes = SystemTextRoutes.load(CONTRACT, source_rom())
    path = tmp_path / 'ready.json'
    path.write_text('{"translations": []}')
    for key, entry in routes.entries.items():
        with pytest.raises(ValueError):
            routes.enrich_json(path, {key: 'i' * 512 + sentinel(entry)})
        raw = bytes.fromhex(entry['source_hex'])
        commands = Builder._extract_control_sequences_from_raw(raw)
        for command in commands:
            if len(command) < 2:
                continue
            changed = bytearray(raw)
            changed[raw.index(bytes(command)) + len(command) - 1] ^= 1
            text = ''.join(f'<0x{b:02X}>' for b in changed[:-1])
            with pytest.raises(ValueError):
                routes.enrich_json(path, {key: text})


def test_window_routines_and_unselected_branch_are_guarded(tmp_path):
    rom = source_rom()
    routes = SystemTextRoutes.load(CONTRACT, rom)
    path = tmp_path / 'ready.json'
    path.write_text('{"translations": []}')
    for site in [0x458314, 0x11AE90, 0x11B05C, 0x11A1D6, 0x456F1C]:
        changed = bytearray(rom)
        changed[site] ^= 1
        with pytest.raises(ValueError, match='métadonnées'):
            routes.verify(changed, path, {})


def test_species_copy_table_bounds_are_real_and_guarded_after_patches(tmp_path):
    rom = source_rom()
    routes = SystemTextRoutes.load(CONTRACT, rom)
    font = bytes.fromhex(routes.entries[0x457D44]['layout']['engine_fonts']['2']['hex'])
    cells = [rom[0x166A98C + i * 11:0x166A98C + (i + 1) * 11] for i in range(1294)]
    assert all(255 in cell for cell in cells)
    names = [cell[:cell.index(255)] for cell in cells]
    assert max(map(len, names)) == 10
    assert max(sum(font[b] for b in name) for name in names) == 59
    path = tmp_path / 'ready.json'
    path.write_text('{"translations": []}')
    rom[0x166A98C + 11] ^= 1
    with pytest.raises(ValueError, match='métadonnées'):
        routes.verify(rom, path, {})
