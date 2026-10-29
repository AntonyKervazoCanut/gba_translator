"""PT-23 : préimages, consommateurs, isolation et texte final réellement livré."""
import hashlib
import json
import re
from pathlib import Path

import pytest

from languages.pt.patches.batch_23 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt23_audit.json').read_text())
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_source_and_every_reference_including_unaligned(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        refs = [m.start() for m in re.finditer(
            re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert refs == row['references']
        if row['status'] == 'exception':
            assert not refs
            for consumer in row['related_consumers']:
                for site in consumer['sites']:
                    assert int.from_bytes(source[int(site, 16):int(site, 16) + 4], 'little') == int(consumer['offset'], 16) + 0x08000000
    replacement = next(r for r in AUDIT['entries'] if r['offset'] == '0x792af0')
    assert replacement['references'] == [0x792740]


def test_atomic_bounded_idempotent_patch(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 262
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 262, 'relocated': 0}
    assert bytes(rom) == after
    allowed = set()
    for _, refs, raw in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(target, target + len(raw)))
    assert {i for i, (a, b) in enumerate(zip(source, rom)) if a != b} <= allowed
    patch.definitions[0] = dict(patch.definitions[0], source_hex='00ff')
    with pytest.raises(ValueError, match='préimage'):
        patch.apply(rom)
    assert bytes(rom) == after


def test_built_rom_exact_delivery_and_no_overlap(source, built):
    patch = make_patch(source)
    patch.verify(built)
    for row, (offset, refs, encoded) in zip(
            [r for r in AUDIT['entries'] if r['status'] == 'translated'], patch.entries()):
        assert offset == int(row['offset'], 16)
        assert encoded == TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        for ref in refs:
            target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
            assert built[target:target + len(encoded)] == encoded


def test_real_font_widths_with_expanded_dynamic_buffers(source, built):
    # Cas conservateur : noms joueur/rival/espèce de 10 caractères ; saison Primavera.
    buffers = {(0xFD, 1): 'W' * 10, (0xFD, 6): 'W' * 10,
               (0xFD, 2): 'W' * 10, (0xFD, 3): 'Primavera',
               (0xFD, 4): '100'}
    season_offsets = {0x7938ED, 0x7939BC, 0x793A06, 0x793AA1}
    for offset, _, raw in make_patch(source).entries():
        dynamic = dict(buffers)
        if offset in season_offsets:
            dynamic[(0xFD, 4)] = 'Primavera'
        for font in LATIN_FONTS:
            _, table = font.offsets(built)
            for segment in re.split(b'[\xfa\xfb]', raw):
                assert max(widths(segment, built, table, dynamic)) <= 208, (hex(offset), font)
