"""PT-28 : pointeurs réels, isolation et injection finale dans la ROM PT."""
import hashlib
import re
import struct
from pathlib import Path

import pytest

from languages.pt.patches.batch_28 import make_patch
from tests.unit.pt.test_batch_pt28 import AUDIT

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
    assert len(patch.entries()) == 277
    patch.verify(built)


def test_patch_is_atomic_idempotent_and_bounded(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 277
    first = bytes(rom)
    assert patch.apply(rom) == {'verified': 277, 'relocated': 0}
    assert bytes(rom) == first
    allowed = set()
    for _, refs, encoded in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = struct.unpack_from('<I', rom, ref)[0] - 0x08000000
            allowed.update(range(target, target + len(encoded)))
    assert all(i in allowed for i, (a, b) in enumerate(zip(source, rom)) if a != b)
    broken = bytearray(source)
    broken[0x7EAC5C] ^= 1
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


def test_casino_prices_keep_columns_fonts_and_original_amounts(source):
    """Les noms restent avant la colonne prix et le total tient dans 160 px."""
    from src.core.font_glyphs import LATIN_FONTS

    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    entries = {offset: (refs, raw) for offset, refs, raw in make_patch(source).entries()}
    prices = AUDIT['entries'][24:39]
    for row in prices:
        offset = int(row['offset'], 16)
        refs, raw = entries[offset]
        original = bytes.fromhex(row['source_hex'])
        position = raw.index(b'\xfc\x13')
        old_position = original.index(b'\xfc\x13')
        assert raw[:position] == original[:old_position]  # Noms conservés.
        assert raw[position:position + 6] == original[old_position:old_position + 6]
        assert raw[position + 3:position + 6] == b'\xfc\x06\x00'
        # Le bloc numérique est inchangé, seule la devise est localisée.
        assert raw[position + 6:].split(b'\x00')[:-1] == original[old_position + 6:].split(b'\x00')[:-1]
        assert len(refs) == (2 if offset <= 0x7EC760 else 1)
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            assert sum(built[widths + c] for c in raw[:position]) <= raw[position + 2]
            assert raw[position + 2] + sum(built[widths + c] for c in raw[position + 6:-1]) <= 160
