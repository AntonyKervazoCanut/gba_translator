"""B-1027 : raccordement borné, atomique et sans modification des métadonnées."""
from pathlib import Path

import pytest

from languages.de.patches import item_names_objets02 as patch
from scripts.check_translation_integrity import load_last_wins

ROOT = Path(__file__).resolve().parents[3]


def fixture_rom():
    """Charge les cellules et la routine réelles extraites de la ROM canonique."""
    fixture = ROOT / 'tests/unit/fixtures/item_names_objets02.bin'
    data = bytearray(0x87CDC4)
    raw = fixture.read_bytes()
    data[0x9A8CA:0x9A8DC] = raw[:18]
    data[0x879E28:0x87CDC4] = raw[18:]
    return data


def test_all_names_are_reached_and_only_name_cells_change():
    data = fixture_rom()
    before = bytes(data)
    texts, _ = load_last_wins(ROOT / 'languages/de/combined_de.txt')
    assert len(patch.EXPECTED_NAMES) == 104
    assert patch.apply(data, texts, bytes(fixture_rom())) == 104
    allowed = set()
    for offset in patch.EXPECTED_NAMES:
        assert (offset - 0x876200) % 44 == 0
        expected = patch.encode(texts[offset]) + b'\xff'
        assert data[offset:offset + len(expected)] == expected
        assert data[offset + 14:offset + 44] == before[offset + 14:offset + 44]
        allowed.update(range(offset, offset + 14))
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(before, data)))
    assert patch.apply(data, texts, bytes(fixture_rom())) == 0


@pytest.mark.parametrize('fault', ['missing', 'overflow', 'control', 'source', 'pointer'])
def test_invalid_batch_is_atomic(fault):
    data = fixture_rom()
    texts, _ = load_last_wins(ROOT / 'languages/de/combined_de.txt')
    offset = next(reversed(patch.EXPECTED_NAMES))
    if fault == 'missing':
        texts.pop(offset)
    elif fault == 'overflow':
        texts[offset] = 'W' * 14
    elif fault == 'control':
        texts[offset] = '{PLAYER}'
    elif fault == 'source':
        data[offset] = 0
    else:
        data[0x9A8D8] ^= 1
    before = bytes(data)
    with pytest.raises((ValueError, KeyError)):
        patch.apply(data, texts, bytes(fixture_rom()))
    assert data == before


@pytest.mark.rom
def test_built_rom_preserves_metadata_and_196_qualified_neighbors():
    import json

    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-de.gba').read_bytes()
    before = (ROOT / 'output/roms/GenedRom-de.gba.objets02.bak').read_bytes()
    texts, _ = load_last_wins(ROOT / 'languages/de/combined_de.txt')
    scope = json.loads((ROOT / 'tests/unit/fixtures/item_names_objets02_scope.json').read_text())
    assert len(scope) == 300
    assert built[0x9A8CA:0x9A8DC] == patch.ROUTINE
    untouched = 0
    for row in scope:
        offset = int(row['offset'], 16)
        if offset in patch.EXPECTED_NAMES:
            expected = (patch.encode(texts[offset]) + b'\xff').ljust(14, b'\x00')
        else:
            expected = bytes.fromhex(row['name_hex_before'])
            untouched += 1
        assert built[offset:offset + 14] == expected, row['offset']
        if offset in patch.EXPECTED_NAMES:
            assert built[offset + 14:offset + 44] == before[offset + 14:offset + 44]
        assert built[offset + 14:offset + 20] == source[offset + 14:offset + 20]
        assert built[offset + 24:offset + 44] == source[offset + 24:offset + 44]
    assert untouched == 196
    # Sur toute la ROM, le patch lui-même ne change que les 104 noms.
    replay = bytearray(before)
    assert patch.apply(replay, texts, source) == 104
    for offset in patch.EXPECTED_NAMES:
        assert replay[offset:offset + 44] == built[offset:offset + 44]
        replay[offset:offset + 14] = before[offset:offset + 14]
    assert replay == before


def test_scope_and_versioned_targets_stay_exact():
    import json
    from languages.de.item_name_cells import OFFSETS

    rows = json.loads((ROOT / 'docs/analysis/1027_OBJETS_02_RACCORDEMENT_DE.json').read_text())['entries']
    targets = {int(row['offset'], 16): row['target'] for row in rows}
    texts, _ = load_last_wins(ROOT / 'languages/de/combined_de.txt')
    assert set(targets) == set(patch.EXPECTED_NAMES)
    assert not set(targets) & OFFSETS
    assert {offset: texts[offset] for offset in targets} == targets
