"""PT-70 : pointeurs réels, isolation et injection finale dans la ROM PT."""
import hashlib
import re
import struct
from pathlib import Path

import pytest

from languages.pt.patches.batch_70 import make_patch
from tests.unit.pt.test_batch_pt70 import AUDIT

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
    assert len(patch.entries()) == 298
    patch.verify(built)


def test_patch_is_atomic_idempotent_and_bounded(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 298
    first = bytes(rom)
    assert patch.apply(rom) == {'verified': 298, 'relocated': 0}
    assert bytes(rom) == first
    allowed = set()
    for _, refs, encoded in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = struct.unpack_from('<I', rom, ref)[0] - 0x08000000
            allowed.update(range(target, target + len(encoded)))
    allowed.update(range(0x1E8A91C, 0x1E8A921))
    assert all(i in allowed for i, (a, b) in enumerate(zip(source, rom)) if a != b)
    broken = bytearray(source)
    broken[0x1F317F2] ^= 1
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


def test_orphan_text_and_false_interior_references_remain_untouched(source):
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    row = next(r for r in AUDIT['entries'] if r['status'] == 'exception')
    offset = int(row['offset'], 16)
    raw = bytes.fromhex(row['source_hex'])
    assert built[offset:offset + len(raw)] == source[offset:offset + len(raw)] == raw
    assert not row['interior_hits']
    for site in (0x13DF497, 0x13E7D7B):
        assert built[site:site + 4] == source[site:site + 4]


def test_gender_buffer_uses_existing_subjects_without_touching_other_dialogues(source):
    from tests.unit.pt.test_batch_pt10 import entries

    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    row = AUDIT['entries'][238]
    setup = row['buffer_setup']
    site = setup['call_offset']
    assert source[site:site + 5].hex() == setup['source_hex']
    assert built[site:site + 5].hex() == setup['replacement_hex']
    assert source[site + 5:row['references'][0] - 2] == built[site + 5:row['references'][0] - 2]
    # checkgender : homme -> 0x7522ab, femme -> 0x7522be ; buffer 0 = FD02.
    expected_helper = bytes.fromhex('a0210d8000000701ab227508210d8001000701be22750803')
    assert source[0x1E6E06A:0x1E6E06A + len(expected_helper)] == expected_helper
    for script, key, expected in [(0x7522AB, 0x789224, 'ele'), (0x7522BE, 0x78922E, 'ela')]:
        assert source[script:script + 2] == b'\x85\x00'
        assert struct.unpack_from('<I', source, script + 2)[0] == key + 0x08000000
        assert entries()[key] == expected
        target = struct.unpack_from('<I', built, script + 2)[0] - 0x08000000
        from src.core.text_codec import TextEncoder
        raw = TextEncoder.encode_pokemon(expected, strict=True)
        assert built[target:target + len(raw)] == raw
    assert '<0xFD><0x02> está vindo' in row['portuguese']
