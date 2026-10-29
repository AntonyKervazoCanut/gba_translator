"""PT-07 : contrôle de chaque mot et de sa cellule Easy Chat dans la vraie ROM."""
import json
import re
import struct
from pathlib import Path

import pytest

from src.core.fixed_tables import in_fixed_table
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def audit():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    offsets = {int(x, 16) for b in batches if b['id'] == 'PT-07' for x in b['offsets']}
    texts = {int(m[1], 16): m[2]
             for line in (ROOT / 'languages/pt/combined_pt.txt').read_text().splitlines()
             if (m := re.match(r'(0x[0-9a-f]+): (.*)', line))
             and int(m[1], 16) in offsets}
    assert len(texts) == len(offsets) == 281
    rows = []
    for offset, text in texts.items():
        pointer = struct.pack('<I', offset + 0x08000000)
        sites = [m.start() for m in re.finditer(re.escape(pointer), source)]
        # Chaque mot appartient à une cellule Easy Chat à pointeur + deux u32.
        assert len(sites) == 1, (hex(offset), sites)
        site = sites[0]
        assert 0x3E9000 < site < 0x3EAE00
        assert not in_fixed_table(offset)
        target = struct.unpack_from('<I', built, site)[0] - 0x08000000
        expected = TextEncoder.encode_pokemon(text, strict=True)
        assert 0 <= target <= len(built) - len(expected)
        rows.append((offset, site, target, expected))
    return source, built, rows


def test_all_281_words_are_exactly_injected_at_live_pointer_targets(audit):
    _, built, rows = audit
    for offset, _, target, expected in rows:
        assert built[target:target + len(expected)] == expected, (hex(offset), hex(target))


def test_index_and_availability_fields_of_every_easy_chat_cell_are_preserved(audit):
    source, built, rows = audit
    for offset, site, _, _ in rows:
        assert built[site + 4:site + 12] == source[site + 4:site + 12], hex(offset)


def test_real_font_widths_fit_the_original_english_word_envelope(audit):
    source, built, rows = audit
    # Le sélecteur emploie la police normale ; vérifier aussi toutes les polices
    # moteur pour les utilisateurs du lexique (courrier et phrases assemblées).
    for font in LATIN_FONTS:
        _, source_widths = font.offsets(source)
        _, built_widths = font.offsets(built)
        original_max = max(sum(source[source_widths + c]
                               for c in source[offset:source.index(b'\xff', offset)])
                           for offset, _, _, _ in rows)
        for offset, _, _, expected in rows:
            width = sum(built[built_widths + c] for c in expected[:-1])
            assert width <= original_max, (hex(offset), font.width_pointer, width, original_max)


def test_audit_matches_live_rom_and_has_no_unjustified_exception(audit):
    _, _, rows = audit
    report = json.loads((ROOT / 'languages/pt/data/pt07_audit.json').read_text())
    assert len(report['entries']) == 281
    recorded = {int(row['offset'], 16): row for row in report['entries']}
    assert set(recorded) == {offset for offset, _, _, _ in rows}
    for offset, site, target, expected in rows:
        row = recorded[offset]
        assert row['status'] == 'traduit/vérifié'
        assert int(row['pointer_site'], 16) == site
        # La cible du bilan est celle du build dont le SHA est enregistré.
        # Un autre lot peut déplacer l'allocation sans modifier cette traduction.
        assert int(row['live_target'], 16) > 0
        assert row['encoded_hex'] == expected.hex()


def test_group_descriptors_and_engine_references_still_reach_all_word_cells(audit):
    source, built, rows = audit
    root = 0x3ECED4
    groups = [struct.unpack_from('<IHH', source, root + index * 8)
              for index in range(4, 11)]
    assert built[root + 4 * 8:root + 11 * 8] == source[root + 4 * 8:root + 11 * 8]
    for site in (0xBD788, 0xBD7C0, 0xBD84C, 0xBDA38, 0xBDD2C, 0xBE270, 0xBE414):
        assert struct.unpack_from('<I', source, site)[0] == root + 0x08000000
        assert built[site:site + 4] == source[site:site + 4]
    for offset, site, _, _ in rows:
        matches = [(base - 0x08000000, count) for base, count, _ in groups
                   if 0 <= site - (base - 0x08000000) < count * 12
                   and (site - (base - 0x08000000)) % 12 == 0]
        assert len(matches) == 1, (hex(offset), hex(site))
        _, count = matches[0]
        order, available = struct.unpack_from('<II', source, site + 4)
        assert order < count and available == 1, (hex(offset), order, available)
