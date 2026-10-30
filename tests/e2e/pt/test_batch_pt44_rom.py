"""PT-44 : pointeurs vivants, ROM finale, polices et faux pointeur graphique."""
import hashlib
import re

import pytest

from languages.fr.patches.font import lz77_decompress
from languages.pt.patches.batch_44 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths
from tests.unit.pt.test_batch_pt44 import AUDIT, ROOT

pytestmark = pytest.mark.rom


def test_live_references_and_final_text():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    make_patch(source).verify(built)
    table = AUDIT['trainer_table']
    base = int(table['base'], 16)
    pointer = (base + 0x08000000).to_bytes(4, 'little')
    assert [m.start() for m in re.finditer(re.escape(pointer), source)] == table['references']
    for ref in table['references']:
        assert built[ref:ref + 4] == pointer
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        assert sorted(row['references'] + row['non_text_references']) == [m.start() for m in
            re.finditer(re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        encoded = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        for ref in row['references']:
            if row['status'] == 'translated':
                assert 0xA6F580 <= ref < 0xA70000
                assert (ref - 0xA6F57C) % 20 in (0, 4, 8)
            target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
            assert built[target:target + len(encoded)] == encoded, row['offset']
        for font in LATIN_FONTS:
            _, table = font.offsets(built)
            assert max(widths(encoded.replace(b"\xfa", b"\xfe").replace(b"\xfb", b"\xfe"), built, table, {})) <= 204, row['offset']
    decoded, size = lz77_decompress(source, 0x176C93C)
    assert len(decoded) == 2048 and size == 910
    site = int(AUDIT["non_text_evidence"]["site"], 16)
    assert 0x176C93C < site < 0x176C93C + size - 3
    assert built[0x176C93C:0x176C93C + size] == source[0x176C93C:0x176C93C + size]


def test_patch_is_bounded_and_idempotent():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 249
    before = bytes(rom)
    assert patch.apply(rom) == {'verified': 249, 'relocated': 0}
    assert rom == before
    allowed = set()
    for _, refs, raw in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(target, target + len(raw)))
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(source, rom)))
