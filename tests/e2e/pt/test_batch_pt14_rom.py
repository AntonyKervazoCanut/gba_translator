"""PT-14 : preuves binaires sur source et ROM construite, sans adresses allouées figées."""
import hashlib
import json
import re
import struct
from pathlib import Path

import pytest

from languages.pt.patches.batch_14 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt14_audit.json').read_text())
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_all_live_targets_and_control_flow(source, built):
    patch = make_patch(source)
    assert len(patch.entries()) == 250
    patch.verify(built)
    for row, (offset, refs, encoded) in zip(
        [r for r in AUDIT['entries'] if r['status'] != 'exception'], patch.entries()
    ):
        assert row['offset'] == hex(offset)
        assert commands(encoded) == commands(bytes.fromhex(row['source_hex']))
        # Le finaliseur n'a ni réorganisé les tokens ni reformulé le texte.
        assert encoded == TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        for ref in refs:
            target = struct.unpack_from('<I', built, ref)[0] - 0x08000000
            assert built[target:target + len(encoded)] == encoded


def test_exception_pointers_and_preimages(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        hits = [m.start() for m in re.finditer(re.escape(struct.pack('<I', offset + 0x08000000)), source)]
        assert hits == [int(p, 16) for p in row['source_sites']]
        if row['status'] == 'exception':
            assert not hits
            replacement = row['replacement']
            target = int(replacement['target'], 16)
            raw = bytes.fromhex(replacement['source_hex'])
            assert source[target:target + len(raw)] == raw
            for ref in replacement['references']:
                assert struct.unpack_from('<I', source, ref)[0] == target + 0x08000000


def test_idempotence_and_bounded_writes(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 250
    first = bytes(rom)
    assert patch.apply(rom) == {'verified': 250, 'relocated': 0}
    assert bytes(rom) == first
    allowed = set()
    for _, refs, encoded in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = struct.unpack_from('<I', rom, ref)[0] - 0x08000000
            allowed.update(range(target, target + len(encoded)))
    assert all(i in allowed for i, (a, b) in enumerate(zip(source, rom)) if a != b)
    corrupted = bytearray(source)
    corrupted[0x41A1E7] ^= 1
    with pytest.raises(ValueError, match='préimage'):
        make_patch(bytes(corrupted)).apply(rom)
    assert bytes(rom) == first


def test_real_font_widths_and_scroll_boundaries(source, built):
    # Le normaliseur compte les lignes logiques incluant FA. Le budget écran
    # ci-dessous mesure séparément chaque ligne réellement affichée.
    for offset, _, raw in make_patch(source).entries():
        for command in commands(raw):
            if command[0] not in (0xFA, 0xFB, 0xFE):
                raw = raw.replace(command, b'')
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            for line in re.split(b'[\xfa\xfb\xfe\xff]', raw):
                assert sum(built[widths + c] for c in line) <= 224, hex(offset)


def test_journal_with_long_pokemon_names(source, built):
    # Les noms variables sont des Pokémon (10 glyphes), jamais un nom de lieu
    # arbitrairement tronqué. Contrôle les combinaisons à plusieurs buffers.
    for offset in (0x41A255, 0x41A277, 0x41AB74, 0x41AB8E, 0x41A4C6, 0x41B306, 0x41B32E):
        row = next(r for r in AUDIT['entries'] if int(r['offset'], 16) == offset)
        text = re.sub(r'<0xF[7D]><0x[0-9A-F]{2}>', 'W' * 10, row['portuguese'])
        raw = TextEncoder.encode_pokemon(text.replace(r'\n', '\n'), strict=True)
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            for line in re.split(b'[\xfa\xfb\xfe\xff]', raw):
                assert sum(built[widths + c] for c in line) <= 224, (hex(offset), text)


def test_levelup_column_budget_and_glossary_exceptions(source, built):
    # Fonction native 0x11e7f0 : labels x=0, police 2 ; signe x=56.
    # Les valeurs viennent de la table 0x459b48 à travers le littéral 0x11e930.
    assert source[0x11E89C:0x11E8A0] == bytes.fromhex('02210022')
    assert source[0x11E8CE:0x11E8D0] == bytes.fromhex('3822')
    assert struct.unpack_from('<I', built, 0x11E930)[0] == 0x08459B48
    _, widths = LATIN_FONTS[2].offsets(built)
    values = make_patch(source).texts
    for offset in (0x41B2B7, 0x41B2BE, 0x41B2C6, 0x41B2CC, 0x41B2D4):
        raw = TextEncoder.encode_pokemon(values[offset], strict=True)[:-1]
        assert sum(built[widths + c] for c in raw) < 56
    for name in ('Velocidade', 'Ataque Especial', 'Defesa Especial'):
        raw = TextEncoder.encode_pokemon(name, strict=True)[:-1]
        assert sum(built[widths + c] for c in raw) >= 56
    assert [values[o] for o in (0x41B2C6, 0x41B2CC, 0x41B2D4)] == [
        'Speed', 'Sp. Atk', 'Sp. Def']


def test_journal_item_move_and_location_buffers(source, built):
    values = make_patch(source).texts
    places = [values[int(r['offset'], 16)] for r in AUDIT['entries']
              if 0x41B09F <= int(r['offset'], 16) <= 0x41B277]
    nickname, player, item = 'W' * 10, 'W' * 7, 'W' * 18
    wild_places = {values[o] for o in (
        0x41B0CD, 0x41B0F6, 0x41B14B, 0x41B15A, 0x41B166,
        0x41B172, 0x41B1F4, 0x41B226, 0x41B236, 0x41B25B, 0x41B277,
    )}
    for place in places:
        scenarios = {
            0x41A1E7: [item, nickname],
            0x41A277: [nickname, item, item],
            0x41A965: [nickname, item, item],
            0x41A7DD: [place, item],
            0x41A810: [place, '999999', item],
            0x41A858: [player, place, '999999', item],
            0x41A896: [item, place, '999999'],
            0x41AF0C: [place, player, nickname, nickname, 'com tenacidade'],
        }
        # Un journal de capture sauvage ne combine pas un surnom avec le
        # musée de Pewter ou la maison du Name Rater : aucune rencontre là-bas.
        if place in wild_places:
            scenarios.update({
                0x41A9A9: [player, nickname, place],
                0x41A9D4: ['999', nickname, place],
                0x41AA01: [player, nickname, place],
                0x41AAAA: [nickname, '999', nickname, place],
                0x41AB29: ['999', nickname, '999', nickname, place],
            })
        for offset, buffers in scenarios.items():
            replacements = iter(buffers)
            text = re.sub(r'<0xF[7D]><0x[0-9A-F]{2}>', lambda _, it=replacements: next(it), values[offset])
            raw = TextEncoder.encode_pokemon(text.replace(r'\n', '\n'), strict=True)
            for font in LATIN_FONTS:
                _, widths = font.offsets(built)
                for line in raw[:-1].split(b'\xfe'):
                    assert sum(built[widths + c] for c in line) <= 224, (hex(offset), text)
