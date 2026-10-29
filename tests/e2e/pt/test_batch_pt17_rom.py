"""PT-17 : preuves binaires sur source et ROM construite, sans adresses allouées figées."""
import hashlib
import json
import re
import struct
from pathlib import Path

import pytest

from languages.pt.patches.batch_17 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt17_audit.json').read_text())
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_all_live_targets_and_control_flow(source, built):
    patch = make_patch(source)
    assert len(patch.entries()) == 210
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
            assert not row['references']
            if row.get('replacement'):
                replacement = row['replacement']
                target = int(replacement['target'], 16)
                for ref in replacement['references']:
                    assert struct.unpack_from('<I', source, ref)[0] == target + 0x08000000


def test_idempotence_and_bounded_writes(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 210
    first = bytes(rom)
    assert patch.apply(rom) == {'verified': 210, 'relocated': 0}
    assert bytes(rom) == first
    allowed = set()
    for _, refs, encoded in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = struct.unpack_from('<I', rom, ref)[0] - 0x08000000
            allowed.update(range(target, target + len(encoded)))
    assert all(i in allowed for i, (a, b) in enumerate(zip(source, rom)) if a != b)
    corrupted = bytearray(source)
    corrupted[0x44DEC7] ^= 1
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
        for font in (LATIN_FONTS[2],):
            _, widths = font.offsets(built)
            for line in re.split(b'[\xfa\xfb\xfe\xff]', raw):
                limit = 112 if 0x454254 <= offset <= 0x4556CB else 224
                assert sum(built[widths + c] for c in line) <= limit, hex(offset)


def test_dynamic_names_and_levels_fit_the_dialogue_window(built):
    _, widths = LATIN_FONTS[2].offsets(built)
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            continue
        # Joueurs : sept glyphes ; espèces : douze ; niveaux : trois chiffres.
        text = re.sub(r'<0xFD><0x0[123]>', 'W' * 7, row['portuguese'])
        text = re.sub(r'<0xF7><0x0([0-3])>',
                      lambda m: '999' if int(m[1]) % 2 == 0 else 'W' * 12, text)
        raw = TextEncoder.encode_pokemon(text.replace(r'\n', '\n'), strict=True)
        for command in commands(raw):
            if command[0] not in (0xFA, 0xFB, 0xFE):
                raw = raw.replace(command, b'')
        for line in re.split(b'[\xfa\xfb\xfe\xff]', raw):
            assert sum(built[widths + c] for c in line) <= 224, row['offset']


def test_binary_coincidences_and_pointer_tables_are_not_text(source, built):
    # Ces deux faux pointeurs sont dans des données graphiques et non dans
    # les consommateurs de textes. La table de choix reste une table.
    for site in (0xCBA129, 0x1DCCF22, 0x11AE90):
        assert built[site:site + 4] == source[site:site + 4]
    assert struct.unpack_from('<I', built, 0x11AE90)[0] == 0x08458314
    assert struct.unpack_from('<I', source, 0x14C)[0] == 0x084556F8
