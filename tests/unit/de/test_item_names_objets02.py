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
    assert patch.apply(data, texts) == 104
    allowed = set()
    for offset in patch.EXPECTED_NAMES:
        assert (offset - 0x876200) % 44 == 0
        expected = patch.encode(texts[offset]) + b'\xff'
        assert data[offset:offset + len(expected)] == expected
        assert data[offset + 14:offset + 44] == before[offset + 14:offset + 44]
        allowed.update(range(offset, offset + 14))
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(before, data)))
    assert patch.apply(data, texts) == 0


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
        patch.apply(data, texts)
    assert data == before
