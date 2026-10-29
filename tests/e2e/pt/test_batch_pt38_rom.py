"""PT-38 : préimages, injection réelle, isolation et polices du moteur."""
import hashlib
import json
import re
from pathlib import Path

import pytest

from languages.pt.patches.batch_38 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.moves import iter_entries
from tests.e2e.pt.test_batch_pt13_rom import widths

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt38_audit.json').read_text())
pytestmark = pytest.mark.rom


def test_live_source_and_final_injection():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    patch = make_patch(source)
    patch.verify(built)
    source_moves = list(iter_entries(source))
    for row, (offset, refs, raw) in zip(AUDIT['entries'], patch.entries()):
        assert source[offset:offset + len(bytes.fromhex(row['source_hex']))].hex() == row['source_hex']
        assert sorted(refs + row['non_text_references']) == [m.start() for m in re.finditer(
            re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert row['move_ids'] == [m.index for m in source_moves if m.text_offset == offset]
        for font in LATIN_FONTS:
            _, table = font.offsets(built)
            assert max(widths(raw, built, table, {})) <= 122, (row['offset'], font)
    selected = {i for r in AUDIT['entries'] for i in r['move_ids']}
    selected_refs = {p for _, refs, _ in patch.entries() for p in refs}
    for entry in source_moves:
        if entry.index not in selected:
            assert entry.struct_offset not in selected_refs


def test_bounded_atomic_idempotent_patch():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 283
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 283, 'relocated': 0}
    assert bytes(rom) == after
    allowed = set()
    for _, refs, raw in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(target, target + len(raw)))
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(source, rom)))
    for evidence in AUDIT['non_text_evidence']:
        start = int(evidence['start'], 16)
        size = evidence['physical_bytes']
        assert rom[start:start + size] == source[start:start + size]
    patch.definitions[0]['source_hex'] = '00ff'
    with pytest.raises(ValueError, match='préimage'):
        patch.apply(rom)
    assert bytes(rom) == after


def test_false_pointer_is_inside_a_referenced_audio_sample():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    evidence, = AUDIT['non_text_evidence']
    start = int(evidence['start'], 16)
    assert source[start:start + 16].hex() == evidence['header_hex']
    samples = int.from_bytes(source[start + 12:start + 16], 'little')
    assert samples == evidence['samples']
    assert evidence['physical_bytes'] == 16 + ((samples + 63) // 64) * 33
    assert start + 16 < int(evidence['site'], 16) < start + evidence['physical_bytes'] - 3
    for ref in evidence['header_references']:
        assert int.from_bytes(source[int(ref, 16):int(ref, 16) + 4], 'little') == start + 0x08000000
