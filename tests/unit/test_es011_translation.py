"""ES-011 : sélection fermée, commandes complètes et octets aux lecteurs finaux."""
import importlib
import importlib.util
import json
import re
from pathlib import Path

import pytest

from scripts.audit_translation_coverage import parse_combined
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / 'docs/analysis/es/011_TRAITEMENT.json'
Builder = importlib.import_module('src.translators.19_build_translated_rom_generic').TranslatedROMBuilder


def test_es011_exact_selection_values_commands_and_budgets():
    report = json.loads(REPORT.read_text())
    lot = next(row for row in json.loads((ROOT / 'docs/analysis/es/lots.json').read_text()) if row['id'] == 'ES-011')
    combined = parse_combined(ROOT / 'languages/es-maint/combined_es-maint.txt')

    assert [row['offset'] for row in report['entries']] == lot['offsets']
    assert len(set(lot['offsets'])) == 374
    assert report['counts'] == {'traduit': 297, 'conserve_nom': 5, 'conserve_sans_lecteur_identifie': 4,
                                'doublon_canonique': 4, 'conserve_credits_historiques': 60, 'exclu_binaire': 4}
    for row in report['entries']:
        key = int(row['offset'], 16)
        assert row['justification']
        if 'texte' not in row:
            assert key not in combined
            continue
        assert combined[key] == row['texte'].replace('\n', r'\n')
        encoded = TextEncoder.encode_pokemon(row['texte'], skip_aliases=SPANISH_GLYPH_CHARS, strict=True)
        assert encoded.hex() == row['encoded_hex']
        assert len(encoded) <= 512
        source = bytes.fromhex(row['source_hex'])
        assert Builder._extract_control_sequences_from_raw(encoded) == Builder._extract_control_sequences_from_raw(source)
        layout = {'allow_pagination': True, **(row.get('layout') or {})}
        widths = Builder._encoded_layout_widths(encoded, layout)
        assert widths == row['largeurs_px']
        assert max(widths) <= row['budget_px']
        assert all(len(page.splitlines()) <= row['max_lignes']
                   for page in re.split(r'<0xF[AB]>', row['texte']))
        if 'largeurs_variables_px' in row:
            assert max(row['largeurs_variables_px']) <= row['budget_px']
        if row.get('reserve_fd_px'):
            expanded = re.sub(r'<0xFD><0x[0-9A-F]{2}>', 'W' * 12, row['texte'])
            estimated = Builder._encoded_layout_widths(TextEncoder.encode_pokemon(
                expanded, skip_aliases=SPANISH_GLYPH_CHARS), {'allow_pagination': True})
            assert estimated == row['largeurs_variables_px']
        if row['surface'] == 'Pokédex':
            assert len(row['texte'].splitlines()) <= 3
            assert not Builder._extract_control_sequences_from_raw(encoded)


@pytest.mark.rom
def test_es011_final_rom_all_readers_exclusions_and_prefixes():
    report = json.loads(REPORT.read_text())
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    actual = (ROOT / 'output/roms/GenedRom-es-maint.gba').read_bytes()
    for root in (0x88E34, 0x105D44):
        assert int.from_bytes(source[root:root + 4], 'little') == 0x09A357CC
        assert actual[root:root + 4] == source[root:root + 4]

    for row in report['entries']:
        key = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[key:key + len(raw)] == raw
        if 'texte' not in row:
            if row['decision'] == 'doublon_canonique':
                continue  # Testé via sa clé contractuelle, relocation ou insertion en place.
            assert actual[key:key + len(raw)] == raw, row['offset']
            for reference in row['references']:
                ref = int(reference, 16)
                assert actual[ref:ref + 4] == source[ref:ref + 4]
            if row.get('source_vivante_hors_lot'):
                neighbor = row['source_vivante_hors_lot']
                ref, target = int(neighbor['reference'], 16), int(neighbor['cible'], 16)
                expected = bytes.fromhex(neighbor['source_hex'])
                assert actual[ref:ref + 4] == source[ref:ref + 4]
                assert actual[target:target + len(expected)] == expected
            continue
        live = int(row['live_offset'], 16)
        assert actual[key:live] == source[key:live]
        expected = bytes.fromhex(row['encoded_hex'])
        if row['surface'] == 'Pokédex':
            ref = int(row['references'][0], 16)
            base = 0x1A357CC + row['index_table'] * 36
            assert ref == base + 0x10
            assert actual[base:ref] == source[base:ref]
            assert actual[ref + 4:base + 36] == source[ref + 4:base + 36]
            secondary = int.from_bytes(source[ref + 4:ref + 8], 'little') - 0x08000000
            assert source[secondary] == actual[secondary] == 0xFF
        assert row['references']
        for reference in row['references']:
            ref = int(reference, 16)
            assert int.from_bytes(source[ref:ref + 4], 'little') == live + 0x08000000
            target = int.from_bytes(actual[ref:ref + 4], 'little') - 0x08000000
            assert 0 <= target < len(actual)
            assert actual[target:target + len(expected)] == expected, (row['offset'], reference, hex(target))


def test_es011_routes_preserve_every_reviewed_page_without_generic_rewrap():
    from src.core.item_description_routes import SystemTextRoutes

    records = json.loads(REPORT.read_text())['entries']
    data = json.loads((ROOT / 'languages/es-maint/system_texts.json').read_text())
    routes = {int(row['offset'], 16): row for row in data['entries']}
    for row in records:
        if 'texte' not in row:
            continue
        key = int(row['offset'], 16)
        delta = int(row['live_offset'], 16) - key
        metadata = {'preserve_control_flow': True}
        if row.get('layout'):
            metadata.update(layout=row['layout'], strict_encoded_layout=True)
        else:
            if 'layout' in routes[key]:
                layout = {**routes[key]['layout'], 'engine_fonts': data['engine_fonts'],
                          'glyph_widths_hex': data['engine_fonts'][str(routes[key]['layout']['initial_font'])]['hex']}
                metadata.update(layout=layout, strict_encoded_layout=True)
                assert Builder._encoded_layout_widths(bytes.fromhex(row['encoded_hex']), layout) == row['largeurs_variables_px']
            assert routes[key]['source_hex'] == row['source_hex']
            assert routes[key]['pointer_offsets'] == [int(p, 16) for p in row['references']]
        normalized = SystemTextRoutes.normalize({'offset': key, 'translation': row['texte'],
            'english_raw_bytes': row['source_hex'][delta * 2:], **metadata})
        assert normalized['translation'] == row['texte'], row['offset']


def test_es011_native_views_keep_every_script_reader_and_choose_an_aligned_site(tmp_path, monkeypatch):
    report = json.loads(REPORT.read_text())
    contract = tmp_path / 'docs/analysis/es/011_TRAITEMENT.json'
    contract.parent.mkdir(parents=True)
    contract.write_text(json.dumps(report))
    spec = importlib.util.spec_from_file_location('es011_native_views',
        ROOT / 'tests/e2e-playwright/fixtures/prepare_es011_production.py')
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, 'ROOT', tmp_path)

    module.prepare()

    actual = json.loads((tmp_path / 'output/reports/es011-native.json').read_text())['entries']
    expected = [row for row in report['entries'] if 'texte' in row and not row['commandes_source']]
    assert [row['offset'] for row in actual] == [row['offset'] for row in expected]
    assert any(int(row['references'][0], 16) % 4 for row in expected)
    for before, after in zip(expected, actual):
        assert sorted(after['references']) == sorted(before['references'])
        assert int(after['references'][0], 16) % 4 == 0
        assert dict(after, references=before['references']) == before
