"""PT-27 : pointeurs réels, isolation et injection finale dans la ROM PT."""
import hashlib
import re
import struct
from pathlib import Path

import pytest

from languages.pt.patches.batch_27 import make_patch
from tests.unit.pt.test_batch_pt27 import AUDIT

ROOT = Path(__file__).resolve().parents[3]
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


def test_source_references_and_consumer_contexts(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        hits = [m.start() for m in re.finditer(re.escape(struct.pack('<I', offset + 0x08000000)), source)]
        assert hits == row['references']
        for ref, context in zip(hits, row['reference_contexts']):
            assert source[ref - 2:ref + 5].hex() == context


def test_every_live_entry_reaches_final_rom(source):
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    patch = make_patch(source)
    assert len(patch.entries()) == 270
    patch.verify(built)


def test_patch_is_atomic_idempotent_and_bounded(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 270
    first = bytes(rom)
    assert patch.apply(rom) == {'verified': 270, 'relocated': 0}
    assert bytes(rom) == first
    allowed = set()
    for _, refs, encoded in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = struct.unpack_from('<I', rom, ref)[0] - 0x08000000
            allowed.update(range(target, target + len(encoded)))
    assert all(i in allowed for i, (a, b) in enumerate(zip(source, rom)) if a != b)
    broken = bytearray(source)
    broken[0x7D61AD] ^= 1
    with pytest.raises(ValueError, match='préimage'):
        make_patch(bytes(broken)).apply(rom)
    assert bytes(rom) == first


def test_actual_font_budgets_in_final_rom(source):
    from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
    from src.core.font_glyphs import LATIN_FONTS

    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    rows = {int(r['offset'], 16): r for r in AUDIT['entries']}
    for offset, _, raw in make_patch(source).entries():
        # Les tampons runtime réservent neuf glyphes larges ; les couleurs ne
        # consomment aucun pixel. Les limites sont mesurées aux pointeurs finaux.
        for command in _extract_control_sequences_from_raw(raw):
            if command[0] == 0xFD:
                raw = raw.replace(bytes(command), b'\xd1' * 9)
            elif command[0] not in (0xFA, 0xFB, 0xFE):
                raw = raw.replace(bytes(command), b'')
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            for line in re.split(b'[\xfa\xfb\xfe\xff]', raw):
                assert sum(built[widths + c] for c in line) <= rows[offset]['max_width'], (
                    hex(offset), hex(font.glyph_pointer), line.hex())


def test_corrupted_and_thumb_exceptions_have_concrete_evidence(source):
    # Le vrai msgbox corrompu vise un préfixe de script, pas le texte sain.
    assert struct.unpack_from('<I', source, 0x7E97B6)[0] == 0x087E97F3
    assert source[0x7E97F3:0x7E9805].hex() == '75084f07004e167c08510000160650020002'
    # La coïncidence commence au milieu du suffixe d'un BL Thumb 32 bits.
    prefix, suffix = struct.unpack_from('<HH', source, 0x5D290)
    assert prefix & 0xF800 == 0xF000 and suffix & 0xF800 == 0xF800
    assert struct.unpack_from('<I', source, 0x5D293)[0] == 0x087EA1FB
    patch = make_patch(source)
    refs = {p for _, references, _ in patch.entries() for p in references}
    assert 0x7E97B6 not in refs and 0x5D293 not in refs
