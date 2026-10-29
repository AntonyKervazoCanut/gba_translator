"""Vérifie chaque pointeur PT-03 et chaque cellule fixe dans la ROM finale."""
from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

import pytest

from languages.pt.patches.trainer_class_names import apply
from scripts.apply_combined_fr import _load_combined
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_built_batch_01_pt import canonical

pytestmark = pytest.mark.rom
ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt03_audit.json').read_text())


@pytest.fixture(scope='module')
def roms() -> tuple[bytes, bytes, dict]:
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    translations, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    assert sha256(source).hexdigest() == AUDIT['source_sha256']
    return source, built, translations


@pytest.mark.parametrize('entry', AUDIT['entries'], ids=lambda e: e['offset'])
def test_actual_injection_or_preservation(entry: dict, roms: tuple) -> None:
    source, built, translations = roms
    offset = int(entry['offset'], 16)
    raw = bytes.fromhex(entry['source_hex'])
    assert source[offset:offset + len(raw)] == raw
    if entry['status'] == 'exception':
        if 'live_indirection' in entry:
            live = entry['live_indirection']
            at = int(live['pointer'], 16)
            original_target = int(live['source_target'], 16)
            target = int.from_bytes(built[at:at + 4], 'little') - 0x8000000
            assert 0 <= target < len(built)
            expected = (TextEncoder.encode_pokemon(translations[original_target], strict=True)
                        if original_target in translations else bytes.fromhex(live['source_hex']))
            assert canonical(built[target:built.index(0xFF, target) + 1]) == canonical(expected)
            return
        # Les glyphes sont modifiés uniquement par le patch F-758, pas par PT-03.
        if not 0x1EAF00 <= offset < 0x230000:
            assert built[offset:offset + len(raw)] == raw
        return
    expected = TextEncoder.encode_pokemon(translations[offset], strict=True) if offset in translations else raw
    if 'cell_start' in entry:
        assert offset == int(entry['cell_start'], 16)
        assert built[offset:offset + len(expected)] == expected
        for pointer in entry['table_pointers']:
            at = int(pointer, 16)
            assert int.from_bytes(built[at:at + 4], 'little') == 0x823E558
    for pointer in entry['pointers']:
        at = int(pointer, 16)
        assert int.from_bytes(source[at:at + 4], 'little') == 0x8000000 + offset
        target = int.from_bytes(built[at:at + 4], 'little') - 0x8000000
        assert 0 <= target < len(built)
        end = built.index(0xFF, target)
        assert canonical(built[target:end + 1]) == canonical(expected), (entry['offset'], pointer, hex(target))


def test_fixed_cells_are_bounded_atomic_and_idempotent(roms: tuple) -> None:
    source, _, _ = roms
    candidate = bytearray(source)
    assert apply(candidate, source) > 0
    allowed = set()
    for entry in AUDIT['entries']:
        if entry['status'] == 'translated' and 'cell_start' in entry:
            at = int(entry['offset'], 16)
            allowed.update(range(at, at + 13))
    assert {i for i, (a, b) in enumerate(zip(source, candidate)) if a != b} <= allowed
    assert apply(candidate, source) == 0
    candidate[0x23E787] ^= 1
    before = bytes(candidate)
    with pytest.raises(ValueError, match='inattendue'):
        apply(candidate, source)
    assert candidate == before
