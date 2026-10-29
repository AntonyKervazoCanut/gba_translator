"""Vérifie les 282 décisions PT-08 dans la ROM reconstruite, table comprise."""
from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

import pytest

from scripts.apply_combined_fr import _load_combined
from src.core.text_codec import TextEncoder

pytestmark = pytest.mark.rom
ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt08_audit.json').read_text())


@pytest.fixture(scope='module')
def roms() -> tuple:
    return ((ROOT / 'input/roms/englishrom.gba').read_bytes(),
            (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes(),
            _load_combined(ROOT / 'languages/pt/combined_pt.txt')[0])


@pytest.mark.parametrize('entry', AUDIT['entries'], ids=lambda e: e['offset'])
def test_live_word_and_table_metadata(entry: dict, roms: tuple) -> None:
    source, built, pt = roms
    offset = int(entry['offset'], 16)
    original = bytes.fromhex(entry['source_hex'])
    assert source[offset:offset + len(original)] == original
    if entry['status'] == 'exception':
        assert built[offset:offset + len(original)] == original
        for pointer in entry['pointers'] + ([entry['interior_pointer']] if 'interior_pointer' in entry else []):
            at = int(pointer, 16)
            assert built[at:at + 12] == source[at:at + 12]
        return
    expected = TextEncoder.encode_pokemon(pt[offset], strict=True)
    for pointer in entry['pointers']:
        at = int(pointer, 16)
        assert int.from_bytes(source[at:at + 4], 'little') == offset + 0x08000000
        target = int.from_bytes(built[at:at + 4], 'little') - 0x08000000
        assert 0 <= target < len(built) - len(expected)
        assert built[target:target + len(expected)] == expected, (entry['offset'], pointer, hex(target))
        # Chaque entrée Easy Chat : pointeur + ordre alphabétique + disponibilité.
        assert built[at + 4:at + 12] == source[at + 4:at + 12]
    for literal in (0x6594, 0x66F4):
        widths = int.from_bytes(built[literal:literal + 4], 'little') - 0x08000000
        assert 0 <= widths < len(built) - 256
        assert sum(built[widths + c] for c in expected[:-1]) <= entry['pixel_budget']


def test_english_source_identity(roms: tuple) -> None:
    assert sha256(roms[0]).hexdigest() == AUDIT['source_sha256']
