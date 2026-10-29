"""PT-29 : pointeurs réels, tuiles intactes, cellules fixes et injection finale."""
import hashlib
import json
import re
from pathlib import Path

import pytest

from languages.pt.patches.batch_29 import make_patch
from languages.pt.patches.font import apply_patches
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt29_audit.json').read_text())
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_source_preimages_all_references_and_exception_owners(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        refs = [m.start() for m in re.finditer(
            re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert refs == row.get('raw_references', row['references'])
        assert sorted(row['references'] + row.get('non_text_references', [])) == refs
        for owner in row.get('related_consumers', []):
            for site in owner['sites']:
                p = int(site, 16)
                assert int.from_bytes(source[p:p + 4], 'little') == int(owner['offset'], 16) + 0x08000000
    title = next(r for r in AUDIT['entries'] if r['offset'] == '0x834ae7')
    assert title['consumer_offset'] == '0x834af4'
    assert title['consumer_references'] == [0x834270]
    assert int.from_bytes(source[0x834270:0x834274], 'little') == 0x08834AF4


def test_patch_atomic_bounded_idempotent_and_padding_guard(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 265
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 265, 'relocated': 0}
    assert bytes(rom) == after
    # Simule les erreurs de la passe générique sur une clé de bourrage et deux
    # motifs de pixels pris pour des pointeurs : le finaliseur les restaure.
    rom[0x834AE7:0x834AF4] = b'x' * 13
    for site in (0xFA6636, 0xFA6C32):
        rom[site:site + 4] = b'BAD!'
    assert patch.apply(rom) == {'verified': 265, 'relocated': 0}
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
    damaged = bytearray(source)
    damaged[0x834AE7] = 1
    with pytest.raises(ValueError, match='Préimage'):
        make_patch(damaged)


def test_final_rom_delivery_fixed_cells_and_graphics(source, built):
    patch = make_patch(source)
    patch.verify(built)
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            continue
        encoded = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        refs = row.get('consumer_references', row['references'])
        targets = [int.from_bytes(built[p:p + 4], 'little') - 0x08000000 for p in refs]
        if not refs:
            # Vraies cellules gItems, pas des pointeurs vers des copies mortes.
            offset = int(row['offset'], 16)
            assert offset in (0x87622C, 0x876258)
            assert (offset - 0x876200) % 44 == 0
            assert int.from_bytes(built[0x9A8D8:0x9A8DC], 'little') == 0x08876200
            targets = [offset]
        for target in targets:
            assert built[target:target + len(encoded)] == encoded
    # Une référence graphique vivante ne doit surtout pas être repointée en texte.
    assert built[0x8280F0:0x8280F8] == source[0x8280F0:0x8280F8]
    assert built[0x827F30:0x8280F0] == source[0x827F30:0x8280F0]
    # Palette et bourrage de la clé EV-IV restent intacts.
    assert built[0x834AD4:0x834AF4] == source[0x834AD4:0x834AF4]
    for site in (0xFA6636, 0xFA6C32):
        assert built[site - 16:site + 16] == source[site - 16:site + 16]


def test_real_font_widths_with_expanded_buffers(source):
    rom = bytearray(source)
    apply_patches(rom)
    for offset, _, raw in make_patch(source).entries():
        # Noms joueur/rival/espèce jusqu'à 10 caractères ; noms de pierre et talent.
        buffers = {(0xFD, i): 'W' * 10 for i in (0, 1, 2, 3, 4, 6, 15, 16, 24)}
        if offset == 0x83008C:
            buffers[(0xFD, 1)] = 'Charizardite X'
            buffers[(0xFD, 3)] = 'Mega Cuff'
        if offset in (0x830CE0, 0x830CF6, 0x830D1A):
            buffers[(0xFD, 24)] = 'Primordial Sea'
        if offset == 0x7FD7CA:
            buffers[(0xFD, 2)] = 'Psíquico'
        for font in LATIN_FONTS:
            _, table = font.offsets(rom)
            for segment in re.split(b'[\xfa\xfb]', raw):
                assert max(widths(segment, rom, table, buffers)) <= 208, hex(offset)
