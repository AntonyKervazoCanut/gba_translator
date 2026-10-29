"""PT-33 : livraison binaire, faux pointeurs intacts et budgets des cinq polices."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pytest

from languages.pt.patches.batch_33 import make_patch
from languages.pt.patches.font import apply_patches
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt33_audit.json').read_text())
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source() -> bytes:
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built() -> bytes:
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_source_preimages_references_and_exception_consumers(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        refs = [m.start() for m in re.finditer(
            re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert refs == row.get('raw_references', row['references'])
        assert sorted(row['references'] + row.get('legacy_table_references', []) + row.get('non_text_references', [])) == refs
        for target_key, refs_key in [('owner_offset', 'owner_sites'),
                                     ('related_offset', 'related_sites'),
                                     ('consumer_offset', 'consumer_references')]:
            if target_key in row:
                assert row[refs_key]
                for ref in row[refs_key]:
                    assert int.from_bytes(source[ref:ref + 4], 'little') == int(row[target_key], 16) + 0x08000000
    # Un vrai littéral Thumb 0x08250892 est aligné à 0x2d694 ; le motif
    # chevauchant deux octets de bourrage n'est pas un pointeur vers du texte.
    assert source[0x2D692:0x2D694] == b'\x00\x00'
    assert int.from_bytes(source[0x2D694:0x2D698], 'little') == 0x08250892

    for base in (0x904000, 0x904004):
        assert (base + 0x08000000).to_bytes(4, 'little') not in source
    for site in (0xE5440, 0x137BC8, 0x9F3B64):
        assert int.from_bytes(source[site:site + 4], 'little') == 0x0899F194


def test_patch_is_atomic_bounded_and_idempotent(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 263
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 263, 'relocated': 0}
    assert bytes(rom) == after
    allowed = set()
    for _, refs, raw in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(target, target + len(raw)))
    assert {i for i, (a, b) in enumerate(zip(source, rom)) if a != b} <= allowed
    patch.definitions[0] = dict(patch.definitions[0], source_hex='00ff')
    with pytest.raises(ValueError, match='préimage'):
        patch.apply(rom)
    assert bytes(rom) == after


def test_final_rom_delivers_all_263_strings_and_preserves_graphics(source, built):
    patch = make_patch(source)
    patch.verify(built)
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            continue
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        for ref in row.get('consumer_references', row['references']):
            target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
            assert built[target:target + len(raw)] == raw
    assert built[0x2D690:0x2D698] == source[0x2D690:0x2D698]
    assert built[0x440D80:0x440E40] == source[0x440D80:0x440E40]
    assert built[0x920284] == 0
    # Les dix descriptions de l'ancienne table ne sont pas revendiquées.
    for row in AUDIT['entries']:
        if 'legacy_table_references' in row:
            for ref in row['legacy_table_references']:
                assert built[ref:ref + 4] == source[ref:ref + 4]
    assert len(built) == len(source)


def test_real_fonts_with_maximum_dynamic_buffers(source):
    rom = bytearray(source)
    apply_patches(rom)
    patch = make_patch(source)
    for ix, row in enumerate(AUDIT['entries']):
        if row['status'] == 'exception':
            continue
        buffers = {(0xFD, k): 'W' * 10 for k in range(64)}
        if ix < 16 or 146 <= ix < 271:
            buffers.update({(0xFD, k): 'The opposing ' + 'W' * 10 for k in (15, 16, 19)})
            buffers.update({(0xFD, k): 'W' * 17 for k in (24, 25, 26, 27)})
            buffers[(0xFD, 22)] = 'W' * 13  # Nom gItems : 14 octets, terminateur inclus.
        if ix in (13, 14):
            buffers[(0xFD, 3)] = 'Defesa Especial'
        if ix == 80:
            buffers[(0xFD, 2)] = 'rapaz'
        if ix == 95:
            buffers[(0xFD, 2)] = 'ela'
        if ix == 96:
            buffers[(0xFD, 3)], buffers[(0xFD, 2)] = 'Ela', 'ela'
        if ix in (120, 121):
            buffers[(0xFD, 2)] = '999'
        if ix in (121, 123):
            buffers[(0xFD, 3 if ix == 121 else 2)] = 'W' * 17
        raw = TextEncoder.encode_pokemon(patch.texts[int(row['offset'], 16)].replace(r'\n', '\n'), strict=True)
        limit = 122 if ix >= 271 else 224 if ix < 16 or ix >= 146 else 208
        for font in LATIN_FONTS:
            _, table = font.offsets(rom)
            for segment in re.split(b'[\xfa\xfb]', raw):
                assert max(widths(segment, rom, table, buffers)) <= limit, (row['offset'], font.glyph_pointer)
