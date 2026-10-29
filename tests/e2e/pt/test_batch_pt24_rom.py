"""PT-24 : consommateurs réels, budgets des polices et écritures bornées."""
import hashlib
import json
import re
from pathlib import Path

import pytest

from languages.pt.patches.batch_24 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt24_audit.json').read_text())
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_source_consumers_items_and_exceptions(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        refs = [m.start() for m in re.finditer(
            re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert refs == row['references']
        for item, ref in zip(row.get('item_ids', []), refs):
            assert 0x876074 + item * 44 + 0x14 == ref
        if row['status'] == 'exception' and 'owner_offset' in row:
            owner = int(row['owner_offset'], 16)
            owner_raw = bytes.fromhex(row['owner_source_hex'])
            assert source[owner:owner + len(owner_raw)] == owner_raw
            for ref in row['owner_sites']:
                assert int.from_bytes(source[ref:ref + 4], 'little') == owner + 0x08000000
    assert sum(bool(r.get('item_ids')) for r in AUDIT['entries']) == 23
    corrupt = [r['offset'] for r in AUDIT['entries'] if
               r['status'] == 'exception' and r['references']]
    assert corrupt == ['0x7ab089', '0x7b4a4e', '0x7b8edd']


def test_patch_atomic_idempotent_and_no_neighbor_writes(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 255
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 255, 'relocated': 0}
    assert bytes(rom) == after
    allowed = set()
    for _, refs, raw in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(target, target + len(raw)))
    changed = {i for i, (a, b) in enumerate(zip(source, rom)) if a != b}
    assert changed <= allowed
    patch.definitions[0]['source_hex'] = '00ff'
    with pytest.raises(ValueError, match='préimage'):
        patch.apply(rom)
    assert bytes(rom) == after


def test_final_rom_exact_delivery_and_actual_fonts(source, built):
    patch = make_patch(source)
    patch.verify(built)
    patch.verify_source_spans(built)
    for row in AUDIT['entries']:
        if row['status'] == 'exception' and row['references']:
            raw = bytes.fromhex(row['source_hex'])
            for ref in row['references']:
                target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
                assert target == int(row['offset'], 16)
                assert built[target:target + len(raw)] == raw
    rows = [r for r in AUDIT['entries'] if r['status'] != 'exception']
    for row, (offset, refs, raw) in zip(rows, patch.entries()):
        expected = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        assert raw == expected
        for ref in refs:
            target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
            assert built[target:target + len(raw)] == expected
        for font in LATIN_FONTS:
            _, table = font.offsets(built)
            for page in re.split(b'[\xfa\xfb]', raw):
                measured = widths(page, built, table, {(0xFD, 1): 'W' * 10, (0xFD, 2): 'W' * 10})
                assert max(measured) <= row['layout']['max_width'], (hex(offset), font)


def test_generic_in_place_writes_do_not_destroy_shared_suffixes(source):
    patch = make_patch(source)
    rom = bytearray(source)
    # Reproduire une passe generique qui a raccourci les parents sur place.
    # Le patch doit les reloger tout en conservant les suffixes anglais,
    # y compris ceux dont les pointeurs ne figurent pas dans notre lot.
    for offset, _, raw in patch.entries():
        original = next(r for r in AUDIT['entries'] if int(r['offset'], 16) == offset)
        if len(raw) <= len(bytes.fromhex(original['source_hex'])):
            rom[offset:offset + len(raw)] = raw
    patch.apply(rom)
    patch.verify(rom)
    patch.verify_source_spans(rom)
    for row in AUDIT['entries']:
        if row['status'] == 'exception' and row['references']:
            raw = bytes.fromhex(row['source_hex'])
            for ref in row['references']:
                target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
                assert target == int(row['offset'], 16)
                assert rom[target:target + len(raw)] == raw
