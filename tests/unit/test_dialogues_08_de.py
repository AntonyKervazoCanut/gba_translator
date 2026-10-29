"""B-680 : décisions exhaustives, commandes et pointeurs de dialogues-08."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pytest

from src.core.dialogue_linewrap import GLYPH_WIDTHS, VARIABLE_WIDTH
from src.core.text_codec import GERMAN_UMLAUT_CHARS, TextEncoder

ROOT = Path(__file__).resolve().parents[2]
ROWS = json.loads((ROOT / 'docs/analysis/680_DIALOGUES_08_DE.json').read_text())


def encode(text):
    return TextEncoder.encode_pokemon(
        text.replace(r'\n', '\n').replace(r'\l', '<0xFA>').replace(r'\p', '<0xFB>'),
        skip_aliases=GERMAN_UMLAUT_CHARS,
    )


def inspect(data):
    """Consomme les commandes atomiquement, y compris leurs arguments FA/FB."""
    widths, commands, pages = [0], [], 0
    index = 0
    while index < len(data):
        byte = data[index]
        size = 1
        if byte == 0xFC:
            assert data[index + 1] in (1, 3, 6, 8)
            size = 3
        elif byte in (0xFD, 0xF8, 0xF9):
            size = 2
        elif byte == 0xF7:
            size = 3
        if size > 1:
            commands.append(data[index:index + size])
            if byte == 0xFD:
                widths[-1] += VARIABLE_WIDTH
            elif byte == 0xF8:
                widths[-1] += 8
        elif byte in (0xFA, 0xFB, 0xFE):
            widths.append(0)
            pages += byte == 0xFB
        elif byte != 0xFF:
            widths[-1] += GLYPH_WIDTHS[byte]
        index += size
    return commands, pages, max(widths)


def unwrapped(data):
    return re.sub(b'\x00+', b'\x00', data.replace(b'\xfe', b'\x00').replace(b'\xfa', b'\x00'))


def test_complete_scope():
    offsets = [int(row['offset'], 16) for row in ROWS]
    assert len(offsets) == len(set(offsets)) == 300
    assert offsets[0] == 0x1F2FE44 and offsets[-1] == 0x1F54716
    assert all(row['decision'] and row['motif'] and row['scene'] and row['genre'] for row in ROWS)
    assert 0x7A823B not in offsets
    assert sum(len(row['refs']) for row in ROWS) == 407


def test_consumers_without_relocation_fit_the_original_slots():
    # Ces anciens consommateurs ignoraient la chaîne relocalisée : l'un
    # affichait un fragment DE et les deux autres restaient en anglais.
    for row in ROWS:
        if int(row['offset'], 16) in (0x1F35323, 0x1F4E4E2):
            assert len(encode(row['de'])) <= len(bytes.fromhex(row['source_hex']))


@pytest.mark.parametrize('row', ROWS, ids=lambda row: row['offset'])
def test_winning_text_controls_and_boxes(row):
    offset = int(row['offset'], 16)
    matches = re.findall(
        rf'^0x0*{offset:x}: (.*)$',
        (ROOT / 'languages/de/combined_de.txt').read_text(), re.M | re.I,
    )
    assert (matches[-1] if matches else None) == row['de']
    if not row.get('changed'):
        return
    data = encode(row['de'])
    source = bytes.fromhex(row['source_hex'])
    commands, pages, width = inspect(data)
    assert commands == inspect(source)[0]
    assert pages == inspect(source)[1]
    assert width <= 192
    assert len(data) == row['encoded_bytes']
    assert not re.search(r'\{[^}]*\}', row['de'])
    for page in re.split(b'\xfb', data):
        assert page.count(b'\xfe') <= 1


@pytest.mark.rom
@pytest.mark.parametrize('row', ROWS, ids=lambda row: row['offset'])
def test_injected_bytes_and_all_original_references(row):
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-de.gba').read_bytes()
    assert hashlib.sha256(source).hexdigest() == row['canonical_sha256']
    offset = int(row['offset'], 16)
    original = bytes.fromhex(row['source_hex'])
    assert source[offset:offset + len(original)] == original
    assert row.get('rom_checks') is not None
    for site_hex in row['refs']:
        site = int(site_hex, 16)
        assert int.from_bytes(source[site:site + 4], 'little') == offset + 0x08000000
    for check in row['rom_checks']:
        site = int(check['site'], 16)
        target = int.from_bytes(built[site:site + 4], 'little') - 0x08000000
        # Le placement peut bouger quand un autre lot est intégré : suivre
        # le pointeur vivant plutôt qu'une adresse de destination figée.
        assert 0 <= target < len(built)
        expected = bytes.fromhex(check['expected_hex'])
        if row.get('acheminement'):
            # B-1016 doit pouvoir acheminer ce texte sans que ce témoin
            # historique impose de conserver l'anglais pour toujours.
            expected = built[target:built.index(b'\xff', target) + 1]
            if expected == original:
                continue
        else:
            assert built[target:target + len(expected)] == expected
        if row.get('changed'):
            assert unwrapped(expected) == unwrapped(encode(row['de']))
            assert inspect(expected)[:2] == inspect(original)[:2]
            assert inspect(expected)[2] <= 192
