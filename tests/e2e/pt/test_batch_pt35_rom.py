"""PT-35 : octets livrés, cellules indexées et absence d'écritures étrangères."""
import hashlib
import json
import re
from pathlib import Path

import pytest

from languages.pt.patches.batch_35 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from tests.e2e.pt.test_batch_pt13_rom import widths

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt35_audit.json').read_text())
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_source_all_references_and_replacement_evidence(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        assert row['references'] == [m.start() for m in re.finditer(
            re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        for consumer in row.get('related_consumers', []):
            for site in consumer['sites']:
                assert int.from_bytes(source[site:site + 4], 'little') == int(consumer['offset'], 16) + 0x08000000
        if 'graphic_owner_offset' in row:
            site = int(row['graphic_owner_pointer'], 16)
            assert int.from_bytes(source[site:site + 4], 'little') == int(row['graphic_owner_offset'], 16) + 0x08000000
        if 'replacement_name_index' in row:
            assert int(row['replacement_name_offset'], 16) == 0xA36398 + 17 * row['replacement_name_index']


def test_patch_atomic_idempotent_bounded_and_no_truncation(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom) == {'verified': 154, 'relocated': 154, 'fixed_cells': 9}
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 154, 'relocated': 0, 'fixed_cells': 9}
    assert bytes(rom) == after
    allowed = set()
    for _, refs, raw in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(target, target + len(raw)))
    for row, cell, _ in patch.cell_entries():
        allowed.update(range(int(row['offset'], 16), cell + 7))
        for ref in row['references']:
            allowed.update(range(ref, ref + 4))
    assert {i for i, (a, b) in enumerate(zip(source, rom)) if a != b} <= allowed
    patch.texts[0x961B73] = 'Nome que excede a célula'
    with pytest.raises(ValueError, match='dépassée'):
        patch.apply(rom)
    assert bytes(rom) == after
    patch = make_patch(source)
    patch.definitions[0] = dict(patch.definitions[0], source_hex='00ff')
    with pytest.raises(ValueError, match='préimage'):
        patch.apply(rom)
    assert bytes(rom) == after


def test_final_rom_and_all_exceptions_untouched(source, built):
    make_patch(source).verify(built)
    for row in AUDIT['entries']:
        if row['status'] != 'exception':
            continue
        start = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        if 'cell_offset' in row:
            # La clé peut commencer dans le bourrage du type précédent,
            # dont le terminateur FF est réécrit par sa propre traduction.
            start = int(row['cell_offset'], 16)
            raw = source[start:start + row['cell_bytes']]
        assert built[start:start + len(raw)] == raw, row['offset']


def test_real_fonts_with_runtime_battle_buffers(source, built):
    patch = make_patch(source)
    # Noms de Pokémon de dix caractères ; noms d'objets/capacités réellement longs.
    buffers = {(0xFD, i): 'W' * 10 for i in (0, 1, 15, 16, 17, 19, 24, 52, 57)}
    buffers.update({(0xFD, 20): 'Light That Burns the Sky',
                    (0xFD, 22): 'Utility Umbrella', (0xFD, 25): 'Supercrescimento',
                    (0xFD, 26): 'Primordial Sea', (0xFD, 53): 'adversária',
                    (0xFD, 54): 'adversária'})
    for offset, _, raw in patch.entries():
        row = next(r for r in AUDIT['entries'] if int(r['offset'], 16) == offset)
        for font in LATIN_FONTS:
            _, table = font.offsets(built)
            for segment in re.split(b'[\xfa\xfb]', raw):
                assert max(widths(segment, built, table, buffers)) <= row['max_width'], (hex(offset), font.glyph_pointer, widths(segment, built, table, buffers))
    for _, _, raw in patch.cell_entries():
        for font in LATIN_FONTS:
            _, table = font.offsets(built)
            assert max(widths(raw, built, table)) <= 42
