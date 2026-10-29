"""PT-13 : livraison réelle, bornes, tables et tampons des menus système."""
from __future__ import annotations

import hashlib
import json
import re
import struct
from pathlib import Path

import pytest

from languages.pt.patches.batch_13 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import BUILDER, commands

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt13_audit.json').read_text())
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source() -> bytes:
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built() -> bytes:
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_all_live_consumers_deliver_exact_strings(source, built):
    patch = make_patch(source)
    assert len(patch.entries()) == 276
    patch.verify(built)
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for offset, refs, encoded in patch.entries():
        row = next(r for r in AUDIT['entries'] if int(r['offset'], 16) == offset)
        expected_refs = [m.start() for m in re.finditer(
            re.escape(struct.pack('<I', offset + 0x08000000)), source)]
        assert refs == expected_refs
        assert encoded == TextEncoder.encode_pokemon(
            row['portuguese'].replace(r'\n', '\n'), strict=True)
        assert commands(encoded) == commands(bytes.fromhex(row['source_hex']))
        for ref in refs:
            target = int.from_bytes(built[ref:ref + 4], 'little') - 0x08000000
            assert built[target:target + len(encoded)] == encoded


def test_exceptions_have_verified_owner_or_replacement(source):
    exceptions = [r for r in AUDIT['entries'] if r['status'] == 'exception']
    assert len(exceptions) == 5
    for row in exceptions:
        offset = int(row['offset'], 16)
        assert struct.pack('<I', offset + 0x08000000) not in source
        if 'owner_offset' in row:
            target = int(row['owner_offset'], 16)
            refs = [int(p, 16) for p in row['owner_sites']]
            raw = bytes.fromhex(row['owner_source_hex'])
        else:
            target = int(row['replacement_target'], 16)
            refs = [int(row['replacement_pointer'], 16)]
            raw = bytes.fromhex(row['replacement_source_hex'])
        assert refs and target != offset
        assert source[target:target + len(raw)] == raw
        for ref in refs:
            assert int.from_bytes(source[ref:ref + 4], 'little') == target + 0x08000000


def test_patch_is_atomic_idempotent_and_bounded(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 276
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 276, 'relocated': 0}
    assert bytes(rom) == after
    allowed = set()
    for _, refs, encoded in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(target, target + len(encoded)))
    changed = {i for i, (before, after) in enumerate(zip(source, rom)) if before != after}
    assert changed <= allowed
    patch.definitions[0] = dict(patch.definitions[0], source_hex='00ff')
    with pytest.raises(ValueError, match='préimage'):
        patch.apply(rom)
    assert bytes(rom) == after


def widths(raw: bytes, rom: bytes, table: int, buffers: dict | None = None) -> list[int]:
    """Mesure les vrais glyphes, positions FC13, icônes et tampons développés."""
    result, cursor, index = [], 0, 0
    while index < len(raw):
        code = raw[index]
        if code == 0xFF:
            break
        size = 1
        if code == 0xFE:
            result.append(cursor)
            cursor = 0
        elif code == 0xFC:
            size = 2 + BUILDER.FC_ARG_COUNTS.get(raw[index + 1], 0)
            if raw[index + 1] == 0x13:
                assert cursor <= raw[index + 2], ('colonne chevauchée', cursor, raw.hex())
                cursor = raw[index + 2]
        elif code in BUILDER.RAW_ARG_PREFIXES:
            size += BUILDER.RAW_ARG_PREFIXES[code]
            if code == 0xF8:
                cursor += 12
            elif code == 0xF9:
                cursor += 8
            else:
                replacement = (buffers or {}).get((code, raw[index + 1]), '')
                cursor += sum(rom[table + b] for b in TextEncoder.encode_pokemon(replacement)[:-1])
        else:
            cursor += rom[table + code]
        index += size
    return result + [cursor]


def test_literal_widths_and_fixed_columns_use_real_fonts(source, built):
    for offset, _, raw in make_patch(source).entries():
        # L'éditeur de mots utilise la largeur utile 224 ; les messages PC
        # sans retour sont une seule ligne dans leur fenêtre inférieure.
        limit = 224
        if 0x418208 <= offset <= 0x418452:
            limit = 192
        if 0x419B44 <= offset <= 0x419BDB:
            limit = 120
        for font in LATIN_FONTS:
            _, table = font.offsets(built)
            assert max(widths(raw, built, table)) <= limit, (hex(offset), font.glyph_pointer)


def test_summary_buffers_and_pc_dynamic_names_fit(source, built):
    entries = make_patch(source).entries()
    # Le moteur limite le nom saisi à 10 caractères ; le test utilise W,
    # le glyphe large. Le scénario de lieu long développe dix-huit W.
    for offset, _, raw in entries:
        if not (0x418208 <= offset <= 0x418452 or 0x419782 <= offset <= 0x4199F4):
            continue
        buffers = {(0xF7, 0): 'W' * 10, (0xF7, 1): '100', (0xF7, 2): 'W' * 18}
        for font in LATIN_FONTS:
            _, table = font.offsets(built)
            limit = 192 if offset < 0x419782 else 208
            assert max(widths(raw, built, table, buffers)) <= limit, (hex(offset), font.glyph_pointer)
