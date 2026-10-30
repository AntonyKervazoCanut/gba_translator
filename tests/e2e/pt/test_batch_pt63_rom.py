"""PT-63 : octets livrés, pointeurs vivants et budgets des cinq polices."""
import hashlib
import re

import pytest

from languages.pt.patches.batch_63 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths
from tests.unit.pt.test_batch_pt63 import AUDIT, ROOT

pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_source_pointers_and_documented_exceptions(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[off:off + len(raw)] == raw
        assert [m.start() for m in re.finditer(
            re.escape((off + 0x08000000).to_bytes(4, 'little')), source)] == row['references']
        if row['status'] == 'exception':
            assert source[off - 16:off + 32] == bytes.fromhex(row['context_hex'])
            ref = int(row['replacement_pointer'], 16)
            assert int.from_bytes(source[ref:ref + 4], 'little') == int(row['replacement_target'], 16) + 0x08000000


def test_final_delivery_and_unused_text_preserved(source, built):
    patch = make_patch(source)
    assert len(patch.entries()) == 291
    patch.verify(built)
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            off = int(row['offset'], 16)
            raw = bytes.fromhex(row['source_hex'])
            assert built[off:off + len(raw)] == raw
    probe = bytearray(built)
    assert patch.apply(probe) == {'verified': 291, 'relocated': 0}
    assert probe == built


def test_native_font_budgets_and_expanded_runtime_buffers(built):
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            continue
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        buffers = {(0xFD, int(k)): v for k, v in row['buffers'].items()}
        for font in LATIN_FONTS:
            _, table = font.offsets(built)
            for page in re.split(b'[\xfa\xfb]', raw):
                measured = widths(page, built, table, buffers)
                assert max(measured) <= row['native_max_width'], (row['offset'], font.glyph_pointer, measured)


def test_finalizer_atomic_idempotent_and_bounded(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 291
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 291, 'relocated': 0}
    assert rom == after
    allowed = set()
    for _, refs, raw in patch.entries():
        for ref in refs:
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(ref, ref + 4))
            allowed.update(range(target, target + len(raw)))
    assert {i for i, (a, b) in enumerate(zip(source, rom)) if a != b} <= allowed
    patch.definitions[-1] = dict(patch.definitions[-1], source_hex='00ff')
    with pytest.raises(ValueError, match='préimage'):
        patch.apply(rom)
    assert rom == after
