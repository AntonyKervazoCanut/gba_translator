"""B-1013 : régression des 67 chaînes exclues, depuis les sources canoniques."""
import importlib
import json

import pytest

from tests.unit.de.test_combat_ui_03 import ROOT, ROWS, commands, encoded

BUILDER = importlib.import_module('src.translators.19_build_translated_rom_generic').TranslatedROMBuilder
TARGETS = [row for row in ROWS if row.get('proposed_after')]


@pytest.mark.parametrize('row', TARGETS, ids=lambda row: row['offset'])
def test_structured_normalization_keeps_commands_and_layout(row):
    builder = BUILDER.__new__(BUILDER)
    builder.english_texts = None
    text = row['proposed_after'].replace(r'\n', '\n').replace(r'\p', '<0xFB>')
    normalized = builder._normalize_translation_item(int(row['offset'], 16), {
        'translation': text, 'english_raw_bytes': row['hex'],
        'english_text': row['rom'], 'category': 'dialogue',
        'layout': {'max_lines': 5 if row['move_ids'] else 2,
                   'max_width': 122 if row['move_ids'] else 192},
    })
    assert normalized['translation'] == text
    assert commands(encoded(text)) == commands(bytes.fromhex(row['hex']))


def test_invalid_layout_fails_instead_of_silently_rewrapping():
    builder = BUILDER.__new__(BUILDER)
    builder.english_texts = None
    with pytest.raises(ValueError):
        builder._normalize_translation_item(0, {
            'translation': 'A' * 100 + '\nB', 'english_raw_bytes': encoded('A\nB').hex(),
            'layout': {'max_lines': 2, 'max_width': 192},
        })


def test_manifest_matches_only_the_67_deferred_entries():
    rows = json.loads((ROOT / 'languages/de/data/combat_ui_03_structure.json').read_text())
    assert {row['offset'] for row in rows} == {row['offset'] for row in TARGETS}
    assert len(rows) == 67


@pytest.mark.parametrize('translation', ['AB', 'A<0xFA>B', 'A\nB\nC'])
def test_declared_structure_rejects_missing_or_changed_breaks(translation):
    builder = BUILDER.__new__(BUILDER)
    builder.english_texts = None
    with pytest.raises(ValueError, match='commandes ou ruptures'):
        builder._normalize_translation_item(0, {
            'translation': translation, 'english_raw_bytes': encoded('A\nB').hex(),
            'layout': {'max_lines': 2, 'max_width': 192},
        })


@pytest.mark.rom
def test_all_live_targets_match_after_build():
    from src.core.structured_text import StructuredTextPatch
    patch = StructuredTextPatch(
        (ROOT / 'input/roms/englishrom.gba').read_bytes(),
        json.loads((ROOT / 'languages/de/data/combat_ui_03_structure.json').read_text()),
        ROOT / 'languages/de/combined_de.txt',
    )
    rom = (ROOT / 'output/roms/GenedRom-de.gba').read_bytes()
    patch.verify(rom)
    assert len(patch.entries()) == 67


@pytest.mark.rom
def test_atomic_patch_idempotence_and_canonical_source_guards(tmp_path):
    from src.core.structured_text import StructuredTextPatch
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    definitions = json.loads((ROOT / 'languages/de/data/combat_ui_03_structure.json').read_text())
    patch = StructuredTextPatch(source, definitions, ROOT / 'languages/de/combined_de.txt')
    rom = bytearray(source)
    before = bytes(rom)
    assert patch.apply(rom)['verified'] == 67
    after = bytes(rom)
    assert patch.apply(rom)['relocated'] == 0
    assert bytes(rom) == after
    for offset, _, _ in patch.entries():
        raw = bytes.fromhex(next(d['source_hex'] for d in definitions if int(d['offset'], 16) == offset))
        assert rom[offset:offset + len(raw)] == before[offset:offset + len(raw)]
    # Refus atomique d'une ROM sans place, puis d'une préimage changée.
    full = bytearray(b'\x00') * len(source)
    for _, refs, _ in patch.entries():
        for ref in refs:
            full[ref:ref + 4] = source[ref:ref + 4]
    snapshot = bytes(full)
    with pytest.raises(ValueError, match='espace libre'):
        patch.apply(full)
    assert bytes(full) == snapshot
    bad_source = bytearray(source)
    bad_source[int(definitions[0]['offset'], 16)] ^= 1
    bad = StructuredTextPatch(bytes(bad_source), definitions, ROOT / 'languages/de/combined_de.txt')
    with pytest.raises(ValueError, match='préimage'):
        bad.apply(rom)
    assert bytes(rom) == after
