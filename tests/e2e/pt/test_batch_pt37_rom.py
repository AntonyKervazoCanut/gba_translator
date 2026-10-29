"""PT-37 : preuves sur la source réelle et sur la ROM PT construite."""
import hashlib
import json
import re
from pathlib import Path

import pytest

from languages.pt.patches.batch_37 import make_patch
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt37_audit.json').read_text())
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


def test_source_consumers_and_preimages(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    targets = {int(r['offset'], 16): [] for r in AUDIT['entries']}
    for match in re.finditer(b'[\x08\x09]', source):
        ref = match.start() - 3
        if ref >= 0:
            target = int.from_bytes(source[ref:ref + 4], 'little') - 0x08000000
            if target in targets:
                targets[target].append(ref)
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        assert targets[offset] == row['references']
    for literal in AUDIT['ability_table']['literals']:
        ref = int(literal, 16)
        assert int.from_bytes(source[ref:ref + 4], 'little') == 0x08A36398
    # Trois consommateurs actifs de descriptions, pas l'ancienne table PT-34.
    for ref in (0xE5440, 0x137BC8, 0x9F3B64):
        assert int.from_bytes(source[ref:ref + 4], 'little') == 0x0899F194


def test_final_rom_delivers_every_entry(source):
    rom = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    make_patch(source).verify(rom)
    for literal in AUDIT['ability_table']['literals']:
        ref = int(literal, 16)
        assert rom[ref:ref + 4] == source[ref:ref + 4]
    for row in AUDIT['entries']:
        if row['kind'] == 'ability_name':
            offset = int(row['offset'], 16)
            assert rom[offset:offset + 17] == source[offset:offset + 17]
            expected = TextEncoder.encode_pokemon(row['expected'], strict=True)
            assert rom[offset:offset + len(expected)] == expected
            for ref in row['references']:
                target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
                assert 0 <= target <= len(rom) - len(expected)
                assert rom[target:target + len(expected)] == expected
    # Vérification séparée des descriptions au consommateur indexé et aux CT.
    for row in AUDIT['entries']:
        if row['kind'] == 'move_description':
            assert any(0x99F190 <= p <= 0x99FE5C for p in row['references'])
