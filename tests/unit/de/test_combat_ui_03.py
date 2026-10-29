"""B-669 : périmètre fermé, commandes et budgets des textes DE."""
from __future__ import annotations

import importlib
import json
import re
from functools import lru_cache
from pathlib import Path

import pytest

from src.core.dialogue_linewrap import line_width
from src.core.text_codec import GERMAN_UMLAUT_CHARS, TextEncoder

ROOT = Path(__file__).resolve().parents[3]
ROWS = json.loads((ROOT / 'tests/unit/fixtures/de_combat_ui_03.json').read_text())
BUILDER = importlib.import_module('src.translators.19_build_translated_rom_generic').TranslatedROMBuilder


@lru_cache(maxsize=1)
def combined() -> dict[int, str]:
    """Résout la dernière occurrence sans normaliser les espaces du texte."""
    entries = {}
    for line in (ROOT / 'languages/de/combined_de.txt').read_text().splitlines():
        match = re.match(r'^(0x[0-9a-fA-F]+): ?(.*)$', line)
        if match:
            entries[int(match[1], 16)] = match[2]
    return entries


def encoded(text: str) -> bytes:
    """Encode les ruptures et les umlauts comme le build allemand."""
    for escape, raw in [(r'\n', '\n'), (r'\l', '<0xFA>'), (r'\p', '<0xFB>')]:
        text = text.replace(escape, raw)
    return TextEncoder.encode_pokemon(text, skip_aliases=GERMAN_UMLAUT_CHARS)


def commands(raw: bytes) -> list[bytes]:
    """Extrait commandes et ruptures, sans confondre arguments et caractères."""
    result = []
    index = 0
    while index < len(raw):
        code = raw[index]
        if code == 0xFF:
            break
        size = 1
        if code == 0xFC:
            size = 2 + BUILDER.FC_ARG_COUNTS.get(raw[index + 1], 0)
        elif code in BUILDER.RAW_ARG_PREFIXES:
            size += BUILDER.RAW_ARG_PREFIXES[code]
        if code >= 0xF7:
            result.append(raw[index:index + size])
        index += size
    return result


def test_closed_scope_and_individual_decisions():
    """Les 300 lignes sont uniques, qualifiées et reliées au rapport."""
    assert len(ROWS) == len({r['offset'] for r in ROWS}) == 300
    report = (ROOT / 'docs/22_DE_COMBAT_UI_03.md').read_text()
    for row in ROWS:
        assert row['reason'] and row['scene']
        assert f"| `{row['offset']}` |" in report
    assert sum(r['decision'] == 'corrigé' for r in ROWS) == 204
    deferred = [r for r in ROWS if r['decision'] == 'besoin de patch séparé']
    assert len(deferred) == 67
    for row in deferred:
        assert row['proposed_after'] and row['after'] is None
        assert int(row['offset'], 16) not in combined()


def test_deferred_cases_preserve_the_verified_pipeline_diagnosis():
    """Distingue extraction absente/vide et rewrap, sans masquer une exclusion."""
    deferred = [row for row in ROWS if row['decision'] == 'besoin de patch séparé']
    descriptions = [row for row in deferred if row['move_ids']]
    assert len(descriptions) == 49
    assert sum('extraction EN vide' in row['reason'] for row in descriptions) == 5
    assert sum('offset absent' in row['reason'] for row in descriptions) == 44
    assert sum('rewrap automatique' in row['reason'] for row in deferred) == 18
    assert all('B-1013' in row['reason'] for row in deferred)


@pytest.mark.parametrize('row', [r for r in ROWS if r['decision'] == 'corrigé'], ids=lambda r: r['offset'])
def test_source_controls_and_boxes(row):
    """Le texte gagnant conserve les commandes EN et les budgets de fenêtre."""
    actual = combined()[int(row['offset'], 16)]
    assert actual == row['after']
    raw = encoded(actual)
    assert commands(raw) == commands(bytes.fromhex(row['hex']))
    if row['move_ids']:
        lines = actual.split(r'\n')
        assert len(lines) <= 5
        assert max(map(line_width, lines)) <= 122
    elif row['offset'] == '0xA37377':
        assert len(raw) <= 17
    else:
        # Enlever les commandes de couleur et réserver la place des boutons.
        visible = re.sub(r'<0xFC><0x[0-9A-F]{2}><0x[0-9A-F]{2}>', '', actual)
        visible = re.sub(r'<0xF[78]><0x[0-9A-F]{2}>', '  ', visible)
        assert max(line_width(line) for line in re.split(r'\\[nlp]', visible)) <= 208


@pytest.mark.rom
@pytest.mark.parametrize('row', [r for r in ROWS if r['decision'] == 'corrigé'], ids=lambda r: r['offset'])
def test_built_rom_at_live_references(row):
    """Chaque référence EN doit atteindre les octets DE exacts après build."""
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    rom = (ROOT / 'output/roms/GenedRom-de.gba').read_bytes()
    offset = int(row['offset'], 16)
    expected = encoded(row['after'])
    assert source[offset:offset + len(bytes.fromhex(row['hex']))].hex() == row['hex']
    if row['offset'] == '0xA37377':
        targets = [offset]  # table indexée, pas un pointeur par nom
    else:
        assert row['refs'], row['offset']
        targets = [int.from_bytes(rom[p:p + 4], 'little') - 0x08000000 for p in row['refs']]
    for target in targets:
        assert 0 <= target <= len(rom) - len(expected)
        assert rom[target:target + len(expected)] == expected, (row['offset'], hex(target))
