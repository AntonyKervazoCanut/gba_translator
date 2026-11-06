"""Fenêtres opt-in : police effective, colonnes et expansion bornée."""
import importlib
import json
from pathlib import Path

import pytest

Builder = importlib.import_module('src.translators.19_build_translated_rom_generic').TranslatedROMBuilder
ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def layout():
    fonts = json.loads((ROOT / 'languages/es-maint/text_aliases.json').read_text())['fonts']
    return {'engine_layout': True, 'initial_font': 2,
            'engine_fonts': {'0': fonts['small'], '2': fonts['normal']},
            'max_expanded_bytes': 128, 'buffers': {'0': {'max_width': 60, 'max_bytes': 10}}}


def test_clear_to_uses_column_and_current_font(layout):
    raw = bytes.fromhex('bbfc1320fc0600a1ff')
    widths = Builder._encoded_layout_widths(raw, layout)
    small = bytes.fromhex(layout['engine_fonts']['0']['hex'])
    assert widths == [32 + small[0xA1]]


def test_name_cannot_push_price_even_when_window_has_room(layout):
    with pytest.raises(ValueError, match='colonne'):
        Builder._encoded_layout_widths(bytes.fromhex('bbbbbbbbbbbbbbbbfc1308a1ff'), layout)


def test_font_switch_applies_before_name_and_price(layout):
    raw = bytes.fromhex('fc0600bbbbfc1320a1ff')
    small = bytes.fromhex(layout['engine_fonts']['0']['hex'])
    assert Builder._encoded_layout_widths(raw, layout) == [32 + small[0xA1]]


def test_f7_expands_one_argument_and_preserves_following_space(layout):
    raw = bytes.fromhex('f70000bbff')
    normal = bytes.fromhex(layout['engine_fonts']['2']['hex'])
    assert Builder._encoded_layout_widths(raw, layout) == [60 + normal[0] + normal[0xBB]]


@pytest.mark.parametrize('raw', ['f701ff', 'fc0605bbff', 'fc0801bbff', 'f7', 'fc13', 'f800ff', 'fd01ff'])
def test_unknown_or_truncated_engine_command_rejected(layout, raw):
    with pytest.raises(ValueError):
        Builder._encoded_layout_widths(bytes.fromhex(raw), layout)


def test_expanded_buffer_capacity_includes_terminator(layout):
    layout['max_expanded_bytes'] = 11
    assert Builder._encoded_layout_widths(bytes.fromhex('f700ff'), layout) == [60]
    with pytest.raises(ValueError, match='expans'):
        Builder._encoded_layout_widths(bytes.fromhex('f700bbff'), layout)


def test_legacy_measurement_remains_unchanged():
    assert Builder._encoded_layout_widths(bytes.fromhex('bbfc1320fc0600a1ff')) == [12]


def test_symbols_use_the_effective_font_and_keypad_metrics(layout):
    layout['keypad_widths'] = [8, 8, 16]
    glyphs = bytes.fromhex(layout['engine_fonts']['0']['hex'])
    assert Builder._encoded_layout_widths(bytes.fromhex('fc0600f802f905ff'), layout) == [16 + glyphs[0x105]]


def test_price_at_exact_column_boundary_is_valid(layout):
    width = bytes.fromhex(layout['engine_fonts']['2']['hex'])[0xBB]
    assert Builder._encoded_layout_widths(bytes([0xBB, 0xFC, 0x13, width, 0xFF]), layout) == [width]


@pytest.mark.parametrize('raw', ['bbffbb', 'bb', 'faff', 'fbff'])
def test_unterminated_paginated_or_embedded_terminator_rejected(layout, raw):
    with pytest.raises(ValueError):
        Builder._encoded_layout_widths(bytes.fromhex(raw), layout)


@pytest.mark.parametrize('original,changed', [
    ('fc1320fc0600a1ff', 'fc1321fc0600a1ff'),
    ('fc1320fc0600a1ff', 'fc1320fc0601a1ff'),
    ('f700ff', 'f701ff'), ('fd01ff', 'fd02ff'),
    ('f800ff', 'f801ff'), ('f905ff', 'f906ff'),
    ('bbfafbff', 'bbfbfaff'),
])
def test_strict_control_flow_rejects_every_argument_and_page_order(original, changed):
    from src.core.item_description_routes import SystemTextRoutes

    item = {'offset': 1, 'original_text': 'source', 'english_raw_bytes': original,
            'translation': ''.join(f'<0x{b:02X}>' for b in bytes.fromhex(changed)[:-1]),
            'preserve_control_flow': True}
    with pytest.raises(ValueError, match='commandes'):
        SystemTextRoutes.normalize(item)


def test_control_flow_rejects_512_byte_overrun():
    from src.core.item_description_routes import SystemTextRoutes

    with pytest.raises(ValueError, match='512'):
        SystemTextRoutes.normalize({'offset': 1, 'original_text': 'source',
                                    'english_raw_bytes': 'bbff', 'translation': 'A' * 512,
                                    'preserve_control_flow': True})


def test_small_font_name_fits_where_normal_font_would_cross_column(layout):
    raw = bytes.fromhex('fc0600') + b'\xbb' * 10 + bytes.fromhex('fc1332a1ff')
    assert Builder._encoded_layout_widths(raw, layout) == [55]
    with pytest.raises(ValueError, match='colonne'):
        Builder._encoded_layout_widths(raw[3:], layout)
