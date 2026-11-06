"""PT-81 : pointeurs réels, isolation et injection finale dans la ROM PT."""
import hashlib
import re
import struct
from pathlib import Path

import pytest

from languages.pt.patches.batch_81 import make_patch
from tests.unit.pt.test_batch_pt81 import AUDIT

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
        assert hits == sorted(row['references'] + row.get('non_text_references', []))
        if row.get('consumer_offset'):
            consumer = int(row['consumer_offset'], 16)
            assert [m.start() for m in re.finditer(re.escape(struct.pack('<I', consumer + 0x08000000)), source)] == row['consumer_references']
        for ref, context in zip(row['references'], row['reference_contexts']):
            assert source[ref - 2:ref + 5].hex() == context


def test_every_live_entry_reaches_final_rom(source):
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    patch = make_patch(source)
    assert len(patch.entries()) == 297
    patch.verify(built)
    for row in AUDIT['entries']:
        for ref in row.get('non_text_references', []):
            assert built[ref:ref + 4] == source[ref:ref + 4]


def test_patch_is_atomic_idempotent_and_bounded(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 297
    first = bytes(rom)
    assert patch.apply(rom) == {'verified': 297, 'relocated': 0}
    assert bytes(rom) == first
    allowed = {offset + n for offset, _, _ in patch.SUFFIX_INSTRUCTIONS for n in range(2)}
    for _, refs, encoded in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = struct.unpack_from('<I', rom, ref)[0] - 0x08000000
            allowed.update(range(target, target + len(encoded)))
    assert all(i in allowed for i, (a, b) in enumerate(zip(source, rom)) if a != b)
    broken = bytearray(source)
    broken[0x1F80178] ^= 1
    with pytest.raises(ValueError, match='préimage'):
        make_patch(bytes(broken)).apply(rom)
    assert bytes(rom) == first


def test_actual_font_budgets_in_final_rom(source):
    from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
    from src.core.font_glyphs import LATIN_FONTS

    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    rows = {int(r.get('consumer_offset', r['offset']), 16): r for r in AUDIT['entries']}
    for offset, _, raw in make_patch(source).entries():
        # Les tampons runtime réservent dix glyphes larges ; les couleurs ne
        # consomment aucun pixel. Les limites sont mesurées aux pointeurs finaux.
        for command in _extract_control_sequences_from_raw(raw):
            if command[0] == 0xFD:
                raw = raw.replace(bytes(command), b'\xd1' * AUDIT['buffer_overrides'].get(f'{command[1]:02X}', AUDIT['buffer_glyph_budget']))
            elif command[0] not in (0xFA, 0xFB, 0xFE):
                raw = raw.replace(bytes(command), b'')
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            for line in re.split(b'[\xfa\xfb\xfe\xff]', raw):
                assert sum(built[widths + c] for c in line) <= rows[offset]['max_width'], (
                    hex(offset), hex(font.glyph_pointer), line.hex())



def test_exceptions_and_binary_false_pointers_are_not_repointed(source):
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    rows = AUDIT['entries']
    row = rows[11]
    parent = rows[10]
    delta = int(row['offset'], 16) - int(parent['offset'], 16)
    assert bytes.fromhex(parent['source_hex'])[delta:] == bytes.fromhex(row['source_hex'])
    pcm = row['pcm_matches'][0]
    base, size = pcm['wave_base'], int.from_bytes(source[pcm['wave_base'] + 12:pcm['wave_base'] + 16], 'little')
    assert base + 16 <= pcm['site'] < base + 16 + size
    assert built[pcm['site']:pcm['site'] + 4] == source[pcm['site']:pcm['site'] + 4]
    assert rows[155]['source_hex'] == '00' + rows[156]['source_hex']
    assert not rows[155]['references']


def test_mining_suffix_becomes_empty_for_both_article_branches(source):
    from languages.pt.patches.batch_81 import Batch81Patch

    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    for offset, before, after in Batch81Patch.SUFFIX_INSTRUCTIONS:
        assert source[offset:offset + 2] == before
        assert built[offset:offset + 2] == after
    # movs r3,#255; strb [r2]; adds r3,#0; strb [r2,#1].
    assert built[0x1EDBF5A:0x1EDBF62] == bytes.fromhex('ff23137000335370')
    # La branche sans voyelle conserve son terminateur immédiat.
    assert built[0x1EDBFA2:0x1EDBFA6] == source[0x1EDBFA2:0x1EDBFA6] == bytes.fromhex('ff231370')
