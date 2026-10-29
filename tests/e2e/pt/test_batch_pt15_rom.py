"""PT-15 : octets livrés, tables, pointeurs, isolation et polices réelles."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pytest

from languages.pt.patches.batch_15 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt15_audit.json').read_text())
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_source_consumers_and_exceptions(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        target = offset + row['source_delta']
        refs = [m.start() for m in re.finditer(
            re.escape((target + 0x08000000).to_bytes(4, 'little')), source)]
        assert refs == row['references'], row['offset']
    assert int.from_bytes(source[0x414770:0x414774], 'little') == 0x0841DC48
    # Table fixe des fiches : repointer sa cellule, jamais agrandir sur place.
    dex = [r for r in AUDIT['entries'] if int(r['offset'], 16) >= 0x444CB2]
    assert [r['references'] for r in dex] == [[0x1A35800 + 36 * i] for i in range(85)]


def test_patch_is_bounded_atomic_and_idempotent(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 273
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 273, 'relocated': 0}
    assert bytes(rom) == after
    allowed = set()
    for _, refs, raw in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(target, target + len(raw)))
    changed = {i for i, (a, b) in enumerate(zip(source, rom)) if a != b}
    assert changed <= allowed
    patch.definitions[0]['source_hex'] = '00ff'
    with pytest.raises(ValueError, match='préimage'):
        patch.apply(rom)
    assert bytes(rom) == after


def test_final_rom_delivers_every_text(source, built):
    patch = make_patch(source)
    patch.verify(built)
    rows = [r for r in AUDIT['entries'] if r['status'] == 'translated']
    for row, (_, refs, raw) in zip(rows, patch.entries()):
        expected = TextEncoder.encode_pokemon(
            row['portuguese'][row['source_delta']:].replace(r'\n', '\n'), strict=True)
        assert raw == expected
        for ref in refs:
            target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
            assert built[target:target + len(raw)] == expected


def test_real_font_budgets_and_fixed_columns(source, built):
    buffers = {(0xFD, n): 'W' * 10 for n in (2, 3, 4)}
    buffers.update({(0xF7, n): '999' for n in range(4)})
    for offset, _, raw in make_patch(source).entries():
        limit = 232 if offset >= 0x444C35 else 224 if offset < 0x41DE9D else 208
        for font in LATIN_FONTS:
            _, table = font.offsets(built)
            for page in raw.split(b'\xfb'):
                assert max(widths(page, built, table, buffers)) <= limit, (hex(offset), font)
