"""ES-005 : consommateurs Easy Chat, octets vivants et isolation des cellules."""
import hashlib
import json
import re
import struct
from pathlib import Path

import pytest

from src.core.font_glyphs import LATIN_FONTS

ROOT = Path(__file__).resolve().parents[3]
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def delivery():
    report = json.loads((ROOT / 'docs/analysis/es/005_TRAITEMENT.json').read_text())
    return report, (ROOT / 'input/roms/englishrom.gba').read_bytes(), (ROOT / 'output/roms/GenedRom-es-maint.gba').read_bytes()


def test_every_word_reaches_its_live_pointer_and_original_group(delivery):
    report, source, built = delivery
    groups = [struct.unpack_from('<IHH', source, 0x3eced4 + i * 8) for i in range(22)]
    for row in report['entries']:
        offset, site = int(row['offset'], 16), int(row['pointer_site'], 16)
        sites = [m.start() for m in re.finditer(re.escape(struct.pack('<I', offset + 0x8000000)), source)]
        assert sites == [site]
        base, count, _ = groups[row['group']]
        assert site == base - 0x8000000 + 12 * row['word_index']
        assert row['word_index'] < count
        assert source[offset:source.index(b'\xff', offset) + 1].hex() == row['english_raw']
        target = struct.unpack_from('<I', built, site)[0] - 0x8000000
        expected = bytes.fromhex(row['encoded_hex'])
        assert 0 <= target < len(built) - len(expected)
        assert built[target:target + len(expected)] == expected, (row['offset'], hex(target))
        assert built[site + 4:site + 12] == source[site + 4:site + 12]


def test_descriptors_engine_and_unselected_cells_are_preserved(delivery):
    report, source, built = delivery
    selected = {int(row['pointer_site'], 16) for row in report['entries']}
    assert built[0x3eced4:0x3eced4 + 22 * 8] == source[0x3eced4:0x3eced4 + 22 * 8]
    for site in (0xbd788, 0xbd7c0, 0xbd84c, 0xbda38, 0xbdd2c, 0xbe270, 0xbe414):
        assert source[site:site + 4] == struct.pack('<I', 0x83eced4)
        assert built[site:site + 4] == source[site:site + 4]
    for group in range(2, 10):
        base, count, _ = struct.unpack_from('<IHH', source, 0x3eced4 + group * 8)
        for site in range(base - 0x8000000, base - 0x8000000 + count * 12, 12):
            if site not in selected:
                assert built[site:site + 12] == source[site:site + 12], hex(site)
                target = struct.unpack_from('<I', source, site)[0] - 0x8000000
                original = source[target:source.index(b'\xff', target) + 1]
                assert built[target:target + len(original)] == original, hex(site)


def test_all_five_font_budgets_and_source_hashes(delivery):
    report, _, built = delivery
    for row in report['entries']:
        encoded = bytes.fromhex(row['encoded_hex'])
        for font, limit in zip(LATIN_FONTS, row['width_limits']):
            _, widths = font.offsets(built)
            assert sum(built[widths + code] for code in encoded[:-1]) <= limit, row['offset']
    for path, expected in report['sources'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path


def test_spanish_correspondences_follow_the_offset_map(delivery):
    report, _, _ = delivery
    reference = (ROOT / 'input/roms/spanishrom.gba').read_bytes()
    mapping = json.loads((ROOT / 'output/differences/pointer_offset_map.json').read_text())
    by_english = {}
    for match in mapping['offset_map']:
        by_english.setdefault(match['english_offset'], set()).add(match['spanish_offset'])
    for row in report['entries']:
        offset = int(row['offset'], 16)
        spanish_offset = int(row['spanish_offset'], 16)
        assert by_english[offset] == {spanish_offset}
        expected = bytes.fromhex(row['spanish_raw'])
        assert reference[spanish_offset:spanish_offset + len(expected)] == expected
        sites = [m.start() for m in re.finditer(re.escape(struct.pack('<I', spanish_offset + 0x8000000)), reference)]
        assert sites == [int(site, 16) for site in row['spanish_pointer_sites']]
