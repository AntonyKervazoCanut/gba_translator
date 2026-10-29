"""B-668 : buffers positionnels, aides Pokédex et boîtes des mémos."""
from pathlib import Path
import re

import pytest

from src.core.dialogue_linewrap import line_width

ROOT = Path(__file__).resolve().parents[3]


def translations():
    """Lit les valeurs gagnantes sans perdre les doublons du fichier source."""
    result = {}
    for line in (ROOT / 'languages/de/combined_de.txt').read_text().splitlines():
        match = re.match(r'(0x[0-9a-fA-F]+): (.*)', line)
        if match:
            result[int(match[1], 16)] = match[2]
    return result


@pytest.mark.parametrize('offset,count', [(0x41AF0C, 5), (0x41AF3E, 4)])
def test_combat_results_keep_every_positional_buffer(offset, count):
    """Le Pokémon adverse, le joueur et le gain ont chacun leur buffer."""
    text = translations()[offset]
    assert text.count('{DYNAMIC}') == count
    assert len(text.split(r'\n')) == 3
    # Deux noms de neuf glyphes larges doivent tenir sur une ligne.
    for line in text.split(r'\n'):
        assert line_width(line.replace('{DYNAMIC}', 'MMMMMMMMM')) <= 192


@pytest.mark.parametrize('offset', [0x41992F, 0x41996D, 0x4199AB, 0x4199F4])
def test_fateful_memos_fit_three_lines(offset):
    text = translations()[offset]
    assert re.findall(r'\{[^}]+\}', text) == [
        '{DYNAMIC}', '{DYNAMIC}', '{LV_2}', '{DYNAMIC}',
    ]
    lines = text.split(r'\n')
    assert len(lines) == 3
    assert max(line_width(line) for line in lines if '{' not in line) <= 192
    assert 'geschlüpft' in text


@pytest.mark.parametrize('offset,tokens', [
    (0x415F6C, ['{DPAD_LEFTRIGHT}', '{PLUS}', '{SE_SHOP}', '{B_BUTTON}']),
    (0x415FB3, ['{SE_SHOP}', '{B_BUTTON}']),
])
def test_pokedex_footer_keeps_all_actions(offset, tokens):
    assert re.findall(r'\{[^}]+\}', translations()[offset]) == tokens


def test_floor_labels_keep_ground_floor_and_basements_distinct():
    text = translations()
    assert text[0x41803A] == 'EG'
    assert text[0x41803D] == '1.OG'
    assert text[0x418059] == '10.OG'
    assert [text[o] for o in (0x41805D, 0x418061, 0x418065, 0x418069)] == [
        'U1', 'U2', 'U3', 'U4',
    ]
    # La copie sans référents n'est pas injectée comme une seconde table.
    assert all(offset not in text for offset in range(0x3FE9A9, 0x3FE9BF, 3))
