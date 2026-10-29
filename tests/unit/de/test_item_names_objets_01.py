"""Cellules réelles B-1026 : atomicité, bornes et accès vivant."""
import json
from pathlib import Path

import pytest

from languages.de.patches import item_names as patch
from languages.de.item_name_cells import OFFSETS
from scripts import apply_combined_fr, apply_inline_overrides_fr

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = json.loads((ROOT / 'languages/de/data/item_names_objets_01.json').read_text())


def fixture_rom():
    data = bytearray(0x879850)
    data[0x876200:] = (ROOT / 'tests/unit/fixtures/item_names_objets_01.bin').read_bytes()
    data[0x9A8D8:0x9A8DC] = bytes.fromhex('00628708')
    return data


def targets():
    return {int(row['offset'], 16): 'Prüfung' for row in MANIFEST['entries']}


def test_atomic_bounded_write_and_idempotence():
    rom = fixture_rom()
    original = bytes(rom)
    assert patch.apply_scoped_item_names(rom, original, targets()) == 122
    allowed = set()
    for row in MANIFEST['entries']:
        offset = int(row['offset'], 16)
        assert patch.decode_name(rom, offset) == 'Prüfung'
        allowed.update(range(offset, offset + 14))
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(original, rom)))
    assert patch.apply_scoped_item_names(rom, original, targets()) == 0


@pytest.mark.parametrize('fault', ['preimage', 'target', 'pointer', 'long', 'missing', 'control'])
def test_validation_precedes_every_write(fault):
    source = fixture_rom()
    rom = bytearray(source)
    translations = targets()
    last = max(translations)
    if fault == 'preimage':
        source[last] ^= 1
    elif fault == 'target':
        rom[last] ^= 1
    elif fault == 'pointer':
        rom[0x9A8D8] ^= 1
    elif fault == 'long':
        translations[last] = 'X-Verteidigung'
    elif fault == 'missing':
        del translations[last]
    else:
        translations[last] = '{PLAYER}'
    before = bytes(rom)
    with pytest.raises(ValueError):
        patch.apply_scoped_item_names(rom, source, translations)
    assert rom == before


def test_generic_injection_excludes_cells_and_never_uses_raw_references():
    exclusions = apply_combined_fr._dedicated_offsets_for_combined(
        ROOT / 'languages/de/combined_de.txt'
    )
    assert exclusions == OFFSETS
    assert apply_inline_overrides_fr._dedicated_offsets_for_combined(
        ROOT / 'languages/de/combined_de.txt'
    ) == OFFSETS
    combined = {0x876284: 'Superball', 0x10: 'Unverändert'}
    rows = [{'offset': '0x876284', 'translation': 'ancienne valeur',
             'pointer_offsets': ['0x009AF055']}]
    assert apply_combined_fr._exclude_dedicated_offsets(combined, rows, exclusions) == 1
    assert combined == {0x10: 'Unverändert'}
    assert rows[0]['translation'] == ''
    assert not apply_combined_fr._dedicated_offsets_for_combined(
        ROOT / 'languages/it/combined_it.txt'
    )


def test_combined_targets_fit_real_cells_and_hard_stone_stays_correct():
    from languages.de.patches.fixed_table_names import NAME_FIXES
    combined, _ = apply_combined_fr._load_combined(ROOT / 'languages/de/combined_de.txt')
    rom = fixture_rom()
    assert patch.apply_scoped_item_names(rom, bytes(rom), combined) == 122
    patch.apply_item_name_fixes(rom, patch.ALL_NAMES)
    assert patch.decode_name(rom, 0x878510) == 'Granitstein'
    assert all(not (offset <= 0x878510 < offset + stride)
               for offset, (_, _, stride) in NAME_FIXES.items())
