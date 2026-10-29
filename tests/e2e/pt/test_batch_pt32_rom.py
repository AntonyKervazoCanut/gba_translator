"""PT-32 : vrais pointeurs, cellules fixes, graphismes et budgets ROM."""
import hashlib
import json
import re
from pathlib import Path

import pytest

from languages.pt.patches.batch_32 import make_patch
from languages.pt.patches.font import apply_patches
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt32_audit.json').read_text())
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_source_preimages_references_and_real_item_table(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        refs = [m.start() for m in re.finditer(
            re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert refs == row.get('raw_references', row['references'])
        if 'table_base' in row:
            site = int(row['table_pointer'], 16)
            base = int.from_bytes(source[site:site + 4], 'little') - 0x08000000
            assert base == int(row['table_base'], 16)
            assert base + row['stride'] * row['item_id'] == offset
        for related in row.get('related_consumers', []):
            target = int(related['offset'], 16)
            raw = bytes.fromhex(related['source_hex'])
            assert related['references']
            assert source[target:target + len(raw)] == raw
            for site in related['references']:
                assert int.from_bytes(source[site:site + 4], 'little') == target + 0x08000000
        if 'consumer_offset' in row:
            for site in row['consumer_references']:
                assert int.from_bytes(source[site:site + 4], 'little') == int(row['consumer_offset'], 16) + 0x08000000


def test_final_rom_all_consumers_fixed_cells_and_exceptions(source, built):
    patch = make_patch(source)
    assert len(patch.entries()) == 156
    patch.verify(built)
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        if row['status'] == 'exception' or 'table_base' in row:
            size = row.get('stride', len(bytes.fromhex(row['source_hex'])))
            # Les noms gardés sont des cellules vivantes, sans repointage possible.
            # Seul leur champ nom (14 octets) est sous la responsabilité de PT-32.
            if 'table_base' in row:
                size = row['cell_bytes']
                site = int(row['table_pointer'], 16)
                live = int.from_bytes(built[site:site + 4], 'little') - 0x08000000
                assert live == int(row['table_base'], 16)
                assert live + row['stride'] * row['item_id'] == offset
            assert built[offset:offset + size] == source[offset:offset + size]
        for site in row.get('non_text_references', []):
            assert built[site - 12:site + 16] == source[site - 12:site + 16]
    assert built[0x8B105B] == source[0x8B105B] == 0
    assert built[0x888480:0x888490] == source[0x888480:0x888490]


def test_patch_atomic_idempotent_and_bounded(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 156
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 156, 'relocated': 0}
    assert bytes(rom) == after
    allowed = set()
    for _, refs, raw in patch.entries():
        for site in refs:
            allowed.update(range(site, site + 4))
            target = int.from_bytes(rom[site:site + 4], 'little') - 0x08000000
            allowed.update(range(target, target + len(raw)))
    assert {i for i, (a, b) in enumerate(zip(source, rom)) if a != b} <= allowed
    for row in patch.definitions:
        for site in row.get('non_text_references', []):
            rom[site:site + 4] = b'BAD!'
    assert patch.apply(rom) == {'verified': 156, 'relocated': 0}
    assert bytes(rom) == after
    patch.definitions[0] = dict(patch.definitions[0], source_hex='00ff')
    with pytest.raises(ValueError, match='préimage'):
        patch.apply(rom)
    assert bytes(rom) == after


def test_real_fonts_expanded_buffers_and_menu_budget(source):
    rom = bytearray(source)
    apply_patches(rom)
    buffers = {(0xFD, i): 'W' * 10 for i in range(0x30)}
    for i in (0x0F, 0x10, 0x13):
        buffers[(0xFD, i)] = 'The opposing ' + 'W' * 10
    for i in (0x16, 0x17, 0x18):
        buffers[(0xFD, i)] = 'Primordial Sea'
    for offset, _, raw in make_patch(source).entries():
        buffers[(0xFD, 0x16)] = (
            'Weakness Policy' if offset in (0x8B4EC0, 0x8B5030) else 'Primordial Sea')
        for font in LATIN_FONTS:
            _, table = font.offsets(rom)
            for segment in re.split(b'[\xfa\xfb]', raw):
                assert max(widths(segment, rom, table, buffers)) <= 224, hex(offset)
    for row in AUDIT['entries']:
        if 'table_base' in row:
            raw = TextEncoder.encode_pokemon(row['portuguese'], strict=True)
            for font in LATIN_FONTS:
                assert max(widths(raw, rom, font.offsets(rom)[1])) <= 78
