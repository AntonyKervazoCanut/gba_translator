"""B-1026 : vérification de la ROM reconstruite et des 178 cellules préservées."""
import json
from pathlib import Path

import pytest

from languages.de.item_name_cells import OFFSETS, PREIMAGES
from languages.de.patches.item_names import encode
from scripts.apply_combined_fr import _load_combined

ROOT = Path(__file__).resolve().parents[3]
pytestmark = pytest.mark.rom


def test_all_live_names_metadata_and_remaining_cells():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-de.gba').read_bytes()
    before_names = (ROOT / 'output/roms/GenedRom-de.gba.item-names.bak').read_bytes()
    assert len(before_names) == len(built)
    combined, _ = _load_combined(ROOT / 'languages/de/combined_de.txt')
    scope = json.loads((ROOT / 'tests/unit/fixtures/item_names_objets_01_scope.json').read_text())
    assert len(scope) == 300
    assert len(OFFSETS) == 122
    assert built[0x9A8CA:0x9A8DC] == source[0x9A8CA:0x9A8DC]
    assert int.from_bytes(built[0x9A8D8:0x9A8DC], 'little') == 0x08876200
    for entry in scope:
        offset = int(entry['offset'], 16)
        if offset in OFFSETS:
            assert source[offset:offset + 14] == PREIMAGES[offset]
            expected = (encode(combined[offset]) + b'\xff').ljust(14, b'\x00')
        else:
            expected = bytes.fromhex(entry['name_hex_before'])
        assert built[offset:offset + 14] == expected, entry['offset']
        # Les autres lots peuvent déplacer légitimement les descriptions.
        # Comparer leur pointeur avant/après le patch de CE build, plutôt que
        # figer l'adresse allouée au moment de la qualification B-683.
        assert built[offset + 14:offset + 20] == source[offset + 14:offset + 20], entry['offset']
        assert built[offset + 24:offset + 44] == source[offset + 24:offset + 44], entry['offset']
        assert built[offset + 14:offset + 44] == before_names[offset + 14:offset + 44], entry['offset']
    # Référence brute de l'extraction, non prouvée : jamais repointée.
    assert built[0x9AF055:0x9AF059] == source[0x9AF055:0x9AF059]
