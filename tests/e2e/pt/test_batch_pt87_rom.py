"""PT-87 : consommateurs, exceptions binaires et tampons réels en ROM finale."""
from __future__ import annotations

import hashlib
import re

import pytest

from languages.pt.patches.batch_87 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths
from tests.unit.pt.test_batch_pt87 import ROOT, audit

pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_all_preimages_references_and_exceptions(source):
    data = audit()
    assert hashlib.sha256(source).hexdigest() == data['source_sha256']
    for row in data['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        matches = [m.start() for m in re.finditer(re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert matches == sorted(row['references'] + row['non_text_references'])
        if row['status'] != 'exception':
            continue
        assert not row['references'] and row['reason']
        if 'owner_offset' in row:
            owner = int(row['owner_offset'], 16)
            for ref in row['owner_references']:
                assert int.from_bytes(source[ref:ref + 4], 'little') == owner + 0x08000000
        if row['index'] == 199:
            assert not row.get('interior_references')


def test_every_final_consumer_delivers_complete_translation(source, built):
    patch = make_patch(source)
    # Le possessif féminin est un second groupe de lecteurs pour la même clé.
    assert len(patch.entries()) == 295
    patch.verify(built)
    for _, refs, expected in patch.entries():
        for ref in refs:
            target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
            assert built[target:target + len(expected)] == expected
    copy = bytearray(built)
    assert patch.apply(copy) == {'verified': 295, 'relocated': 0}
    assert copy == built


def test_native_fonts_and_runtime_buffer_widths(built):
    for row in audit()['entries']:
        if row['status'] == 'exception':
            continue
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        buffers = {(0xFD, int(k)): v for k, v in row['buffers'].items()}
        measurements = []
        for font in LATIN_FONTS:
            _, table = font.offsets(built)
            measured = [w for part in re.split(b'[\xfa\xfb]', raw) for w in widths(part, built, table, buffers)]
            assert max(measured) <= row['max_width'], (row['offset'], measured, font)
            measurements.append(measured)
        assert measurements == row['native_widths']


def test_dead_text_false_pointers_are_live_binary_data(source, built):
    for index in (43, 44, 194):
        row = audit()['entries'][index]
        owner = row['binary_owner']
        if owner['kind'] == 'delta_pcm':
            start, end = int(owner['wave_base'], 16), int(owner['compressed_payload_end'], 16)
            header = bytes.fromhex(owner['header_hex'])
            assert source[start:start + 16] == header
            samples = int.from_bytes(header[12:16], 'little') + 1
            blocks, tail = divmod(samples, 64)
            assert samples == owner['decoded_samples']
            assert end == start + 16 + blocks * 33 + (1 + (tail + 1) // 2 if tail else 0)
            assert hashlib.sha256(source[start + 16:end]).hexdigest() == owner['payload_sha256']
            for instrument in owner['instrument_rows']:
                site = int(instrument['offset'], 16)
                assert source[site:site + 12] == bytes.fromhex(instrument['hex'])
                assert built[site:site + 12] == source[site:site + 12]
        else:
            start, end = int(owner['start'], 16), int(owner['end'], 16)
            assert source[start:end] == bytes.fromhex(owner['source_hex'])
        assert built[start:end] == source[start:end], index


def test_patch_atomic_idempotent_and_strictly_bounded(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 295
    final = bytes(rom)
    assert patch.apply(rom) == {'verified': 295, 'relocated': 0}
    assert bytes(rom) == final
    allowed = set()
    for _, refs, raw in patch.entries():
        for ref in refs:
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(ref, ref + 4))
            allowed.update(range(target, target + len(raw)))
    assert {i for i, (a, b) in enumerate(zip(source, final)) if a != b} <= allowed
    patch.contextual_possessive = dict(patch.contextual_possessive, source_instruction_hex='000000000000')
    with pytest.raises(ValueError, match='possessif'):
        patch.apply(rom)
    assert bytes(rom) == final


def test_both_genders_expand_to_correct_possessive_without_changing_objects(source, built):
    data = audit()
    row = data['entries'][177]
    template = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
    for sites in ((0x1EAB917, 0x1EAB91D, 0x1EAB923), (0x1EAB92A, 0x1EAB930, 0x1EAB936)):
        expanded = template
        values = []
        for slot, ref in enumerate(sites, start=2):
            assert source[ref - 2:ref] == bytes([0x85, slot - 2])
            assert built[ref - 2:ref] == source[ref - 2:ref]
            target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
            raw = built[target:built.index(255, target)]
            values.append(raw)
            expanded = expanded.replace(bytes([0xFD, slot]), raw)
        assert values[0] == TextEncoder.encode_pokemon('ele' if sites[0] == 0x1EAB917 else 'ela')[:-1]
        assert values[-1] == TextEncoder.encode_pokemon('sua')[:-1]
        for font in LATIN_FONTS:
            assert max(w for page in re.split(b'[\xfa\xfb]', expanded)
                       for w in widths(page, built, font.offsets(built)[1])) <= 192


def test_already_translated_shared_title_suffix_is_cloned_once(source):
    data = audit()
    patch = make_patch(source)
    rom = bytearray(source)
    title, suffix = data['entries'][45:47]
    offset = int(title['offset'], 16)
    raw = TextEncoder.encode_pokemon(title['portuguese'], strict=True)
    assert raw[1:] == TextEncoder.encode_pokemon(suffix['portuguese'], strict=True)
    rom[offset:offset + len(raw)] = raw
    patch.apply(rom)
    first = int.from_bytes(rom[title['references'][0]:title['references'][0] + 4], 'little')
    second = int.from_bytes(rom[suffix['references'][0]:suffix['references'][0] + 4], 'little')
    assert first + 1 != second
    final = bytes(rom)
    assert patch.apply(rom) == {'verified': 295, 'relocated': 0}
    assert bytes(rom) == final
