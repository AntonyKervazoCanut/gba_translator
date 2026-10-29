"""PT-01 : vérifier chaque référence dans la ROM construite, pas seulement le combined."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from src.core.text_codec import TextEncoder

pytestmark = pytest.mark.rom
ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt01_audit.json').read_text())
ENTRIES = [entry for entry in AUDIT['entries'] if entry['status'] == 'translated']


def canonical(raw: bytes) -> bytes:
    """Autorise le rewrap du moteur, conserve mots, variables, couleurs et pages."""
    return re.sub(b'\x00+', b'\x00', raw.replace(b'\xfe', b'\x00').replace(b'\xfa', b'\x00'))


@pytest.fixture(scope='module')
def built_rom() -> bytes:
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


@pytest.fixture(scope='module')
def translations() -> dict[int, str]:
    result = {}
    for line in (ROOT / 'languages/pt/combined_pt.txt').read_text().splitlines():
        match = re.match(r'0x([\da-fA-F]+):\s?(.*)', line)
        if match:
            result[int(match[1], 16)] = match[2].replace('\\n', '\n')
    return result


@pytest.mark.parametrize('entry', ENTRIES, ids=lambda e: e['offset'])
def test_all_original_references_reach_portuguese(
    entry: dict, built_rom: bytes, translations: dict[int, str],
) -> None:
    expected = TextEncoder.encode_pokemon(translations[int(entry['offset'], 16)], strict=True)
    assert entry['pointers'], entry['offset']
    for address in entry['pointers']:
        at = int(address, 16)
        target = int.from_bytes(built_rom[at:at + 4], 'little') - 0x08000000
        assert 0 <= target < len(built_rom), (entry['offset'], address, hex(target))
        end = built_rom.index(0xFF, target)
        actual = built_rom[target:end + 1]
        assert canonical(actual) == canonical(expected), (
            entry['offset'], address, hex(target), actual.hex(), expected.hex(),
        )


def test_accidental_graphics_and_instruction_words_are_untouched(built_rom: bytes) -> None:
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    for entry in AUDIT['entries']:
        for rejected in entry.get('rejected_occurrences', []):
            at = int(rejected['address'], 16)
            assert built_rom[at:at + 4] == source[at:at + 4], (entry['offset'], hex(at))


def test_audit_source_and_references() -> None:
    from hashlib import sha256
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    assert sha256(source).hexdigest() == AUDIT['source_sha256']
    for entry in AUDIT['entries']:
        offset = int(entry['offset'], 16)
        raw = bytes.fromhex(entry['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        for address in entry['pointers']:
            at = int(address, 16)
            assert int.from_bytes(source[at:at + 4], 'little') == offset + 0x08000000
