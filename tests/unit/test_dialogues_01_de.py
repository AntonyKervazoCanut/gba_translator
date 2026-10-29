"""B-673 : périmètre, commandes ordonnées et vérification de la ROM finale."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pytest

from src.core.dialogue_linewrap import GLYPH_WIDTHS, VARIABLE_WIDTH, line_widths
from src.core.text_codec import GERMAN_UMLAUT_CHARS, TextEncoder

ROOT = Path(__file__).resolve().parents[2]
ROWS = json.loads((ROOT / 'docs/analysis/673_DIALOGUES_01_DE.json').read_text())


def encode(text: str) -> bytes:
    """Encode les retours et les commandes brutes sans perdre les umlauts."""
    return TextEncoder.encode_pokemon(
        text.replace(r'\n', '\n').replace(r'\l', '<0xFA>').replace(r'\p', '<0xFB>'),
        skip_aliases=GERMAN_UMLAUT_CHARS,
    )


def commands(data: bytes) -> list[bytes]:
    """Lit atomiquement les commandes présentes dans ce lot (FC01 et FD)."""
    result = []
    index = 0
    while index < len(data):
        byte = data[index]
        if byte == 0xFC:
            assert data[index + 1] == 1, 'Nouvelle commande : revoir son arité'
            result.append(data[index:index + 3])
            index += 3
        elif byte == 0xFD:
            result.append(data[index:index + 2])
            index += 2
        else:
            assert byte not in (0xF7, 0xF8, 0xF9), 'Nouvelle commande à qualifier'
            index += 1
    return result


def display_widths(data: bytes) -> list[int]:
    """Mesure aussi les glyphes bruts, notamment l'ellipse B0 de six pixels."""
    widths = [0]
    index = 0
    while index < len(data):
        byte = data[index]
        if byte == 0xFC:
            assert data[index + 1] == 1
            index += 3
            continue
        if byte == 0xFD:
            widths[-1] += VARIABLE_WIDTH
            index += 2
            continue
        if byte in (0xFA, 0xFB, 0xFE):
            widths.append(0)
        elif byte != 0xFF:
            widths[-1] += GLYPH_WIDTHS[byte]
        index += 1
    return widths


def without_wrapping(data: bytes) -> bytes:
    """Neutralise FE/FA en espaces GBA (00), sans toucher aux pages FB."""
    return re.sub(b'\x00+', b'\x00', data.replace(b'\xfe', b'\x00').replace(b'\xfa', b'\x00'))


def test_scope_is_complete_and_unique():
    offsets = [int(row['offset'], 16) for row in ROWS]
    assert len(offsets) == len(set(offsets)) == 300
    assert offsets[0] == 0x4ABE2F and offsets[-1] == 0x7BA306
    assert all(row['decision'] and row['motif'] and row['scene'] for row in ROWS)
    assert sum(row['decision'] == 'corrigé' for row in ROWS) == 162
    assert sum(row['decision'] == 'besoin de patch séparé' for row in ROWS) == 20


@pytest.mark.parametrize('row', ROWS, ids=lambda row: row['offset'])
def test_winning_text_and_commands(row):
    offset = int(row['offset'], 16)
    matches = re.findall(
        rf'^0x0*{offset:x}: (.*)$',
        (ROOT / 'languages/de/combined_de.txt').read_text(), re.M | re.I,
    )
    assert (matches[-1] if matches else None) == row['de']
    if not row['decision'].startswith('corrigé'):
        return
    data = encode(row['de'])
    assert max(display_widths(data)) <= 192
    assert commands(data) == commands(bytes.fromhex(row['source_hex']))
    assert data.count(b'\xfb') == bytes.fromhex(row['source_hex']).count(b'\xfb')
    assert not re.search(r'\{[^}]*\}', row['de'])
    expanded = row['de'].replace(r'\n', '\n').replace(r'\l', '<0xFA>').replace(r'\p', '<0xFB>')
    assert max(line_widths(expanded)) <= 192
    if row['scene'].startswith('Sac :'):
        assert len(expanded.splitlines()) <= 3


@pytest.fixture(scope='module')
def rom_pair():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    assert hashlib.sha256(source).hexdigest() == ROWS[0]['canonical_sha256']
    return source, (ROOT / 'output/roms/GenedRom-de.gba').read_bytes()


@pytest.mark.rom
@pytest.mark.parametrize('row', ROWS, ids=lambda row: row['offset'])
def test_final_rom_and_original_pointer_sites(row, rom_pair):
    source, built = rom_pair
    offset = int(row['offset'], 16)
    original = bytes.fromhex(row['source_hex'])
    assert source[offset:offset + len(original)] == original
    for site_hex in row['refs']:
        site = int(site_hex, 16)
        assert int.from_bytes(source[site:site + 4], 'little') == offset + 0x08000000
    if row.get('rom_checks') is None:
        pytest.fail(f"Qualification binaire manquante : {row['offset']}")
    for check in row['rom_checks']:
        site = int(check['site'], 16)
        target = int.from_bytes(built[site:site + 4], 'little') - 0x08000000
        assert 0 <= target < len(built)
        expected = bytes.fromhex(check['expected_hex'])
        assert built[target:target + len(expected)] == expected
        if row['decision'].startswith('corrigé'):
            assert commands(expected) == commands(original)
            assert without_wrapping(expected) == without_wrapping(encode(row['de']))
            assert max(display_widths(expected)) <= 192


@pytest.mark.rom
def test_corrected_text_does_not_overwrite_unresolved_suffix(rom_pair):
    """Les suffixes à repointer ne doivent pas tomber dans une nouvelle chaîne DE."""
    _, built = rom_pair
    unresolved_targets = [
        int.from_bytes(built[int(site, 16):int(site, 16) + 4], 'little') - 0x08000000
        for row in ROWS if row['decision'] == 'besoin de patch séparé'
        for site in row['refs']
    ]
    for row in ROWS:
        if row['decision'] != 'corrigé':
            continue
        for check in row['rom_checks']:
            site = int(check['site'], 16)
            start = int.from_bytes(built[site:site + 4], 'little') - 0x08000000
            end = start + len(bytes.fromhex(check['expected_hex']))
            assert not any(start <= target < end for target in unresolved_targets), row['offset']


def test_encoded_ellipsis_is_counted_and_control_arguments_are_atomic():
    # B0 est imprimable ; FA à l'intérieur de FC01/FD n'est pas un retour.
    assert display_widths(bytes.fromhex('b0ff')) == [6]
    assert commands(bytes.fromhex('fc01fafdfaff')) == [bytes.fromhex('fc01fa'), bytes.fromhex('fdfa')]
    assert display_widths(bytes.fromhex('fc01fafdfab0ff')) == [VARIABLE_WIDTH + 6]
