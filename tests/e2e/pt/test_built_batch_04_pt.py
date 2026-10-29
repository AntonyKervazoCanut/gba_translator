"""PT-04 : contrôle des pointeurs vivants et des vraies cellules après build."""
from __future__ import annotations

import json
import re
from hashlib import sha256
from pathlib import Path

import pytest

from src.core.text_codec import TextEncoder

pytestmark = pytest.mark.rom
ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt04_audit.json').read_text())


@pytest.fixture(scope='module')
def roms() -> tuple[bytes, bytes, dict[int, str]]:
    pt = {}
    for line in (ROOT / 'languages/pt/combined_pt.txt').read_text().splitlines():
        match = re.match(r'0x([\da-fA-F]+):\s?(.*)', line)
        if match:
            pt[int(match[1], 16)] = match[2].replace('\\n', '\n')
    return ((ROOT / 'input/roms/englishrom.gba').read_bytes(),
            (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes(), pt)


def canonical(raw: bytes) -> bytes:
    """Autorise le rewrap mais conserve pages, contrôles et mots."""
    return re.sub(b'\x00+', b'\x00', raw.replace(b'\xfe', b'\0').replace(b'\xfa', b'\0'))


@pytest.mark.parametrize('entry', AUDIT['entries'], ids=lambda e: e['offset'])
def test_every_offset_in_final_rom(entry: dict, roms: tuple) -> None:
    source, built, pt = roms
    offset = int(entry['offset'], 16)
    original = bytes.fromhex(entry['source_hex'])
    assert source[offset:offset + len(original)] == original
    if entry['status'] == 'translated':
        text = pt[offset]
        expected = TextEncoder.encode_pokemon(text, strict=True)
        if entry['delivery'] == 'fixed_cell':
            cell = int(entry['cell_offset'], 16)
            expected = TextEncoder.encode_pokemon(text.lstrip(), strict=True)
            expected = expected[entry.get('prefix_bytes', 0):]
            assert built[cell:cell + entry['cell_bytes']] == expected.ljust(entry['cell_bytes'], b'\0')
        # Largeurs des vraies polices de dialogue/résumé, après patch PT.
        for literal in (0x6594, 0x66F4):
            widths = int.from_bytes(built[literal:literal + 4], 'little') - 0x08000000
            assert 0 <= widths < len(built) - 256
            cursor = index = 0
            while index < len(expected):
                code = expected[index]
                if code in (0xFE, 0xFA, 0xFB, 0xFF):
                    assert cursor <= 192, (entry['offset'], hex(literal), cursor)
                    cursor = 0
                    index += 1
                elif code == 0xFD:
                    cursor += 15 * 6  # Nom de combattant avec préfixe, marge comprise.
                    index += 2
                elif code == 0xFC:
                    assert expected[index + 1] == 3
                    index += 3
                else:
                    cursor += built[widths + code]
                    index += 1
        for pointer in entry['pointers']:
            at = int(pointer, 16)
            target = int.from_bytes(built[at:at + 4], 'little') - 0x08000000
            assert 0 <= target < len(built), (entry['offset'], pointer)
            actual = built[target:built.index(255, target) + 1]
            assert canonical(actual) == canonical(expected), (entry['offset'], pointer, hex(target))
    elif entry['status'] == 'retained_english' or 'cell_offset' in entry:
        cell = int(entry['cell_offset'], 16)
        assert built[cell:cell + entry['cell_bytes']] == bytes.fromhex(entry['source_cell_hex'])
    elif entry['status'] == 'exception':
        assert built[offset:offset + len(original)] == original
        for pointer in entry['all_pointer_occurrences']:
            at = int(pointer, 16)
            assert built[at:at + 4] == source[at:at + 4]
    else:
        assert entry['status'] == 'alias' and entry['canonical_offset']
        if 'prefix_hex' in entry:
            prefix = bytes.fromhex(entry['prefix_hex'])
            assert built[offset:offset + len(prefix)] == prefix


def test_source_hash_and_live_ability_table(roms: tuple) -> None:
    source, _, _ = roms
    assert sha256(source).hexdigest() == AUDIT['source_sha256']
    for entry in AUDIT['entries']:
        if entry['status'] == 'translated' and 0x24F3C4 <= int(entry['offset'], 16) <= 0x24FABE:
            assert any(0x96DE04 <= int(p, 16) < 0x96DE04 + 293 * 4
                       for p in entry['pointers'])
    for at, value in [(0xD80A0, 0x23E558), (0x11B4B4, 0x23E558), (0x8A123C, 0x24FC40)]:
        assert int.from_bytes(source[at:at + 4], 'little') == value + 0x08000000
