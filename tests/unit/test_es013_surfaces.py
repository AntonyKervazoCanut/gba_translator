"""ES-013 : deux tables de natures et refus des décorations non certifiées."""
import json
from pathlib import Path

import pytest

from src.core.item_description_routes import SystemTextRoutes
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder
from src.core.text_reinserter import SmartReinserter

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / 'tests/unit/fixtures/es013_surfaces_contract.json'


def source_rom() -> bytearray:
    fixture = json.loads((ROOT / 'tests/unit/fixtures/es013_surfaces_rom.json').read_text())
    result = bytearray(fixture['rom_size'])
    for part in fixture['slices']:
        raw = bytes.fromhex(part['hex'])
        result[part['offset']:part['offset'] + len(raw)] = raw
    result[-65536:] = b'\xff' * 65536
    return result


def test_nature_ids_reach_both_tables_without_touching_neighbours(tmp_path):
    source = source_rom()
    routes = SystemTextRoutes.load(CONTRACT, source)
    combined = {key: f'ES{index:02d}iii' for index, key in enumerate(routes.entries)}
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': []}))
    routes.enrich_json(path, combined)
    payload = json.loads(path.read_text())
    rom = bytearray(source)
    inserter = SmartReinserter(rom, allow_relocate=True, skip_encode_aliases=SPANISH_GLYPH_CHARS)
    for item in payload['translations']:
        assert not item['allow_fallback'] and not item['allow_truncate']
        assert inserter.reinsert_text(routes.normalize(item))
    inserter.flush_relocations()
    routes.verify(rom, path, combined)
    expected = bytearray(source)
    for index, key in enumerate(routes.entries):
        raw = TextEncoder.encode_pokemon(combined[key], skip_aliases=SPANISH_GLYPH_CHARS)
        targets = []
        for ref in (0x463E60 + index * 4, 0x1FE65F4 + index * 4):
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            assert rom[target:target + len(raw)] == raw
            targets.append(target)
            expected[ref:ref + 4] = rom[ref:ref + 4]
            expected[target:target + len(raw)] = raw
        assert len(set(targets)) == 1
    assert rom == expected
    # An independently stale second consumer must fail final verification.
    rom[0x1FE65F4:0x1FE65F8] = source[0x1FE65F4:0x1FE65F8]
    with pytest.raises(ValueError, match='non injectée'):
        routes.verify(rom, path, combined)


@pytest.mark.parametrize('text', ['ABCDEFGH', 'A\nB', 'A<0xFA>B', 'A<0xFD><0x01>', 'A<0xFF>B'])
def test_nature_envelope_refuses_extended_names_and_controls(tmp_path, text):
    routes = SystemTextRoutes.load(CONTRACT, source_rom())
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': []}))
    with pytest.raises(ValueError):
        routes.enrich_json(path, {0x463DBC: text})


@pytest.mark.parametrize('site', [0x14C, 0x455F70, 0x4556F6, 0x488B8, 0x1375F0, 0x1377A8,
                                  0x1EB8D0C, 0x1EC820C, 0x1ECB154, 0x1ECB198])
def test_structures_and_all_nature_roots_are_guarded(tmp_path, site):
    rom = source_rom()
    routes = SystemTextRoutes.load(CONTRACT, rom)
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': []}))
    rom[site] ^= 1
    with pytest.raises(ValueError, match='racine ou métadonnées'):
        routes.verify(rom, path)


def test_uncertified_decorations_and_small_desk_prefix_are_not_importable(tmp_path):
    routes = SystemTextRoutes.load(CONTRACT, source_rom())
    assert len(routes.entries) == 25 and len(routes.excluded) == 55
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': []}))
    for offset in routes.excluded:
        with pytest.raises(ValueError, match='sans injection'):
            routes.enrich_json(path, {offset: 'PRUEBA'})


def test_exact_subset_preimages_and_unique_es_correspondences():
    report = json.loads((ROOT / 'docs/analysis/es/013_SURFACES.json').read_text())
    preparation = json.loads((ROOT / 'docs/analysis/es/013_PREPARATION.json').read_text())
    selected = [entry for entry in preparation['entries'] if entry['qualification'] in
                ('nature', 'description de décoration', 'fragment de structure')]
    assert [e['offset'] for e in report['entries']] == [e['offset'] for e in selected]
    assert len(selected) == 80
    for entry in selected:
        correspondence = entry['correspondances_es']
        assert len(correspondence) == 1
        if correspondence[0]['preimage_hex'] is None:
            assert correspondence[0]['mapping']['status'] == 'only_in_english'
    contract = json.loads(CONTRACT.read_text())
    for index, entry in enumerate(contract['entries']):
        assert entry['pointer_offsets'] == [0x463E60 + index * 4, 0x1FE65F4 + index * 4]
    assert not report['decoration_native_window_proven']
