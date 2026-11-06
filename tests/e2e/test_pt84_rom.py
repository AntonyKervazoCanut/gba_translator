"""Contrôle binaire PT-84 sur la source réelle et la ROM construite."""
from pathlib import Path

import pytest

from languages.pt.patches.batch_84 import make_patch

ROOT = Path(__file__).resolve().parents[2]
pytestmark = pytest.mark.rom


def test_real_source_patch_is_atomic_idempotent_and_preserves_code():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    patch = make_patch(source)
    rom = bytearray(source)
    before_code = [bytes(rom[r['base']:r['base'] + len(bytes.fromhex(r['source_hex']))])
                   for r in patch.binary_regions]
    stats = patch.apply(rom)
    assert stats['verified'] == 290
    for region, expected in zip(patch.binary_regions, before_code):
        assert rom[region['base']:region['base'] + len(expected)] == expected
    allowed = bytearray(len(rom))
    for _, references, encoded in patch.entries():
        for ref in references:
            allowed[ref:ref + 4] = b'\x01' * 4
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed[target:target + len(encoded)] = b'\x01' * len(encoded)
    assert all(old == new or allowed[index]
               for index, (old, new) in enumerate(zip(source, rom)))
    once = bytes(rom)
    assert patch.apply(rom) == {'verified': 290, 'relocated': 0}
    assert bytes(rom) == once
    patch.verify(rom)


def test_built_pt_rom_contains_every_live_pt84_consumer():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    patch = make_patch(source)
    assert len(patch.entries()) == 290
    patch.verify(built)


def test_source_preimage_and_pointer_mismatches_are_rejected_without_writes():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    patch = make_patch(source)
    first = patch.definitions[0]
    corrupted = bytearray(source)
    corrupted[int(first['offset'], 16)] ^= 1
    invalid = make_patch(bytes(corrupted))
    rom = bytearray(source)
    with pytest.raises(ValueError, match='préimage différente'):
        invalid.apply(rom)
    assert rom == source
    corrupted = bytearray(source)
    corrupted[first['references'][0]] ^= 1
    invalid = make_patch(bytes(corrupted))
    with pytest.raises(ValueError, match='pointeur source différent'):
        invalid.apply(rom)
    assert rom == source
