"""PT-49 : préimages, consommateurs vivants, polices et isolation binaire."""
import hashlib
import json
import re
from pathlib import Path

import pytest

from languages.fr.patches.font import lz77_decompress
from languages.pt.patches.batch_49 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from tests.e2e.pt.test_batch_pt13_rom import widths

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt49_audit.json').read_text())
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


def test_source_preimages_and_pointer_classification(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        refs = [m.start() for m in re.finditer(
            re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert refs == sorted(row['references'] + row.get('non_text_references', []))
        if row['kind'] in ('item_description', 'tm_description', 'extended_item_name'):
            delta = 0 if row['kind'] == 'extended_item_name' else 20
            for item, ref in zip(row.get('item_ids', []), refs):
                assert 0x876074 + item * 44 + delta == ref
        if row['status'] == 'exception_binary':
            assert not row['references']
            assert row.get('binary_owners') or row.get('sprite_owners')
            start = int(row['context_start'], 16)
            assert source[start:start + 64].hex() == row['context_hex']
            for owner in row.get('sprite_owners', []):
                start = int(owner['offset'], 16)
                site = int(owner['site'], 16)
                assert source[site:site + 8].hex() == owner['record_hex']
                assert int.from_bytes(source[site:site + 4], 'little') == start + 0x08000000
                assert int.from_bytes(source[site + 4:site + 8], 'little') == owner['size']
                assert start <= offset < start + owner['size']
            for owner in row.get('binary_owners', []):
                start = int(owner['offset'], 16)
                decoded, size = lz77_decompress(source, start)
                assert size == owner['compressed_bytes'] and len(decoded) == owner['decoded_bytes']
                assert start < offset < start + size
                for site in owner['references']:
                    assert int.from_bytes(source[site:site + 4], 'little') == start + 0x08000000


def test_final_rom_delivery_and_engine_widths(source):
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    patch = make_patch(source)
    patch.verify(built)
    translated = [r for r in AUDIT['entries'] if r['status'] == 'translated']
    for row, (_, refs, raw) in zip(translated, patch.entries()):
        for font in LATIN_FONTS:
            _, table = font.offsets(built)
            assert max(widths(raw, built, table, {})) <= row['layout']['max_width'], row['offset']
        assert raw.count(0xFE) == bytes.fromhex(row['source_hex']).count(0xFE)
    for row in AUDIT['entries']:
        if row['status'] == 'translated':
            continue
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert built[offset:offset + len(raw)] == raw
        for ref in row['references']:
            target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
            assert built[target:target + len(raw)] == raw


def test_patch_is_atomic_idempotent_and_bounded(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 210
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 210, 'relocated': 0}
    assert bytes(rom) == after
    allowed = set()
    for _, refs, raw in patch.entries():
        for site in refs:
            allowed.update(range(site, site + 4))
            target = int.from_bytes(rom[site:site + 4], 'little') - 0x08000000
            allowed.update(range(target, target + len(raw)))
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(source, rom)))
    patch.definitions[0]['source_hex'] = '00ff'
    with pytest.raises(ValueError, match='préimage'):
        patch.apply(rom)
    assert bytes(rom) == after
