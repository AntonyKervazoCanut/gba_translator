"""Acheminement borné des sept textes B-1016, depuis des extraits ROM réels."""
import json
import struct
from pathlib import Path

import pytest

from languages.de.patches import dialogue_routing as patch

ROOT = Path(__file__).resolve().parents[3]
ROWS = json.loads((ROOT / 'tests/unit/fixtures/de_dialogue_routing_1016.json').read_text())


def fixture_rom():
    source = bytearray(b'\x00' * 0x2000000)
    source[0xB00000:0xB10000] = b'\xff' * 0x10000
    for row in ROWS:
        raw = bytes.fromhex(row['raw'])
        source[row['offset']:row['offset'] + len(raw)] = raw
        for site in row['sites']:
            source[site-2:site+6] = bytes.fromhex(row['preimages'][str(site)])
    return source


def valid_combined():
    combined = patch.load_combined(ROOT / 'languages/de/combined_de.txt')
    # Donnée de test seulement : B-680 doit restituer ces deux buffers dans
    # le texte vivant avant activation de la passe dans lang.yaml.
    combined[0x1F4C2ED] = r'<0xFD><0x01> Glückwunsch!\p<0xFD><0x02>\n<0xFD><0x02>'
    return combined


def test_all_consumers_exact_bytes_idempotence_and_no_blind_scan():
    source = fixture_rom()
    rom = bytearray(source)
    combined = valid_combined()
    # Un pointeur non déclaré ne doit jamais être scanné/modifié.
    struct.pack_into('<I', rom, 0x100, 0x087A9A75)
    before = bytes(rom)
    report = patch.apply(rom, combined, source)
    assert len(report) == 7
    for row in ROWS:
        encoded = patch.encode_dialogue(combined[row['offset']], source, row['offset'])
        for site in row['sites']:
            target = struct.unpack_from('<I', rom, site)[0] - patch.GBA_BASE
            assert rom[target:target+len(encoded)] == encoded
            assert rom[site-2:site] == before[site-2:site]
            assert rom[site+4:site+6] == before[site+4:site+6]
    assert rom[0x100:0x104] == before[0x100:0x104]
    assert rom[0x1E67DB8:0x1E67DBC] == before[0x1E67DB8:0x1E67DBC]
    after = bytes(rom)
    patch.apply(rom, combined, source)
    assert rom == after


def test_cube_reuses_already_correct_copy():
    source = fixture_rom()
    rom = bytearray(source)
    combined = valid_combined()
    encoded = patch.encode_dialogue(combined[0x1FB07FE], source, 0x1FB07FE)
    rom[0x1100000:0x1100000+len(encoded)] = encoded
    struct.pack_into('<I', rom, 0x1EAF820, 0x09100000)
    patch.apply(rom, combined, source)
    assert struct.unpack_from('<I', rom, 0x1285745)[0] == 0x09100000
    assert struct.unpack_from('<I', rom, 0x1EAF820)[0] == 0x09100000


def test_invalid_source_pointer_fails_without_mutation():
    source = fixture_rom()
    source[0x74B0AA] = 0
    rom = bytearray(source)
    before = bytes(rom)
    with pytest.raises(ValueError, match='source'):
        patch.apply(rom, patch.load_combined(ROOT / 'languages/de/combined_de.txt'), source)
    assert rom == before


def test_missing_source_commands_refused_atomically():
    source = fixture_rom()
    rom = bytearray(source)
    combined = valid_combined()
    combined[0x1F4C2ED] = 'Hallo.'
    before = bytes(rom)
    with pytest.raises(ValueError, match='commandes différentes'):
        patch.apply(rom, combined, source)
    assert rom == before


@pytest.mark.parametrize('row', ROWS, ids=lambda row: hex(row['offset']))
def test_commands_pages_and_box_budget(row):
    from scripts.apply_inline_overrides_fr import (
        _extract_control_sequences_from_raw,
        _normalize_text,
    )
    from src.core.dialogue_linewrap import line_widths
    source = fixture_rom()
    text = valid_combined()[row['offset']]
    prepared = patch.prepared_text(text, source, row['offset'])
    encoded = patch.encode_dialogue(text, source, row['offset'])
    expected = [x for x in _extract_control_sequences_from_raw(bytes.fromhex(row['raw']))
                if x[0] not in (0xFA, 0xFB)]
    actual = [x for x in _extract_control_sequences_from_raw(encoded)
              if x[0] not in (0xFA, 0xFB)]
    assert actual == expected
    assert encoded[-1] == 0xFF
    assert max(line_widths(prepared)) <= 192
    assert prepared.count('<0xFB>') == _normalize_text(text).count('<0xFB>')
    for page in prepared.split('<0xFB>'):
        assert page.count('\n') <= 1


def test_allocation_failure_does_not_partially_repoint():
    source = fixture_rom()
    rom = bytearray(source)
    rom[0xB00000:0xB10000] = b'\x00' * 0x10000
    before = bytes(rom)
    with pytest.raises(ValueError, match='espace libre insuffisant'):
        patch.apply(rom, valid_combined(), source)
    assert rom == before


def test_german_umlauts_keep_their_actual_glyph_bytes():
    source = fixture_rom()
    # 0x1F0F004 ne contient aucune commande positionnelle dans la source.
    encoded = patch.encode_dialogue('äöüÄÖÜ', source, 0x1F0F004)
    assert encoded == bytes([0xF4, 0xF5, 0xF6, 0xF1, 0xF2, 0xF3, 0xFF])
