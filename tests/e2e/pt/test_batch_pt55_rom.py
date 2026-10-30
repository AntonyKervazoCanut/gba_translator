"""PT-55 : cellules réellement livrées et patch strictement borné."""
from pathlib import Path

import pytest

from languages.pt.patches.batch_55 import apply_patches
from tests.unit.pt.test_batch_pt55 import AUDIT

ROOT = Path(__file__).resolve().parents[3]
pytestmark = pytest.mark.rom


def test_built_cells_and_all_table_readers():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    rom = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    for ref in AUDIT['table_references']:
        assert rom[ref:ref + 4] == source[ref:ref + 4]
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        assert rom[off:off + 11] == source[off:off + 11] == bytes.fromhex(row['source_hex'])


def test_repair_is_atomic_idempotent_and_preserves_every_other_byte():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    rom = bytearray(source)
    expected = bytearray(source)
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        rom[off:off + 11] = b'\xff' * 11
    assert apply_patches(rom, source) == 299
    assert rom == expected
    assert apply_patches(rom, source) == 299
    assert rom == expected
    ref = AUDIT['table_references'][0]
    rom[ref] ^= 1
    before = bytes(rom)
    with pytest.raises(ValueError, match='Lecteur'):
        apply_patches(rom, source)
    assert rom == before
