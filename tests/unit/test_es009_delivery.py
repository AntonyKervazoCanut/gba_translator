"""Livraison ES-009 : sélection figée, décisions et flux de commandes exacts."""
import importlib
import json
from pathlib import Path

import yaml

from scripts.apply_combined_fr import _load_combined
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder

ROOT = Path(__file__).resolve().parents[2]


def test_all_374_decisions_and_exact_protected_values():
    """Ni clé oubliée, ni exclusion utilisée comme traduction fictive."""
    report = json.loads((ROOT / 'docs/analysis/es/009_DELIVERY.json').read_text())
    lot = next(lot for lot in json.loads((ROOT / 'docs/analysis/es/lots.json').read_text())
               if lot['id'] == 'ES-009')
    combined, _ = _load_combined(ROOT / 'languages/es-maint/combined_es-maint.txt')
    protected = yaml.safe_load((ROOT / 'languages/es-maint/protected_entries.yaml').read_text())
    protected = {int(e['offset'], 16): e for e in protected['entries']}
    entries = report['entries']

    assert len(entries) == len({e['offset'] for e in entries}) == 374
    assert {e['offset'] for e in entries} == set(lot['offsets'])
    assert sum(e['translation'] is not None for e in entries) == 337
    assert sum(e['translation'] is None for e in entries) == 37
    for entry in entries:
        key = int(entry['offset'], 16)
        assert entry['decision'] and entry['reason'] and entry['surface']
        if entry['translation'] is None:
            assert key not in combined
        else:
            assert combined[key] == entry['translation'].replace('\\n', '\n')
            assert protected[key]['expected'] == entry['translation']


def test_control_arguments_buffers_and_page_order_are_preserved():
    """Les lettres du décodage debug ne deviennent pas des arguments traduits."""
    report = json.loads((ROOT / 'docs/analysis/es/009_DELIVERY.json').read_text())
    builder = importlib.import_module(
        'src.translators.19_build_translated_rom_generic').TranslatedROMBuilder
    for entry in report['entries']:
        if entry['translation'] is None:
            continue
        source = bytes.fromhex(entry['source_hex'])
        raw = TextEncoder.encode_pokemon(entry['translation'].replace('\\n', '\n'),
                                         skip_aliases=SPANISH_GLYPH_CHARS)
        assert len(raw) <= 512
        assert raw[-1] == 255
        assert builder._extract_control_sequences_from_raw(raw) == (
            builder._extract_control_sequences_from_raw(source)), entry['offset']


def test_graphic_occurrences_require_bounded_in_place_cells():
    """Aucun faux pointeur graphique n'est transmis comme site à repointer."""
    report = json.loads((ROOT / 'docs/analysis/es/009_DELIVERY.json').read_text())
    manifest = json.loads((ROOT / 'languages/es-maint/system_texts.json').read_text())
    routes = {int(e['offset'], 16): e for e in manifest['entries']}
    fixed = {0x417200, 0x417457, 0x41778A, 0x417D90}
    for entry in report['entries']:
        if entry['translation'] is None:
            continue
        key = int(entry['offset'], 16)
        route = routes[key]
        assert route['source_hex'] == entry['source_hex']
        assert route['pointer_offsets'] == entry['pointer_offsets']
        if key in fixed:
            raw = TextEncoder.encode_pokemon(entry['translation'].replace('\\n', '\n'),
                                             skip_aliases=SPANISH_GLYPH_CHARS)
            assert len(raw) < route['fixed_capacity']


def test_party_actions_fit_the_smallest_native_window():
    """La fenêtre 7 tuiles garde huit pixels pour son curseur et sa marge."""
    manifest = json.loads((ROOT / 'languages/es-maint/system_texts.json').read_text())
    combined, _ = _load_combined(ROOT / 'languages/es-maint/combined_es-maint.txt')
    keys = {0x41697E, 0x416984, 0x41698D, 0x416994, 0x4169A3,
            0x4169A9, 0x4169B2, 0x4169B7, 0x4169BC}
    entries = {int(e['offset'], 16): e for e in manifest['entries']}
    guards = {int(e['offset'], 16): e for e in manifest['engine_guards']}

    assert bytes.fromhex(guards[0x45A148]['hex'])[3] == 7
    for key in keys:
        layout = entries[key]['layout']
        font = bytes.fromhex(layout['glyph_widths_hex'])
        raw = TextEncoder.encode_pokemon(combined[key])[:-1]
        assert sum(font[glyph] for glyph in raw) <= layout['max_width'] == 48


def test_plain_pc_messages_share_the_qualified_144_pixel_window():
    """Les messages sans F7 ont les mêmes limites PC que les sept formatés."""
    report = json.loads((ROOT / 'docs/analysis/es/009_DELIVERY.json').read_text())
    manifest = json.loads((ROOT / 'languages/es-maint/system_texts.json').read_text())
    routes = {int(e['offset'], 16): e for e in manifest['entries']}
    selected = [e for e in report['entries'] if e['translation'] is not None
                and 0x418208 <= int(e['offset'], 16) <= 0x418452
                and b'\xf7' not in bytes.fromhex(e['source_hex'])]

    assert len(selected) == 19
    for entry in selected:
        layout = routes[int(entry['offset'], 16)]['layout']
        raw = TextEncoder.encode_pokemon(entry['translation'], skip_aliases=SPANISH_GLYPH_CHARS)
        font = bytes.fromhex(layout['glyph_widths_hex'])
        assert layout['initial_font'] == 1 and layout['max_lines'] == 1
        assert len(raw) <= layout['max_bytes'] == 80
        assert sum(font[glyph] for glyph in raw[:-1]) <= layout['max_width'] == 144


def test_standard_strings_fit_the_smallest_script_buffer():
    """Les noms complets ne doivent pas dépasser STR_VAR_2/3 (20 octets)."""
    report = json.loads((ROOT / 'docs/analysis/es/009_DELIVERY.json').read_text())
    table = report['consumer_tables']['standard_strings']
    selected = [e for e in report['entries'] if 'std_id' in e]
    addresses = table['script_buffers'] + [table['next_buffer']]

    assert len(selected) == 28
    assert min(addresses[i+1] - addresses[i] for i in range(len(addresses)-1)) == 20
    for entry in selected:
        key = int(entry['offset'], 16)
        assert 0x3E06B8 + entry['std_id'] * 4 in entry['pointer_offsets'], hex(key)
        raw = TextEncoder.encode_pokemon(entry['translation'], skip_aliases=SPANISH_GLYPH_CHARS)
        assert len(raw) <= table['minimum_capacity'] == 20
