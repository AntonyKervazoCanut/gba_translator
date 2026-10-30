"""PT-75 : pointeurs réels, isolation et injection finale dans la ROM PT."""
import hashlib
import re
import struct
from pathlib import Path

import pytest

from languages.pt.patches.batch_75 import make_patch
from tests.unit.pt.test_batch_pt75 import AUDIT

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
        assert hits == row.get('all_reference_hits', row['references'])
        if row.get('consumer_offset'):
            consumer = int(row['consumer_offset'], 16)
            assert [m.start() for m in re.finditer(re.escape(struct.pack('<I', consumer + 0x08000000)), source)] == row['consumer_references']
        for ref, context in zip(row['references'], row['reference_contexts']):
            assert source[ref - 2:ref + 5].hex() == context


def test_every_live_entry_reaches_final_rom(source):
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    patch = make_patch(source)
    assert len(patch.entries()) == 296
    patch.verify(built)


def test_patch_is_atomic_idempotent_and_bounded(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 296
    first = bytes(rom)
    assert patch.apply(rom) == {'verified': 296, 'relocated': 0}
    assert bytes(rom) == first
    allowed = set()
    for _, refs, encoded in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = struct.unpack_from('<I', rom, ref)[0] - 0x08000000
            allowed.update(range(target, target + len(encoded)))
    assert all(i in allowed for i, (a, b) in enumerate(zip(source, rom)) if a != b)
    broken = bytearray(source)
    broken[0x1F5A677] ^= 1
    with pytest.raises(ValueError, match='préimage'):
        make_patch(bytes(broken)).apply(rom)
    assert bytes(rom) == first


def test_actual_font_budgets_in_final_rom(source):
    from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
    from src.core.font_glyphs import LATIN_FONTS

    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    rows = {int(r.get('consumer_offset', r['offset']), 16): r for r in AUDIT['entries']}
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



def test_excluded_audio_bytes_and_orphan_label_are_unchanged(source):
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    for row in AUDIT['entries']:
        for site in row.get('non_text_references', []):
            assert built[site:site + 4] == source[site:site + 4]
    row = AUDIT['entries'][143]
    offset = int(row['offset'], 16)
    raw = bytes.fromhex(row['source_hex'])
    assert not row['references'] and not row['interior_hits']
    assert built[offset:offset + len(raw)] == raw


def test_braille_routine_and_map_table_are_preserved(source):
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    for index in (13, 17, 20):
        ref = AUDIT['entries'][index]['references'][0]
        assert source[ref - 2:ref] == built[ref - 2:ref] == b'\x0f\x00'
        assert source[ref + 4:ref + 9] == built[ref + 4:ref + 9] == bytes.fromhex('235d28ec09')
    assert AUDIT['entries'][24]['consumer_references'] == [0x1EAFBC4, 0x1FB4728]
    assert AUDIT['entries'][25]['references'] == [0x1FB472C]
    assert source[0x1FB4730:0x1FB4734] == built[0x1FB4730:0x1FB4734]
