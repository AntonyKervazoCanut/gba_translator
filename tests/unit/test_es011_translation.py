"""ES-011 : sélection fermée, commandes complètes et octets aux lecteurs finaux."""
import importlib
import json
from pathlib import Path

import pytest

from scripts.audit_translation_coverage import parse_combined
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / 'docs/analysis/es/011_TRAITEMENT.json'
Builder = importlib.import_module('src.translators.19_build_translated_rom_generic').TranslatedROMBuilder


def test_es011_exact_selection_values_commands_and_budgets():
    report = json.loads(REPORT.read_text())
    lot = next(row for row in json.loads((ROOT / 'docs/analysis/es/lots.json').read_text()) if row['id'] == 'ES-011')
    combined = parse_combined(ROOT / 'languages/es-maint/combined_es-maint.txt')

    assert [row['offset'] for row in report['entries']] == lot['offsets']
    assert len(set(lot['offsets'])) == 374
    assert report['counts'] == {'traduit': 297, 'conserve_nom': 5, 'conserve_sans_lecteur_identifie': 4,
                                'doublon_canonique': 4, 'conserve_credits_historiques': 60, 'exclu_binaire': 4}
    for row in report['entries']:
        key = int(row['offset'], 16)
        assert row['justification']
        if 'texte' not in row:
            assert key not in combined
            continue
        assert combined[key] == row['texte'].replace('\n', r'\n')
        encoded = TextEncoder.encode_pokemon(row['texte'], skip_aliases=SPANISH_GLYPH_CHARS, strict=True)
        assert encoded.hex() == row['encoded_hex']
        assert len(encoded) <= 512
        source = bytes.fromhex(row['source_hex'])
        assert Builder._extract_control_sequences_from_raw(encoded) == Builder._extract_control_sequences_from_raw(source)
        layout = {'allow_pagination': True, **(row.get('layout') or {})}
        widths = Builder._encoded_layout_widths(encoded, layout)
        assert widths == row['largeurs_px']
        assert max(widths) <= row['budget_px']
        if row['surface'] == 'Pokédex':
            assert len(row['texte'].splitlines()) <= 3
            assert not Builder._extract_control_sequences_from_raw(encoded)


@pytest.mark.rom
def test_es011_final_rom_all_readers_exclusions_and_prefixes():
    report = json.loads(REPORT.read_text())
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    actual = (ROOT / 'output/roms/GenedRom-es-maint.gba').read_bytes()

    for row in report['entries']:
        key = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[key:key + len(raw)] == raw
        if 'texte' not in row:
            if row['decision'] == 'doublon_canonique':
                continue  # Testé via sa clé contractuelle, relocation ou insertion en place.
            assert actual[key:key + len(raw)] == raw, row['offset']
            for reference in row['references']:
                ref = int(reference, 16)
                assert actual[ref:ref + 4] == source[ref:ref + 4]
            continue
        live = int(row['live_offset'], 16)
        assert actual[key:live] == source[key:live]
        expected = bytes.fromhex(row['encoded_hex'])
        assert row['references']
        for reference in row['references']:
            ref = int(reference, 16)
            assert int.from_bytes(source[ref:ref + 4], 'little') == live + 0x08000000
            target = int.from_bytes(actual[ref:ref + 4], 'little') - 0x08000000
            assert 0 <= target < len(actual)
            assert actual[target:target + len(expected)] == expected, (row['offset'], reference, hex(target))
