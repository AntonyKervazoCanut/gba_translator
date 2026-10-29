"""B-670: scope, display budgets and live-ROM regression guards."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from src.core.pokedex import line_width
from src.core.text_codec import GERMAN_UMLAUT_CHARS, TextEncoder
from languages.de.patches.move_names import load_translations
from languages.fr.patches.move_names import resolve_live_base

ROOT = Path(__file__).resolve().parents[2]
ROWS = json.loads((ROOT / 'docs/analysis/combat_ui-04_de.json').read_text())


def test_qualification_covers_all_300_distinct_offsets():
    """The report must keep both endpoints and every original scoped offset."""
    offsets = [int(row['offset'], 16) for row in ROWS]
    assert len(offsets) == len(set(offsets)) == 300
    assert offsets[0] == 0xA3C9C6 and offsets[-1] == 0xA411BB
    assert sum(row['decision'] == 'corrigé' for row in ROWS) == 152
    assert sum(row['decision'] == 'déjà patché' for row in ROWS) == 148


@pytest.mark.parametrize('row', ROWS, ids=lambda row: row['offset'])
def test_scoped_winning_text_and_actual_line_budgets(row):
    """Measure explicit line breaks, rather than the possibility of rewrapping."""
    offset = int(row['offset'], 16)
    text = (ROOT / 'languages/de/combined_de.txt').read_text()
    matches = re.findall(rf'^0x0*{offset:x}: (.*)$', text, re.I | re.M)
    if row['decision'] == 'corrigé':
        assert matches[-1] == row['expected_rom']
        lines = matches[-1].replace('\\n', '\n').splitlines()
        assert len(lines) <= 5
        assert all(line_width(line) <= 122 for line in lines)
        assert not re.search(r'\{|<0x|\\[lp]', matches[-1])
    else:
        assert not matches  # Fixed names intentionally come from the official patch.
        assert load_translations()[offset] == row['expected_rom']
        encoded = TextEncoder.encode_pokemon(row['expected_rom'], skip_aliases=GERMAN_UMLAUT_CHARS)
        assert len(encoded) <= 13  # Includes 0xFF terminator.


@pytest.mark.rom
@pytest.mark.parametrize('row', ROWS, ids=lambda row: row['offset'])
def test_built_de_bytes_via_all_live_table_pointers(row):
    """Read the table actually dereferenced by the game after the entire build."""
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-de.gba').read_bytes()
    expected = TextEncoder.encode_pokemon(
        row['expected_rom'].replace('\\n', '\n'), skip_aliases=GERMAN_UMLAUT_CHARS,
    )
    if row['decision'] == 'corrigé':
        for index in row['move_indices']:
            site = 0x99F190 + 4 * index
            assert int.from_bytes(source[site:site + 4], 'little') - 0x08000000 == int(row['offset'], 16)
            target = int.from_bytes(built[site:site + 4], 'little') - 0x08000000
            assert 0 <= target < len(built) - len(expected)
            assert built[target:target + len(expected)] == expected
    else:
        target = resolve_live_base(built) + row['move_indices'][0] * 13
        assert built[target:target + len(expected)] == expected


@pytest.mark.rom
def test_corrected_descriptions_do_not_overlap_other_move_cells():
    """Every targeted span stays disjoint from every other live description."""
    built = (ROOT / 'output/roms/GenedRom-de.gba').read_bytes()
    spans = {}
    for index in range(1, 894):
        site = 0x99F190 + 4 * index
        target = int.from_bytes(built[site:site + 4], 'little') - 0x08000000
        if 0 <= target < len(built):
            end = built.find(b'\xff', target)
            assert end >= target
            spans[index] = (target, end + 1)
    for row in ROWS:
        if row['decision'] != 'corrigé':
            continue
        for index in row['move_indices']:
            start, end = spans[index]
            for other_start, other_end in spans.values():
                # Shared G-Max descriptions legitimately have identical pointers.
                assert (start, end) == (other_start, other_end) or end <= other_start or other_end <= start
