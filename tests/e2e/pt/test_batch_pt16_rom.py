"""PT-16 : consommateurs réels, budgets, idempotence et isolation binaire."""
import hashlib
import json
import re
import struct
from pathlib import Path

import pytest

from languages.pt.patches.batch_16 import make_patch
from languages.pt.patches.font import apply_patches
from src.core import pokedex
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt16_audit.json').read_text())
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_source_and_structured_consumers(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        # Le filtre heuristique iter_entries exclut les guillemets courbes
        # d'Electrode ; lire sa vraie structure ne dépend pas de ce filtre.
        site = pokedex.DEX_TABLE_BASE + row['dex_index'] * pokedex.DEX_TABLE_STRIDE
        assert struct.unpack_from('<I', source, site)[0] == offset + 0x08000000
        assert site in row['references']
        hits = [m.start() for m in re.finditer(re.escape(struct.pack('<I', offset + 0x08000000)), source)]
        assert hits == row['references']
    # La seconde référence Weezing est un consommateur de code, non une autre fiche.
    assert next(r['references'] for r in AUDIT['entries'] if r['offset'] == '0x447800') == [
        0x146B64, 0x1A36754]


def test_every_translation_reaches_built_rom(source, built):
    patch = make_patch(source)
    assert len(patch.entries()) == 282
    patch.verify(built)
    entries = {e.index: e for e in pokedex.iter_entries(built)}
    for row, (offset, refs, encoded) in zip(AUDIT['entries'], patch.entries()):
        assert offset == int(row['offset'], 16)
        assert encoded == TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        assert entries[row['dex_index']].text == row['portuguese'].replace(r'\n', '\n')
        for ref in refs:
            target = struct.unpack_from('<I', built, ref)[0] - 0x08000000
            assert built[target:target + len(encoded)] == encoded


def test_three_lines_and_actual_five_font_budgets(source, built):
    for _, _, raw in make_patch(source).entries():
        lines = raw[:-1].split(b'\xfe')
        assert len(lines) == pokedex.DEX_MAX_LINES == 3
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            assert all(sum(built[widths + c] for c in line) <= pokedex.DEX_LINE_WIDTH for line in lines)


def test_patch_idempotence_and_no_other_table_changes(source):
    patch = make_patch(source)
    rom = bytearray(source)
    apply_patches(rom)
    before = bytes(rom)
    assert patch.apply(rom)['verified'] == 282
    first = bytes(rom)
    assert patch.apply(rom) == {'verified': 282, 'relocated': 0}
    assert bytes(rom) == first
    allowed = set()
    for _, refs, encoded in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = struct.unpack_from('<I', rom, ref)[0] - 0x08000000
            allowed.update(range(target, target + len(encoded)))
    assert all(i in allowed for i, (a, b) in enumerate(zip(before, rom)) if a != b)
    changed_ids = {r['dex_index'] for r in AUDIT['entries']}
    after_entries = {e.index: e for e in pokedex.iter_entries(rom)}
    for entry in pokedex.iter_entries(source):
        if entry.index not in changed_ids:
            assert after_entries[entry.index] == entry
    broken = bytearray(source)
    broken[0x446E63] ^= 1
    with pytest.raises(ValueError, match='préimage'):
        make_patch(bytes(broken)).apply(rom)
    assert bytes(rom) == first
