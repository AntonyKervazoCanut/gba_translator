"""PT-05 : vérifier les préimages, tous les pointeurs et les textes livrés."""
from __future__ import annotations

import hashlib
import json
import re
import struct
from pathlib import Path

import pytest

from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder

pytestmark = pytest.mark.rom
ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt05_audit.json').read_text())


@pytest.fixture(scope='module')
def roms() -> tuple[bytes, bytes]:
    return ((ROOT / 'input/roms/englishrom.gba').read_bytes(),
            (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes())


@pytest.fixture(scope='module')
def translations() -> dict[int, bytes]:
    entries = {}
    for line in (ROOT / 'languages/pt/combined_pt.txt').read_text().splitlines():
        match = re.match(r'0x([\da-fA-F]+):\s?(.*)', line)
        if match:
            entries[int(match[1], 16)] = TextEncoder.encode_pokemon(
                match[2].replace('\\n', '\n'), strict=True)
    return entries


def test_canonical_source_and_active_table(roms: tuple[bytes, bytes]) -> None:
    source, built = roms
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for rom in (source, built):
        assert struct.unpack_from('<I', rom, 0x9A8D8)[0] == 0x08876200
        assert struct.unpack_from('<I', rom, 0x9A98C)[0] == 0x08876200
        assert rom[0x9A96C:0x9A990].hex() == AUDIT['item_table']['description_accessor_hex']


@pytest.mark.parametrize('row', AUDIT['entries'], ids=lambda e: e['offset'])
def test_every_offset_and_live_consumer(
    row: dict, roms: tuple[bytes, bytes], translations: dict[int, bytes],
) -> None:
    source, built = roms
    offset = int(row['offset'], 16)
    raw = bytes.fromhex(row['source_hex'])
    assert source[offset:offset + len(raw)] == raw
    # Recherche non alignée : les scripts peuvent contenir des pointeurs impairs.
    refs = []
    at = 0
    pattern = struct.pack('<I', offset + 0x08000000)
    while (at := source.find(pattern, at)) >= 0:
        refs.append(at)
        at += 1
    assert set(refs) == {int(p, 16) for p in row['pointers'] + row['legacy_pointers']}
    if row['status'] == 'translated':
        expected = translations[offset]
        for pointer in row['pointers']:
            address = int(pointer, 16)
            assert (address - 0x876214) % 44 == 0
            target = struct.unpack_from('<I', built, address)[0] - 0x08000000
            assert 0 <= target < len(built)
            assert built[target:target + len(expected)] == expected
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            for line in expected[:-1].split(b'\xfe'):
                assert sum(built[widths + c] for c in line) <= 192
    else:
        assert built[offset:offset + len(raw)] == raw
        for counterpart in row.get('active_counterparts', []):
            address = int(counterpart['pointer'], 16)
            target = struct.unpack_from('<I', source, address)[0] - 0x08000000
            assert target == int(counterpart['target'], 16) and target != offset
