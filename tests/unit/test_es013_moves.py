"""Six descriptions ES-013 : contrat F-1042 réutilisé sans traduction finale."""
import json
from pathlib import Path

import pytest

from src.core.item_description_routes import SystemTextRoutes
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder
from src.core.text_reinserter import SmartReinserter

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / 'tests/unit/fixtures/es013_moves_contract.json'
KEYS = (0x482874, 0x4828BD, 0x4828FF, 0x482946, 0x482985, 0x4829C9)


def source_rom() -> bytearray:
    """Reconstruit les tranches ROM propres du contrat, voisins inclus."""
    fixture = json.loads((ROOT / 'tests/unit/fixtures/es013_moves_rom.json').read_text())
    rom = bytearray(fixture['rom_size'])
    for part in fixture['slices']:
        raw = bytes.fromhex(part['hex'])
        rom[part['offset']:part['offset'] + len(raw)] = raw
    rom[-65536:] = b'\xff' * 65536
    return rom


def test_six_clean_preimages_reconstruct_missing_and_french_cache(tmp_path):
    routes = SystemTextRoutes.load(CONTRACT, source_rom())
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': [
        {'offset': 0x482874, 'original_text': 'Ancien cache français', 'raw_bytes': 'ff'}
    ]}))
    combined = {key: 'PRUEBA' for key in KEYS}
    routes.enrich_json(path, combined)
    items = json.loads(path.read_text())['translations']
    assert {e['offset'] for e in items} == set(KEYS)
    for item in items:
        assert item['english_raw_bytes'] == routes.entries[item['offset']]['source_hex']
        assert item['allow_fallback'] is False
        assert item['allow_truncate'] is False
        assert 'raw_bytes' not in item
    assert routes.entries[0x482985]['source_hex'].startswith('c8e9e1d9')


def test_relocation_reaches_all_eighteen_consumers_and_changes_no_other_byte(tmp_path):
    source = source_rom()
    routes = SystemTextRoutes.load(CONTRACT, source)
    combined = {key: '\n'.join([f'{i:02d}' + 'i' * 25] + ['i' * 30] * 4)
                for i, key in enumerate(KEYS)}
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': []}))
    routes.enrich_json(path, combined)
    rom = bytearray(source)
    inserter = SmartReinserter(rom, allow_relocate=True, skip_encode_aliases=SPANISH_GLYPH_CHARS)
    for item in json.loads(path.read_text())['translations']:
        assert inserter.reinsert_text(routes.normalize(item))
    inserter.flush_relocations()
    routes.verify(rom, path, combined)
    expected = bytearray(source)
    for key, entry in routes.entries.items():
        raw = TextEncoder.encode_pokemon(combined[key], skip_aliases=SPANISH_GLYPH_CHARS)
        targets = set()
        for ref in entry['pointer_offsets']:
            target = int.from_bytes(rom[ref:ref+4], 'little') - 0x08000000
            assert target != key
            targets.add(target)
            expected[ref:ref+4] = rom[ref:ref+4]
            expected[target:target+len(raw)] = raw
        assert len(targets) == 1
    assert rom == expected


@pytest.mark.parametrize('text', ['A\nB\nC\nD\nE\nF', 'W' * 30, 'A<0xFA>B', 'A<0xFB>B', 'A<0xFF>B', 'i' * 512])
def test_window_and_control_flow_refuse_invalid_translation(tmp_path, text):
    routes = SystemTextRoutes.load(CONTRACT, source_rom())
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': []}))
    with pytest.raises(ValueError):
        routes.enrich_json(path, {0x482985: text})


def test_same_engine_contract_has_no_item_or_dynamic_tm_consumer():
    source = source_rom()
    contract = json.loads(CONTRACT.read_text())
    assert tuple(int(e['offset'], 16) for e in contract['entries']) == KEYS
    assert [e['move_ids'] for e in contract['entries']] == [[i] for i in range(2, 8)]
    assert all(not e['item_ids_cfru'] for e in contract['entries'])
    moves = {int.from_bytes(source[0x1A42B2A+i*2:0x1A42B2C+i*2], 'little') for i in range(128)}
    assert not moves.intersection(range(2, 8))
    for entry in contract['entries']:
        move = entry['move_ids'][0]
        assert entry['pointer_offsets'] == [0x4886E8+(move-1)*4, 0x904000+(move-1)*4, 0x99F190+move*4]
        assert entry['layout'] == {'max_lines': 5, 'max_width': 122, 'max_bytes': 512, 'preserve_line_count': False}


@pytest.mark.parametrize('site', [0xE5440, 0x137BC8, 0x9F3B64, 0x1A42B2A, 0x207300])
def test_shared_engine_roots_and_metrics_are_guarded(tmp_path, site):
    source = source_rom()
    routes = SystemTextRoutes.load(CONTRACT, source)
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': []}))
    source[site] ^= 1
    with pytest.raises(ValueError, match='racine ou métadonnées'):
        routes.verify(source, path)


def test_unique_es_mappings_and_production_contract():
    report = json.loads((ROOT / 'docs/analysis/es/013_MOVES.json').read_text())
    production = json.loads((ROOT / 'languages/es-maint/system_texts.json').read_text())
    selected = {e['offset']: e for e in production['entries']}
    contract = json.loads(CONTRACT.read_text())
    for entry in contract['entries']:
        assert selected[entry['offset']] == entry
    for entry in report['entries']:
        assert len(entry['correspondances_es']) == 1
        assert entry['correspondances_es'][0]['mapping']['status'] == 'matched'
    # F-1042's old immutable cells become explicitly routed cells, not broad allowances.
    for guard in report['superseded_guards']:
        assert guard not in production['guards']
