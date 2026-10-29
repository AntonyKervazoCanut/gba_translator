"""PT-18 : préimages réelles, références, budgets et injection finale."""
import hashlib
import json
import re
import struct
from pathlib import Path

import pytest

from languages.pt.patches.batch_18 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt18_audit.json').read_text())
ROWS = AUDIT['entries']
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_source_hash_and_all_pointer_claims(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in ROWS:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        hits = [hex(m.start()) for m in re.finditer(
            re.escape(struct.pack('<I', offset + 0x08000000)), source)]
        assert hits == row['source_sites']
        if row['status'] == 'exception' and 'replacement' in row:
            target = int(row['replacement']['target'], 16)
            if row.get('exception_kind') != 'obsolete_description':
                assert not hits
            else:
                assert hits == [hex(p) for p in row['legacy_references']]
                for site in (0xE5440, 0x137BC8):
                    assert struct.unpack_from('<I', source, site)[0] == 0x0899F194
            replacement_raw = bytes.fromhex(row['replacement']['source_hex'])
            assert source[target:target + len(replacement_raw)] == replacement_raw
            for ref in row['replacement']['references']:
                assert struct.unpack_from('<I', source, ref)[0] == target + 0x08000000
        if 'table_root' in row:
            assert struct.unpack_from('<I', source, int(row['table_literal'], 16))[0] == int(row['table_root'], 16) + 0x08000000
            for ref in row['record_block_references']:
                assert struct.unpack_from('<I', source, int(ref, 16))[0] == int(row['record_block'], 16) + 0x08000000


def test_final_targets_exact_controls_and_no_overlap(source, built):
    patch = make_patch(source)
    assert len(patch.entries()) == 204
    patch.verify(built)
    delivered = [r for r in ROWS if r['status'] in ('translated', 'retained')]
    for row, (offset, refs, raw) in zip(delivered, patch.entries()):
        assert offset == int(row['target'], 16)
        assert raw == TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        assert commands(raw) == commands(bytes.fromhex(row['source_hex']))
        for ref in refs:
            target = struct.unpack_from('<I', built, ref)[0] - 0x08000000
            assert built[target:target + len(raw)] == raw
    # Les noms propres et faux positifs binaires restent byte-perfect.
    for row in ROWS:
        if row['status'] == 'retained_inline' or row['status'] == 'exception' and ('replacement' not in row or row.get('exception_kind') == 'obsolete_description'):
            offset = int(row['offset'], 16)
            raw = bytes.fromhex(row['source_hex'])
            assert built[offset:offset + len(raw)] == raw


def test_real_fonts_and_exact_description_line_counts(source, built):
    for row, (_, _, encoded) in zip(
        [r for r in ROWS if r['status'] in ('translated', 'retained')], make_patch(source).entries()
    ):
        raw = encoded
        for command in commands(raw):
            if command[0] not in (0xFA, 0xFB, 0xFE):
                raw = raw.replace(command, b'')
        cap = 122 if int(row['offset'], 16) >= 0x482834 else 224
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            for line in re.split(b'[\xfa\xfb\xfe\xff]', raw):
                assert sum(built[widths + c] for c in line) <= cap, (row['offset'], cap)
        if cap == 122:
            assert encoded.count(b'\xfe') == bytes.fromhex(row['source_hex']).count(b'\xfe')
            assert encoded.count(b'\xfe') < 5


def test_routing_only_declared_cells_idempotence_and_preimage_guard(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 204
    first = bytes(rom)
    assert patch.apply(rom) == {'verified': 204, 'relocated': 0}
    assert bytes(rom) == first
    allowed = set()
    for _, refs, raw in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = struct.unpack_from('<I', rom, ref)[0] - 0x08000000
            allowed.update(range(target, target + len(raw)))
    assert all(i in allowed for i, (a, b) in enumerate(zip(source, rom)) if a != b)
    corrupt = bytearray(source)
    corrupt[0x482834] ^= 1
    with pytest.raises(ValueError, match='préimage'):
        make_patch(bytes(corrupt)).apply(rom)
    assert bytes(rom) == first


def test_trade_header_columns_and_long_buffers(source, built):
    texts = make_patch(source).texts
    # CLEAR_TO x=60/110/198 ; chaque libellé reste dans sa colonne.
    for font in LATIN_FONTS:
        _, widths = font.offsets(built)
        for label, budget in [('Nome', 60), ('Busca', 50), ('Oferta', 88), ('Nv.', 42)]:
            raw = TextEncoder.encode_pokemon(label, strict=True)[:-1]
            assert sum(built[widths + c] for c in raw) <= budget
    for offset in (0x458A98, 0x458DBC, 0x458E70, 0x458ED0, 0x458F04, 0x458F2C, 0x458F60, 0x459238, 0x459250):
        # Type en majuscules (10 glyphes), nom joueur (7), niveau (3).
        text = texts[offset]
        if offset == 0x458DBC:
            text = text.replace('<0xFD><0x03>', '100').replace('<0xFD><0x02>', 'W' * 10)
        elif offset == 0x458ED0:
            text = text.replace('<0xFD><0x03>', 'W' * 10).replace('<0xFD><0x02>', 'W' * 7)
        else:
            text = re.sub(r'<0xFD><0x[0-9A-F]{2}>', 'W' * 7, text)
        raw = TextEncoder.encode_pokemon(text.replace(r'\n', '\n'), strict=True)
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            for line in re.split(b'[\xfa\xfb\xfe\xff]', raw):
                assert sum(built[widths + c] for c in line) <= 224, hex(offset)
