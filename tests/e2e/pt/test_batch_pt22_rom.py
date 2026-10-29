"""PT-22 : livraison réelle aux pointeurs vivants, commandes et budgets GBA."""
from __future__ import annotations

import hashlib
import json
import re
import struct
from pathlib import Path

import pytest

from languages.pt.patches.batch_22 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands

ROOT = Path(__file__).resolve().parents[3]
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


@pytest.fixture(scope='module')
def audit():
    return json.loads((ROOT / 'languages/pt/data/pt22_audit.json').read_text())


def test_all_live_consumers_deliver_exact_translations(source, built, audit):
    patch = make_patch(source)
    patch.verify(built)
    rows = [row for row in audit['entries'] if row['status'] == 'translated']
    entries = patch.entries()
    assert len(entries) == len(rows) == 240
    for row, (offset, refs, raw) in zip(rows, entries):
        assert int(row['offset'], 16) == offset
        assert refs == row['references']
        expected = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        assert raw == expected
        assert commands(raw) == commands(bytes.fromhex(row['source_hex']))
        for site in refs:
            target = struct.unpack_from('<I', built, site)[0] - 0x08000000
            assert built[target:target + len(raw)] == expected, (row['offset'], hex(site))


def test_source_preimages_all_pointer_occurrences_and_exceptions(source, audit):
    assert hashlib.sha256(source).hexdigest() == audit['source_sha256']
    for row in audit['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        sites = [match.start() for match in re.finditer(
            re.escape(struct.pack('<I', offset + 0x08000000)), source)]
        assert [hex(site) for site in sites] == row['source_sites']
        if row['status'] == 'exception':
            assert row['reason'] and not row['references']


def test_historical_move_table_is_not_a_live_description_consumer(source, built, audit):
    # La table réellement lue est à +4 du repère historique moves.py.
    roots = (0xE5440, 0x137BC8, 0x9F3B64)
    assert all(struct.unpack_from('<I', source, site)[0] == 0x0899F194 for site in roots)
    assert all(built[site:site + 4] == source[site:site + 4] for site in roots)
    live_targets = {struct.unpack_from('<I', source, 0x99F194 + n * 4)[0] - 0x08000000
                    for n in range(894)}
    legacy = [row for row in audit['entries'] if 0x780A50 <= int(row['offset'], 16) <= 0x78122B]
    assert len(legacy) == 26
    assert all(row['status'] == 'exception' for row in legacy)
    assert not {int(row['offset'], 16) for row in legacy} & live_targets
    assert not list(re.finditer(re.escape(struct.pack('<I', 0x08904000)), source))
    # Le lot ne doit pas requalifier une table morte en preuve de livraison.
    for row in legacy:
        for value in row['source_sites']:
            site = int(value, 16)
            assert built[site:site + 4] == source[site:site + 4], hex(site)


def test_objects_use_the_actual_item_table_and_preserve_metadata(source, built, audit):
    base = struct.unpack_from('<I', source, 0x9A8D8)[0] - 0x08000000
    assert base == 0x876200
    rows = {int(row['offset'], 16): row for row in audit['entries']}
    for offset, site in ((0x7812CF, 0x877420), (0x78133B, 0x8771B8), (0x78137A, 0x877580)):
        assert (site - base - 20) % 44 == 0
        assert rows[offset]['references'] == [site]
        assert struct.unpack_from('<I', source, site)[0] == offset + 0x08000000
        # Le nom, prix, usage et paramètres voisins de l'objet restent intacts.
        assert built[site - 20:site] == source[site - 20:site]
        assert built[site + 4:site + 24] == source[site + 4:site + 24]


def test_applymovement_and_accidental_code_pointers_are_unchanged(source, built, audit):
    assert source[0x778EAF:0x778EB1] == built[0x778EAF:0x778EB1] == b'\x04\xfe'
    rows = {int(row['offset'], 16): row for row in audit['entries']}
    for offset in (0x778EAF, 0x78000F, 0x780119):
        for value in rows[offset]['source_sites']:
            site = int(value, 16)
            assert built[site:site + 4] == source[site:site + 4], hex(site)
    for value in rows[0x778EAF]['source_sites']:
        site = int(value, 16)
        assert source[site - 3] == 0x4F


def test_real_font_widths_and_worst_case_name_buffers(source, built, audit):
    _, widths = LATIN_FONTS[2].offsets(built)
    item_offsets = {0x7812CF, 0x78133B, 0x78137A}
    for row in audit['entries']:
        if row['status'] != 'translated':
            continue
        offset = int(row['offset'], 16)
        text = row['portuguese']
        # FD01 = nom joueur et FD06 = nom rival : sept glyphes chacun.
        text = re.sub(r'<0xFD><0x0[16]>', 'W' * 7, text)
        # Les autres tampons dépendent du script : Pokémon, titre, lien familial,
        # pronom ou liste d'ingrédients. Leur place doit rester libre après PT-22.
        index = row['index']
        bounds = {}
        if index in (8, 238, 239):
            bounds = {2: 3, 3: 3, 4: 3}
        elif index in (15, 17, 118):
            bounds = {2: 12}
        elif index in (84, 89):
            bounds = {2: 5}
        elif index in (163, 167):
            bounds = {2: 7}
        elif index == 20:
            bounds = {4: 3}
        elif index in (261, 262, 263, 264, 265, 266, 274, 276):
            bounds = {2: 24}
        elif index == 277:
            bounds = {3: 9}
        for number, length in bounds.items():
            text = text.replace(f'<0xFD><0x{number:02X}>', 'W' * length)
        raw = TextEncoder.encode_pokemon(text.replace(r'\n', '\n'), strict=True)
        for command in commands(raw):
            if command[0] not in (0xFA, 0xFB, 0xFE):
                raw = raw.replace(command, b'')
        budget = row.get('physical_max_width', 186 if offset in item_offsets else 224)
        for line in re.split(b'[\xfa\xfb\xfe\xff]', raw):
            assert sum(built[widths + code] for code in line) <= budget, row['offset']


def test_patch_is_idempotent_atomic_and_has_bounded_writes(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 240
    first = bytes(rom)
    assert patch.apply(rom) == {'verified': 240, 'relocated': 0}
    assert bytes(rom) == first
    allowed = set()
    for _, refs, raw in patch.entries():
        for site in refs:
            allowed.update(range(site, site + 4))
            target = struct.unpack_from('<I', rom, site)[0] - 0x08000000
            allowed.update(range(target, target + len(raw)))
    assert all(index in allowed for index, (old, new) in enumerate(zip(source, rom)) if old != new)
    corrupted = bytearray(source)
    corrupted[0x773613] ^= 1
    with pytest.raises(ValueError, match='préimage'):
        make_patch(bytes(corrupted)).apply(rom)
    assert bytes(rom) == first
