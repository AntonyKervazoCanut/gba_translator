"""Contrat fermé ES-012 : couverture, budgets et consommateurs réels."""

import hashlib
import importlib
import json
from pathlib import Path

import pytest

from scripts.audit_translation_coverage import parse_combined
from src.core.dialogue_linewrap import line_width
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder
from src.core.text_converter import JSONToCSVConverter

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / 'docs/analysis/es/012_TRAITEMENT.json'


def test_es012_covers_the_exact_contract_and_prose_budgets():
    report = json.loads(REPORT.read_text())
    lot = next(lot for lot in json.loads(
        (ROOT / 'docs/analysis/es/lots.json').read_text()
    ) if lot['id'] == 'ES-012')
    combined = parse_combined(ROOT / 'languages/es-maint/combined_es-maint.txt')

    assert [entry['offset'] for entry in report['entries']] == lot['offsets']
    assert len(lot['offsets']) == len(set(lot['offsets'])) == 374
    assert report['counts'] == {
        'traduit': 353, 'importe': 8, 'conserve_copie_non_referencee': 4,
        'exclu_fragment': 7, 'exclu_binaire': 2,
    }
    for entry in report['entries']:
        offset = int(entry['offset'], 16)
        assert entry['justification']
        if 'texte' not in entry:
            assert offset not in combined
            continue
        text = entry['texte']
        assert combined[offset] == text.replace('\n', r'\n')
        raw = TextEncoder.encode_pokemon(text, skip_aliases=SPANISH_GLYPH_CHARS, strict=True)
        assert raw.hex() == entry['encoded_hex']
        assert len(raw) <= 512
        assert len(text.splitlines()) <= entry['max_lignes'] == 3
        assert max(map(line_width, text.splitlines())) <= entry['budget_px']
        assert not set(raw[:-1]) & {0xFC, 0xFD, 0xF8, 0xF9, 0xF7, 0xFA, 0xFB}
        assert not set(bytes.fromhex(entry['source_hex'])[:-1]) & {
            0xFC, 0xFD, 0xF8, 0xF9, 0xF7, 0xFA, 0xFB,
        }
        if entry['decision'] == 'importe':
            assert text == entry['correspondances_es'][0]['texte']


def test_es012_builder_preserves_every_reviewed_layout():
    module = importlib.import_module('src.translators.19_build_translated_rom_generic')
    builder = module.TranslatedROMBuilder(module.BuildConfig(
        source_rom=ROOT / 'input/roms/englishrom.gba',
        language='spanish', preserve_spanish_glyphs=True,
    ))
    converter = JSONToCSVConverter()
    report = json.loads(REPORT.read_text())

    for entry in report['entries']:
        if 'texte' not in entry:
            continue
        offset = int(entry['offset'], 16)
        normalized = builder._normalize_translation_item(offset, {
            'translation': entry['texte'],
            'english_text': entry['en_vivant'],
            'english_raw_bytes': entry['source_hex'],
            'category': converter.categorize_text(entry['en_vivant'], offset),
        })
        assert normalized['translation'] == entry['texte'], entry['offset']


@pytest.mark.rom
def test_es012_all_values_reach_their_final_consumers_and_exclusions_stay_intact():
    report = json.loads(REPORT.read_text())
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    final = (ROOT / 'output/roms/GenedRom-es-maint.gba').read_bytes()

    assert hashlib.sha256(source).hexdigest() == report['sources']['input/roms/englishrom.gba']
    for entry in report['entries']:
        offset = int(entry['offset'], 16)
        original = bytes.fromhex(entry['source_hex'])
        assert source[offset:offset + len(original)] == original
        if 'texte' not in entry:
            assert final[offset:offset + len(original)] == original, entry['offset']
            for neighbor in entry['references_voisines']:
                ref = int(neighbor['reference'], 16)
                assert final[ref:ref + 4] == source[ref:ref + 4]
                target = int.from_bytes(final[ref:ref + 4], 'little') - 0x08000000
                assert source[target] == final[target] == 0xFF
            continue
        for false_ref in entry['excluded_raw_matches']:
            ref = int(false_ref, 16)
            assert final[ref:ref + 4] == source[ref:ref + 4]
        expected = bytes.fromhex(entry['encoded_hex'])
        assert entry['references']
        for ref in entry['references']:
            ref = int(ref, 16)
            assert int.from_bytes(source[ref:ref + 4], 'little') == offset + 0x08000000
            target = int.from_bytes(final[ref:ref + 4], 'little') - 0x08000000
            assert 0 <= target < len(final)
            assert final[target:target + len(expected)] == expected, (entry['offset'], hex(ref), hex(target))
