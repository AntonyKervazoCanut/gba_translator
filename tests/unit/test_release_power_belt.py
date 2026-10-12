"""Régression #209 : les patchs distribués contiennent le nom traduit."""

from pathlib import Path

import pytest

from src.core.bps import _decode_number, inspect_bps_patch


@pytest.mark.parametrize(
    ('language', 'expected'),
    [('fr', 'Ceint. Pouv.'), ('it', 'Vigorfascia'), ('de', 'Machtgurt')],
)
def test_tracked_patch_contains_translated_power_belt(language, expected):
    """Contrôle la cellule cible du bundle public sans ROM privée."""
    from importlib import import_module

    module = import_module(f'languages.{language}.patches.item_names')
    patch = (Path(__file__).resolve().parents[2] / 'patches'
             / f'pokemon_unbound_{language}.bps').read_bytes()
    inspect_bps_patch(patch)
    limit = len(patch) - 12
    cursor = 4
    _, cursor = _decode_number(patch, cursor, limit)
    _, cursor = _decode_number(patch, cursor, limit)
    metadata_length, cursor = _decode_number(patch, cursor, limit)
    cursor += metadata_length
    target_offset = 0
    cell_offset = 0x878C1C
    translated = module.encode(expected) + b'\xff'
    # SourceRead conserve les octets du nom anglais connu de cette cellule.
    cell = bytearray((module.encode('Power Belt') + b'\xff' * 14)[:len(translated)])

    while cursor < limit:
        action, cursor = _decode_number(patch, cursor, limit)
        length = (action >> 2) + 1
        kind = action & 3
        assert kind in (0, 1), 'Le bundle utilise SourceRead / TargetRead'
        if kind == 1:
            for offset in range(max(target_offset, cell_offset),
                                min(target_offset + length, cell_offset + len(cell))):
                index = offset - cell_offset
                cell[index] = patch[cursor + offset - target_offset]
            cursor += length
        target_offset += length

    assert bytes(cell) == translated
