"""PT-65 : injection finale, pointeurs, isolation et budgets des polices réelles."""
import hashlib
import json
import re
from pathlib import Path

import pytest

from languages.pt.patches.batch_65 import make_patch
from languages.pt.patches.font import apply_patches
from src.core.font_glyphs import LATIN_FONTS
from tests.e2e.pt.test_batch_pt13_rom import widths

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt65_audit.json').read_text())
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_source_references_and_exceptions(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        refs = [m.start() for m in re.finditer(re.escape(
            (offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert refs == sorted(row['references'] + row['non_text_references'])
        if row['status'] == 'exception':
            for ref in row['owner_sites']:
                assert int.from_bytes(source[ref:ref + 4], 'little') == int(row['owner_offset'], 16) + 0x08000000
            for site in row.get('consumer_code', []):
                start, preimage = int(site['offset'], 16), bytes.fromhex(site['source_hex'])
                assert source[start:start + len(preimage)] == preimage


def test_all_293_strings_are_delivered(source, built):
    patch = make_patch(source)
    assert len(patch.entries()) == 293
    patch.verify(built)
    assert len(built) == len(source)
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            offset = int(row['offset'], 16)
            raw = bytes.fromhex(row['source_hex'])
            assert built[offset:offset + len(raw)] == raw


def test_atomic_idempotent_and_bounded(source):
    patch, rom = make_patch(source), bytearray(source)
    assert patch.apply(rom)['verified'] == 293
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 293, 'relocated': 0}
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


def test_real_font_columns_and_dynamic_buffers(source):
    rom = bytearray(source)
    apply_patches(rom)
    rows = {int(r['offset'], 16): r for r in AUDIT['entries']}
    for offset, _, raw in make_patch(source).entries():
        row = rows[offset]
        buffers = {(0xFD, k): 'W' * 10 for k in range(64)}
        # Noms d'objets : cellule moteur de 14 octets, nul inclus.
        if row['index'] in (41, 42, 43, 44, 45, 293):
            buffers[(0xFD, 2)] = 'W' * 13
        if row['index'] == 43:
            buffers[(0xFD, 4)] = '99'
        if row['index'] in (43, 44):
            buffers[(0xFD, 3)] = '99999'
        if row['index'] in (82, 99, 101, 103, 110, 114, 236, 238, 240):
            buffers[(0xFD, 2)] = '99999'
            buffers[(0xFD, 3)] = '99999'
            buffers[(0xFD, 4)] = '99999'
        if row['index'] in (145, 148, 153, 154):
            buffers[(0xFD, 2)] = 'Especialista'
        if row['index'] == 212:
            buffers.update({(0xFD, 4): 'filha', (0xFD, 3): 'ela', (0xFD, 2): 'ela'})
        if row['index'] == 227:
            buffers.update({(0xFD, 2): '12', (0xFD, 3): '31', (0xFD, 4): '2026',
                            (0xFD, 7): '11', (0xFD, 8): '59', (0xFD, 10): 'PM'})
        # FC 06 00 sélectionne Small avant le prix des fiches.
        fonts = LATIN_FONTS[:1] if 36 <= row['index'] <= 39 else LATIN_FONTS
        for font in fonts:
            _, table = font.offsets(rom)
            limit = 224 if row['layout'] == 'fullscreen' else 208
            if row['layout'] == 'mission':
                limit = 192
            for page in re.split(b'[\xfa\xfb]', raw):
                assert max(widths(page, rom, table, buffers)) <= limit, (row['index'], hex(font.glyph_pointer))


def test_false_pointers_are_live_pcm_samples(source, built):
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
            assert built[header:header + 16 + size] == source[header:header + 16 + size]
    assert count == 2


def test_generic_audio_repoint_is_restored(source):
    patch, rom = make_patch(source), bytearray(source)
    refs = [p for r in AUDIT['entries'] for p in r['non_text_references']]
    assert len(refs) == 2
    for ref in refs:
        rom[ref:ref + 4] = (0x09FFFFFF).to_bytes(4, 'little')
    patch.apply(rom)
    for ref in refs:
        assert rom[ref:ref + 4] == source[ref:ref + 4]
