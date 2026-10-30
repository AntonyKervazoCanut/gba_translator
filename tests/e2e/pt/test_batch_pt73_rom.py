"""PT-73 : lecteurs réels, fenêtres Options et injection atomique bornée."""
import hashlib
import re

import pytest

from languages.pt.patches.batch_73 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths
from tests.unit.pt.test_batch_pt73 import ROOT, audit

pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_all_readers_and_exceptions(source, built):
    data = audit()
    assert hashlib.sha256(source).hexdigest() == data['source_sha256']
    patch = make_patch(source)
    patch.verify(built)
    for row in data['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        found = [m.start() for m in re.finditer(
            re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert sorted(found) == sorted(row['references'] + row['non_text_references'])
        if row['status'] == 'exception':
            assert not found and row['reason']
            continue
        encoded = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        for ref in row['references']:
            target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
            assert built[target:target + len(encoded)] == encoded, row['offset']
        for ref in row['non_text_references']:
            assert built[ref:ref + 4] == source[ref:ref + 4]


def test_real_fonts_with_expanded_buffers(built):
    for row in audit()['entries']:
        if row['status'] == 'exception':
            continue
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        buffers = {(0xFD, int(k)): v for k, v in row['buffers'].items()}
        measured = [max(max(widths(segment, built, font.offsets(built)[1], buffers))
                        for segment in re.split(b'[\xfa\xfb]', raw)) for font in LATIN_FONTS]
        assert measured == row['expanded_widths'], row['offset']
        assert max(measured) <= row['pixel_budget'], row['offset']
        if row.get('byte_budget'):
            assert len(raw) <= row['byte_budget']


def test_patch_atomic_idempotent_and_bounded(source):
    patch = make_patch(source)
    rom = bytearray(source)
    entries = patch.entries()
    assert patch.apply(rom)['verified'] == len(entries)
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': len(entries), 'relocated': 0}
    assert bytes(rom) == after
    allowed = set()
    local = audit()['runtime_buffers']['croagunk_local_fix']
    site = int(local['literal_site'], 16)
    base = int.from_bytes(rom[site:site + 4], 'little') - 0x08000000
    allowed.update(range(site, site + 4))
    allowed.update(range(base + 32, base + 48 + sum(map(len, patch.local_strings()))))
    for _, refs, encoded in entries:
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(target, target + len(encoded)))
    assert {i for i, (a, b) in enumerate(zip(source, rom)) if a != b} <= allowed
    ref = entries[0][1][0]
    rom[ref:ref + 4] = bytes(4)
    corrupted = bytes(rom)
    with pytest.raises(ValueError, match='hors ROM'):
        patch.apply(rom)
    assert bytes(rom) == corrupted
    with pytest.raises(ValueError, match='préimage ROM'):
        make_patch(bytes(1) + source[1:])


def test_runtime_consumers_and_pcm_evidence(source, built):
    data = audit()
    for group in data['runtime_buffers']['rows']:
        for evidence in group['evidence']:
            start, raw = int(evidence['offset'], 16), bytes.fromhex(evidence['source_hex'])
            assert source[start:start + len(raw)] == raw
    for row in data['entries']:
        for pcm in row.get('pcm_matches', []):
            start = pcm['wave_base']
            header = bytes.fromhex(pcm['header_hex'])
            assert source[start:start + 16] == header
            ref = pcm['instrument_pointer']
            assert int.from_bytes(source[ref:ref + 4], 'little') == start + 0x08000000
            assert start + 16 <= pcm['site'] < start + 16 + int.from_bytes(header[12:16], 'little')
    local = data['runtime_buffers']['croagunk_local_fix']
    # La table partagée et toutes les chaînes d'autres lots restent intactes.
    for row in local['descriptors']:
        start = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[start:start + len(raw)] == raw
        assert built[start:start + len(raw)] == raw
        site = int(row['pointer_site'], 16)
        assert built[site:site + 4] == source[site:site + 4]
    function = int(local['function'], 16)
    helper = bytes.fromhex(local['function_source_hex'])
    literal = int(local['literal_site'], 16) - function
    assert built[function:function + literal] == helper[:literal]
    assert built[function + literal + 4:function + len(helper)] == helper[literal + 4:]
    call = int(local['function_pointer_site'], 16)
    assert [m.start() for m in re.finditer(re.escape(
        (function + 0x08000001).to_bytes(4, 'little')), source)] == [call]
    options = data['options_evidence']
    for offset_key, hex_key in (
        ('label_copy_code_offset', 'label_copy_code_hex'),
        ('window_templates_offset', 'window_templates_hex'),
        ('label_item_x_literal', 'label_item_x_literal_hex'),
        ('value_draw_function', 'value_draw_hex'),
        ('options_table_read_code', 'options_table_read_hex'),
    ):
        start = int(options[offset_key], 16)
        raw = bytes.fromhex(options[hex_key])
        assert source[start:start + len(raw)] == raw
        assert built[start:start + len(raw)] == raw
