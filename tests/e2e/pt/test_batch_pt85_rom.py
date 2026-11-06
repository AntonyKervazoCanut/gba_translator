"""PT-85 : références source et injection réelle des 300 consommateurs."""
import hashlib
import re
import struct
from pathlib import Path

import pytest

from languages.pt.patches.batch_85 import make_patch
from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.font_glyphs import LATIN_FONTS
from tests.unit.pt.test_batch_pt85 import AUDIT

ROOT = Path(__file__).resolve().parents[3]
pytestmark = pytest.mark.rom


def test_references_and_final_injection():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert [m.start() for m in re.finditer(re.escape(struct.pack('<I', offset + 0x08000000)), source)] == row['references']
        assert [source[r-2:r+5].hex() for r in row['references']] == row['reference_contexts']
        if row['index'] >= 63:
            assert all(r % 4 == 0 and 0x1FB2300 <= r < 0x1FB28B0 for r in row['references'])
        else:
            assert all(0x1E9FD00 <= r < 0x1EA6000 for r in row['references'])
    patch = make_patch(source)
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    assert len(patch.entries()) == 300
    patch.verify(built)


def test_atomic_idempotent_bounded_patch():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 300
    first = bytes(rom)
    assert patch.apply(rom) == {'verified': 300, 'relocated': 0}
    allowed = set()
    for _, refs, encoded in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref+4))
            target = struct.unpack_from('<I', rom, ref)[0] - 0x08000000
            allowed.update(range(target, target+len(encoded)))
    assert all(i in allowed for i, (a,b) in enumerate(zip(source, rom)) if a != b)
    assert bytes(rom) == first
    broken = bytearray(source)
    broken[int(AUDIT['entries'][0]['offset'], 16)] ^= 1
    with pytest.raises(ValueError, match='préimage'):
        make_patch(bytes(broken)).apply(rom)
    assert bytes(rom) == first


def test_live_font_pixel_budgets():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    for index, (_, _, raw) in enumerate(make_patch(source).entries()):
        # Nombres : six chiffres ; noms d'objet/mouvement : 100 pixels ;
        # tampon pluriel : un s. Les prix utilisent FC13 (position absolue).
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            x = 0
            cursor = 0
            while cursor < len(raw):
                c = raw[cursor]
                if c == 0xFF:
                    break
                if c in (0xFA, 0xFB, 0xFE):
                    x = 0
                    cursor += 1
                    continue
                if c == 0xFD:
                    param = raw[cursor+1]
                    x += 6 if param == 7 else 100 if param == 12 or index in (38, 46) else 54 if index == 26 else 36
                    cursor += 2
                elif c == 0xFC:
                    command = _extract_control_sequences_from_raw(raw[cursor:])[0]
                    if command[1] == 0x13:
                        assert x <= command[2], (index, 'nom déborde sur prix', x, command)
                        x = command[2]
                    cursor += len(command)
                else:
                    x += built[widths+c]
                    cursor += 1
                assert x <= 192, (index, hex(font.glyph_pointer), x)
