"""PT-60 : vrais pointeurs, cellule fixe, isolation et polices ROM."""
import hashlib
import json
import re
from pathlib import Path

import pytest

from languages.pt.patches.batch_60 import make_patch
from languages.pt.patches.font import apply_patches
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt60_audit.json').read_text())
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_preimages_consumers_and_exceptions(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        refs = [m.start() for m in re.finditer(re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        if row['layout'] == 'fixed_title':
            assert refs == []
            assert int.from_bytes(source[row['references'][0]:row['references'][0] + 4], 'little') == offset + 1 + 0x08000000
        else:
            assert refs == sorted(row['references'] + row.get('non_text_references', []))
        if row['status'] == 'exception':
            assert row['owner_sites']
            for ref in row['owner_sites']:
                assert int.from_bytes(source[ref:ref + 4], 'little') == int(row['owner_offset'], 16) + 0x08000000


def test_all_296_delivered_in_built_rom(source, built):
    patch = make_patch(source)
    patch.verify(built)
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            continue
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        for ref in row['references']:
            target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
            delta = row.get('interior_delta', 0)
            assert built[target:target + len(raw) - delta] == raw[delta:]
    assert len(built) == len(source)


def test_patch_is_atomic_idempotent_and_bounded(source):
    patch, rom = make_patch(source), bytearray(source)
    assert patch.apply(rom)['verified'] == 296
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 296, 'relocated': 0}
    assert bytes(rom) == after
    allowed = set(range(0x1EED1B3, 0x1EED1C0))
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


def test_five_real_fonts_and_dynamic_buffers(source):
    rom = bytearray(source)
    apply_patches(rom)
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            continue
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        buffers = {(0xFD, k): 'W' * 10 for k in range(64)}
        # gItems : cellule de 14 octets, terminateur compris.
        if row['index'] in (246, 247, 248, 251):
            buffers.update({(0xFD, k): 'W' * 13 for k in (2, 3)})
        # Les quantités et adjectifs ont leurs propres limites réelles.
        if row['index'] in (178, 183):
            buffers[(0xFD, 2)] = '3'
        if row['index'] in (202, 204):
            buffers[(0xFD, 3)] = 'bonito'
        if row['index'] in (216,):
            buffers[(0xFD, 3)] = 'filha'
        # Le tampon d'ingrédients est une liste séparée par des scrolls ;
        # les listes exactes 30–32 sont déjà mesurées individuellement.
        if row['index'] in (20, 21, 22, 23, 25):
            buffers[(0xFD, 7)] = '10 Sitrus Berries'
        for font in LATIN_FONTS:
            _, table = font.offsets(rom)
            limit = 224 if row['layout'] in ('credits', 'costume') else 208
            if row['layout'] == 'mission':
                # Les objectifs utilisent la police Small (autres polices
                # mesurées aussi, sans prétendre leur donner la même fenêtre).
                limit = 192
            for segment in re.split(b'[\xfa\xfb]', raw):
                assert max(widths(segment, rom, table, buffers)) <= limit, (row['offset'], font.glyph_pointer)


def test_exception_code_and_alignment_are_real(source, built):
    rows = {r['index']: r for r in AUDIT['entries']}
    assert source[0x1EED32E:0x1EED330] == built[0x1EED32E:0x1EED330] == bytes.fromhex('c046')
    for index in (155, 156):
        for site in rows[index]['consumer_code']:
            offset, raw = int(site['offset'], 16), bytes.fromhex(site['source_hex'])
            assert source[offset:offset + len(raw)] == raw
            if offset != 0x1EB20EC:  # Le littéral texte est repointé vers la traduction.
                assert built[offset:offset + len(raw)] == raw


def test_false_pointers_are_referenced_pcm_audio(source, built):
    count = 0
    for row in AUDIT['entries']:
        for pcm in row.get('pcm_consumers', []):
            count += 1
            ref, header = int(pcm['occurrence'], 16), int(pcm['wave_header'], 16)
            size, voice = pcm['sample_bytes'], int(pcm['voicegroup_pointer'], 16)
            assert source[header:header + 16].hex() == pcm['header_hex']
            assert int.from_bytes(source[header + 12:header + 16], 'little') == size
            assert header + 16 <= ref < header + 16 + size
            assert source[voice - 4:voice] == bytes.fromhex('003c0000')
            assert int.from_bytes(source[voice:voice + 4], 'little') == header + 0x08000000
            # Les échantillons complets restent intacts après le build générique.
            assert built[header:header + 16 + size] == source[header:header + 16 + size]
    assert count == 8
