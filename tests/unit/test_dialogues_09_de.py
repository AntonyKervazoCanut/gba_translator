"""B-681 : les 300 décisions et les octets réellement accessibles du lot 09."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pytest

from scripts.apply_combined_fr import _load_combined, _normalize_text
from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.dialogue_linewrap import GLYPH_WIDTHS, VARIABLE_WIDTH
from src.core.text_codec import GERMAN_UMLAUT_CHARS, TextEncoder

ROOT = Path(__file__).resolve().parents[2]
ROWS = json.loads((ROOT / 'docs/analysis/681_DIALOGUES_09_DE.json').read_text())


def encode(text: str) -> bytes:
    """Encode les contrôles explicites et conserve les glyphes allemands."""
    return TextEncoder.encode_pokemon(
        text.replace(r'\n', '\n').replace(r'\l', '<0xFA>').replace(r'\p', '<0xFB>'),
        skip_aliases=GERMAN_UMLAUT_CHARS,
    )


def commands(data: bytes) -> list[list[int]]:
    """Isole les commandes atomiques, hors défilement et saut de page."""
    return [c for c in _extract_control_sequences_from_raw(data) if c[0] not in (0xFA, 0xFB)]


def widths(data: bytes) -> list[int]:
    """Compte les pixels imprimés, les icônes et les buffers dynamiques."""
    result = [0]
    i = 0
    while i < len(data):
        byte = data[i]
        if byte == 0xFC:
            assert data[i + 1] in (1, 8, 9)
            i += 2 if data[i + 1] == 9 else 3
            continue
        if byte in (0xF7, 0xF8, 0xF9, 0xFD):
            result[-1] += VARIABLE_WIDTH if byte == 0xFD else 8
            i += 2
            continue
        if byte in (0xFA, 0xFB, 0xFE):
            result.append(0)
        elif byte != 0xFF:
            result[-1] += GLYPH_WIDTHS[byte]
        i += 1
    return result


def without_wrapping(data: bytes) -> bytes:
    """Compare le texte et les pages sans imposer une adresse de relogement."""
    space = bytes([0])
    return re.sub(space + b'+', space, data.replace(bytes([0xFE]), space).replace(bytes([0xFA]), space))


def test_scope_and_documented_decisions():
    offsets = [int(row['offset'], 16) for row in ROWS]
    assert len(offsets) == len(set(offsets)) == 300
    assert offsets[0] == 0x1F54752 and offsets[-1] == 0x1F8E271
    assert 0x7A823B not in offsets
    assert all(row['decision'] and row['motif'] and row['scene'] for row in ROWS)


def test_last_winning_values():
    actual, _ = _load_combined(ROOT / 'languages/de/combined_de.txt')
    for row in ROWS:
        expected = row['de']
        if expected is not None:
            expected = _normalize_text(expected)
        assert actual.get(int(row['offset'], 16)) == expected, row['offset']


@pytest.mark.parametrize('row', [r for r in ROWS if r.get('source_modified')], ids=lambda r: r['offset'])
def test_corrected_commands_pages_and_boxes(row):
    actual = encode(row['de'])
    source = bytes.fromhex(row['source_hex'])
    assert commands(actual) == commands(source)
    assert actual.count(b'\xfb') == source.count(b'\xfb')
    assert '{' not in row['de']
    assert max(widths(actual)) <= (232 if row['offset'] in ('0x1F6822D', '0x1F6834C') else 192)
    if int(row['offset'], 16) <= 0x1F54B25:
        assert max(widths(actual)) <= 172
        assert actual.count(b'\xfe') <= 2
        assert b'\xfa' not in actual


@pytest.mark.rom
def test_final_rom_all_recorded_pointer_sites():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-de.gba').read_bytes()
    assert hashlib.sha256(source).hexdigest() == ROWS[0]['canonical_sha256']
    for row in ROWS:
        offset = int(row['offset'], 16)
        original = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(original)] == original
        for site_hex in row['refs']:
            site = int(site_hex, 16)
            assert int.from_bytes(source[site:site + 4], 'little') == offset + 0x08000000
        assert 'rom_checks' in row
        if row['decision'] == 'corrigé':
            assert row['rom_checks'], row['offset']
        for check in row['rom_checks'] + row.get('suffix_checks', []):
            site = int(check['site'], 16)
            target = int.from_bytes(built[site:site + 4], 'little') - 0x08000000
            assert 0 <= target < len(built), row['offset']
            expected = bytes.fromhex(check['expected_hex'])
            assert built[target:target + len(expected)] == expected, row['offset']
            if row['decision'] == 'corrigé':
                assert commands(expected) == commands(original)
                assert without_wrapping(expected) == without_wrapping(encode(row['de'])), row['offset']
                assert max(widths(expected)) <= (232 if row['offset'] in ('0x1F6822D', '0x1F6834C') else 192)
