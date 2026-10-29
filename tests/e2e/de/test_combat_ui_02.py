"""B-668 : vérifie les chaînes corrigées à tous leurs pointeurs EN."""
import json
import struct
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
# Le bundle BPS publié est volontairement inchangé : ces gardes portent sur
# le build DE des sources, pas les ROM matérialisées par make test-rom.
pytestmark = pytest.mark.rom
CASES = json.loads((ROOT / 'tests/fixtures/combat_ui_02.json').read_text())
# Tailles documentées des arguments des commandes FC de Gen III.
FC_ARGS = {
    1: 1, 2: 1, 3: 1, 4: 3, 5: 1, 6: 1, 8: 1, 11: 2, 12: 1,
    13: 1, 14: 1, 16: 2, 17: 1, 18: 1, 19: 1, 20: 1, 25: 1,
}


def logical_bytes(raw):
    """Ignore uniquement espaces et enveloppement ; conserve arguments et pages."""
    result = []
    i = 0
    while i < len(raw):
        value = raw[i]
        if value == 0xFC:
            size = 2 + FC_ARGS.get(raw[i + 1], 0)
        elif value in (0xF7, 0xF8, 0xF9, 0xFD):
            size = 2
        else:
            size = 1
        token = raw[i:i + size]
        if size > 1 or value not in (0x00, 0xFE, 0xFA):
            result.append(token)
        i += size
    return result


@pytest.fixture(scope='module')
def roms():
    return (
        (ROOT / 'input/roms/englishrom.gba').read_bytes(),
        (ROOT / 'output/roms/GenedRom-de.gba').read_bytes(),
    )


@pytest.mark.parametrize('case', CASES, ids=lambda case: case['offset'])
@pytest.mark.private_build
def test_every_live_pointer_keeps_text_and_controls(case, roms):
    source, translated = roms
    offset = int(case['offset'], 16)
    original = bytes.fromhex(case['source_hex'])
    expected = bytes.fromhex(case['expected_hex'])
    assert source[offset:offset + len(original)] == original
    pointer = struct.pack('<I', offset + 0x08000000)
    sites = []
    position = source.find(pointer)
    while position >= 0:
        sites.append(position)
        position = source.find(pointer, position + 1)
    assert sites == [int(site, 16) for site in case['sites']]
    assert sites
    for site in sites:
        target = struct.unpack_from('<I', translated, site)[0] - 0x08000000
        assert 0 <= target < len(translated), hex(site)
        end = translated.index(b'\xff', target)
        actual = translated[target:end + 1]
        assert logical_bytes(actual) == logical_bytes(expected), (
            f"{case['offset']} via {site:#x} -> {target:#x}: {actual.hex()}"
        )
