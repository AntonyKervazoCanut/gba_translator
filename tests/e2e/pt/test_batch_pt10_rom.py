"""PT-10 : commandes, cibles et exceptions contrôlées sur les vraies ROMs."""
from __future__ import annotations

import hashlib
import importlib
import json
import re
import struct
from pathlib import Path

import pytest

from languages.pt.patches.batch_10 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.structured_text import StructuredTextPatch

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt10_audit.json').read_text())
BUILDER = importlib.import_module('src.translators.19_build_translated_rom_generic').TranslatedROMBuilder
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source() -> bytes:
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built() -> bytes:
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_live_consumers_deliver_all_260_exact_strings(source, built):
    patch = make_patch(source)
    assert len(patch.entries()) == 260
    patch.verify(built)
    for offset, refs, encoded in patch.entries():
        row = next(row for row in AUDIT['entries'] if int(row['offset'], 16) == offset)
        expected_refs = [m.start() for m in re.finditer(
            re.escape(struct.pack('<I', offset + 0x08000000)), source)]
        assert refs == expected_refs
        original = bytes.fromhex(row['source_hex'])
        commands = BUILDER._extract_control_sequences_from_raw
        assert commands(encoded, include_breaks=True) == commands(original, include_breaks=True)
        for ref in refs:
            target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
            assert built[target:target + len(encoded)] == encoded


def test_exceptions_have_concrete_replacement_or_owner(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    assert len(AUDIT['entries']) == 282
    exceptions = [row for row in AUDIT['entries'] if row['status'] == 'exception']
    assert len(exceptions) == 22
    for row in exceptions:
        offset = int(row['offset'], 16)
        assert not row['references'] and not row['source_sites']
        assert struct.pack('<I', offset + 0x08000000) not in source
        if 'replacement' in row:
            replacement = row['replacement']
            ref, target = (int(replacement[key], 16) for key in ['pointer', 'target'])
            assert int.from_bytes(source[ref:ref + 4], 'little') == target + 0x08000000
            raw = bytes.fromhex(replacement['source_hex'])
            assert source[target:target + len(raw)] == raw
            assert target != offset
        else:
            owner = int(row['owner_offset'], 16)
            assert owner < offset
            assert row['owner_sites']
            for ref in row['owner_sites']:
                ref = int(ref, 16)
                assert int.from_bytes(source[ref:ref + 4], 'little') == owner + 0x08000000
            raw = bytes.fromhex(row['owner_source_hex'])
            assert source[owner:owner + len(raw)] == raw
        assert row['reason']


def test_patch_is_idempotent_and_only_changes_allocations_and_pointers(source):
    # Le test utilise la ROM réelle, pas une imitation des lecteurs binaires.
    patch = make_patch(source)
    rom = bytearray(source)
    stats = patch.apply(rom)
    assert stats['verified'] == 260
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 260, 'relocated': 0}
    assert bytes(rom) == after
    allowed = set()
    for _, refs, encoded in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(target, target + len(encoded)))
    changed = {index for index, (old, new) in enumerate(zip(source, rom)) if old != new}
    assert changed <= allowed
    # Une préimage divergente doit échouer sans aucune écriture partielle.
    corrupted = bytearray(source)
    corrupted[int(patch.definitions[0]['offset'], 16)] ^= 1
    invalid = StructuredTextPatch(bytes(corrupted), patch.definitions, ROOT / 'languages/pt/combined_pt.txt')
    with pytest.raises(ValueError, match='préimage'):
        invalid.apply(rom)
    assert bytes(rom) == after


def test_literal_widths_use_real_fonts_and_scroll_boundaries(source, built):
    # Les placeholders sont développés par les tests métier ; ici seuls les
    # glyphes littéraux sont mesurés, sans compter FC/FD et leurs arguments.
    for offset, _, encoded in make_patch(source).entries():
        lines = [[]]
        index = 0
        while index < len(encoded) - 1:
            byte = encoded[index]
            if byte in (0xFA, 0xFB, 0xFE):
                lines.append([])
            elif byte == 0xFC:
                index += 1 + BUILDER.FC_ARG_COUNTS.get(encoded[index + 1], 0)
            elif byte in BUILDER.RAW_ARG_PREFIXES:
                index += BUILDER.RAW_ARG_PREFIXES[byte]
            else:
                lines[-1].append(byte)
            index += 1
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            for line in lines:
                assert sum(built[widths + byte] for byte in line) <= 224, hex(offset)


def test_stat_buffers_fit_with_long_names_and_real_stat_labels(source, built):
    texts = make_patch(source).texts
    stats = [texts[o] for o in (0x3FD590, 0x3FD593, 0x3FD59A, 0x3FD5A2,
                               0x3FD5A8, 0x3FD5B0, 0x3FD5B8, 0x3FD5C1)]
    nickname = 'The opposing ' + 'W' * 10
    # Le buff extrême reste anglais car son offset est extérieur à PT-10.
    # Il est compté aussi dans la variante objet, avec les noms extrêmes.
    for offset in (0x3FCB5F, 0x3FCB6A, 0x3FCB8F, 0x3FCB9A, 0x3FCB75):
        modifiers = ('!', 'muito!', 'drastically !')
        for stat in stats:
            for modifier in modifiers:
                text = texts[offset]
                for token, replacement in {
                    '<0xFD><0x0F>': nickname, '<0xFD><0x10>': nickname,
                    '<0xFD><0x13>': nickname, '<0xFD><0x16>': 'Liechi Berry',
                    '<0xFD><0x00>': stat, '<0xFD><0x01>': modifier,
                }.items():
                    text = text.replace(token, replacement)
                from src.core.text_codec import TextEncoder
                raw = TextEncoder.encode_pokemon(text.replace(r'\n', '\n'), strict=True)
                for font in LATIN_FONTS:
                    _, widths = font.offsets(built)
                    for line in raw[:-1].split(b'\xfe'):
                        assert sum(built[widths + byte] for byte in line) <= 224, (
                            hex(offset), stat, modifier, text)
