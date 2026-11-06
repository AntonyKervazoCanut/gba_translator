"""Contrats des mots structurés ES-004 sur des tranches ROM réelles."""
import json
from pathlib import Path

import pytest

from src.core.item_description_routes import SystemTextRoutes
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder
from src.core.text_reinserter import SmartReinserter

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / 'tests/unit/fixtures/es004_system_contract.json'


def source_rom():
    fixture = json.loads((ROOT / 'tests/unit/fixtures/es004_system_rom.json').read_text())
    rom = bytearray(fixture['rom_size'])
    for part in fixture['slices']:
        raw = bytes.fromhex(part['hex'])
        rom[part['offset']:part['offset']+len(raw)] = raw
    rom[-65536:] = b'\xff' * 65536
    return rom


def test_structured_routes_preserve_every_other_byte(tmp_path):
    source = source_rom()
    routes = SystemTextRoutes.load(CONTRACT, source)
    combined = {key: ('ZREZA' if key == 0x3DF7E8 else f'{n:02d}áéíóúüñ¡¿')
                for n, key in enumerate(routes.entries)}
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': []}))
    routes.enrich_json(path, combined)
    rom = bytearray(source)
    inserter = SmartReinserter(rom, allow_relocate=True, skip_encode_aliases=SPANISH_GLYPH_CHARS)
    items = json.loads(path.read_text())['translations']
    for item in items:
        assert inserter.reinsert_text(routes.normalize(item))
    inserter.flush_relocations()
    routes.verify(rom, path, combined)

    expected = bytearray(source)
    relocated = 0
    for item in items:
        key = item['offset']
        raw = TextEncoder.encode_pokemon(combined[key], skip_aliases=SPANISH_GLYPH_CHARS)
        refs = item['pointer_offsets']
        if not refs:
            assert key == 0x3DF7E8
            expected[key:key+len(raw)] = raw
        for ref in refs:
            target = int.from_bytes(rom[ref:ref+4], 'little')-0x08000000
            relocated += target != key
            expected[ref:ref+4] = rom[ref:ref+4]
            expected[target:target+len(raw)] = raw
    assert len(items) == 89
    assert relocated > 0
    assert rom == expected


@pytest.mark.parametrize('text', ['W'*13, 'A\nB', 'A<0xFA>B', 'A<0xFC><0x01><0x02>B'])
def test_easy_chat_rejects_overflow_and_commands(tmp_path, text):
    routes = SystemTextRoutes.load(CONTRACT, source_rom())
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': []}))
    with pytest.raises(ValueError):
        routes.enrich_json(path, {0x3E7F35: text})


def test_berry_name_cannot_relocate_or_overflow(tmp_path):
    routes = SystemTextRoutes.load(CONTRACT, source_rom())
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': []}))
    with pytest.raises(ValueError, match='octets'):
        routes.enrich_json(path, {0x3DF7E8: '1234567'})
    routes.enrich_json(path, {0x3DF7E8: '123456'})
    item = json.loads(path.read_text())['translations'][0]
    assert item['pointer_offsets'] == []
    assert item['max_length'] == 7


@pytest.mark.parametrize('site', [0x3DF7EF, 0x14E294, 0x3ECEDC, 0x3E7FE4, 0x8B7CC])
def test_structures_and_engine_roots_are_guarded(tmp_path, site):
    rom = source_rom()
    routes = SystemTextRoutes.load(CONTRACT, rom)
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': []}))
    rom[site] ^= 1
    with pytest.raises(ValueError, match='métadonnées'):
        routes.verify(rom, path)
    with pytest.raises(ValueError):
        SystemTextRoutes.load(CONTRACT, rom)


def test_fixture_matches_production_and_exact_es004_selection():
    contract = json.loads(CONTRACT.read_text())
    production = json.loads((ROOT / 'languages/es-maint/system_texts.json').read_text())
    keys = {e['offset'] for e in contract['entries']}
    assert len(keys) == 89
    assert [e for e in production['entries'] if e['offset'] in keys] == contract['entries']
    assert production['guards'] == contract['guards']
    preparation = json.loads((ROOT / 'docs/analysis/es/004_PREPARATION.json').read_text())
    items = json.loads((ROOT / 'languages/es-maint/item_descriptions.json').read_text())
    selected = {e['offset'] for e in preparation['entries']}
    active = {e['offset'] for e in items['entries']} & selected
    excluded = {e['offset'] for e in items['excluded']}
    assert len(active) == 167 and len(excluded) == 118
    assert active | keys | excluded == selected
    assert not (active & keys or keys & excluded or active & excluded)


@pytest.mark.rom
def test_current_engine_roots_and_exclusion_targets():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    report = json.loads((ROOT / 'docs/analysis/es/004_ROUTES.json').read_text())
    import hashlib
    assert hashlib.sha256(source).hexdigest() == report['source_sha256']
    SystemTextRoutes.verify_guards(source, report['legacy_engine_guards'])
    old = {int(e['offset'], 16) for e in report['entries']
           if e['decision'] == 'conservation sans injection'}
    for base, count, stride in [(0x876214, 1000, 44), (0x99F194, 892, 4)]:
        targets = {int.from_bytes(source[p:p+4], 'little')-0x08000000
                   for p in range(base, base+count*stride, stride)}
        assert not (old & targets)
    assert (0x083DB028).to_bytes(4, 'little') not in source
    assert not any(0x083DB028 <= int.from_bytes(source[p:p+4], 'little') < 0x083DF09C
                   for p in range(0, 0x1B0000, 4))
    glyphs = TextEncoder.encode_pokemon('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789áéíóúüñÁÉÍÓÚÜÑ¡¿', skip_aliases=SPANISH_GLYPH_CHARS)[:-1]
    for metrics in [0x1FB100, 0x207300]:
        assert max(source[metrics+glyph] for glyph in glyphs) <= 6
    SystemTextRoutes.load(ROOT / 'languages/es-maint/system_texts.json', source)
