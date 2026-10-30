"""PT-45 : octets livrés, préimages et budgets des polices réelles."""
import hashlib
import json
import re
from pathlib import Path

import pytest

from languages.pt.patches.batch_45 import make_patch
from languages.pt.patches.font import apply_patches
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt45_audit.json').read_text())
pytestmark = pytest.mark.rom

@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()

@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_live_preimages_and_false_prefix(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[off:off + len(raw)] == raw
        assert [m.start() for m in re.finditer(re.escape(
            (off + 0x08000000).to_bytes(4, 'little')), source)] == row['references']
    false = AUDIT['entries'][241]
    assert false['offset'] == '0xa4a8dd' and not false['references']
    assert source[0xA4A8DD:0xA4A8E0] == bytes.fromhex('00c046')
    assert int.from_bytes(source[0x9EB8F4:0x9EB8F8], 'little') == 0x08A4A8E0
    # Table indexée de répliques ; plusieurs lecteurs du moteur partagent la base.
    for base, refs in [(0xA6F130, (0x9C584C, 0x9E65B8)),
                       (0xA6F36C, (0x9C5878, 0x9E65B4)),
                       (0xA6F574, (0x9C5888, 0x9E65B0, 0x9E670C, 0x9E68F4))]:
        for ref in refs:
            assert int.from_bytes(source[ref:ref + 4], 'little') == base + 0x08000000
    for ref in (0x9655D4, 0x965AB6, 0x96CEFB, 0x96BD4A, 0x96BD8D):
        assert source[ref - 4:ref] == bytes.fromhex('20e00302')


def test_final_rom_delivers_all_282_entries(source, built):
    patch = make_patch(source)
    assert len(patch.entries()) == 282
    patch.verify(built)
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            continue
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        for ref in row['references']:
            target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
            assert built[target:target + len(raw)] == raw
    assert built[0xA4A8DD:0xA4A8E0] == source[0xA4A8DD:0xA4A8E0]
    assert len(source) == len(built)


def test_real_font_widths_with_expanded_battle_buffers(source):
    rom = bytearray(source)
    apply_patches(rom)
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            continue
        off = int(row['offset'], 16)
        buffers = {(0xFD, k): 'W' * 10 for k in range(64)}
        # Les noms précédés de leur camp peuvent occuper 23 caractères.
        buffers.update({(0xFD, k): 'The opposing ' + 'W' * 10 for k in (15, 16, 19)})
        buffers[(0xFD, 0)] = 'Elétrico'
        buffers[(0xFD, 22)] = 'W' * 13
        buffers[(0xFD, 25)] = 'W' * 17
        buffers[(0xFD, 24)] = 'W' * 17
        buffers[(0xFD, 26)] = 'W' * 17
        buffers[(0xFD, 61)] = 'The opposing'
        buffers[(0xFD, 59)] = 'W' * 10
        buffers[(0xFD, 60)] = 'W' * 10
        buffers[(0xFD, 54)] = 'adversária'
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        for font in LATIN_FONTS:
            _, table = font.offsets(rom)
            for page in re.split(b'[\xfa\xfb]', raw):
                assert max(widths(page, rom, table, buffers)) <= row['max_width'], (hex(off), font.glyph_pointer, widths(page, rom, table, buffers))

def test_patch_is_atomic_bounded_and_idempotent(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 282
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 282, 'relocated': 0}
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
