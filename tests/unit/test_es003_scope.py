"""Garde le périmètre contractuel et les cellules physiques du lot ES-003."""
import json
from pathlib import Path

from scripts.audit_translation_coverage import parse_combined
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder

ROOT = Path(__file__).resolve().parents[2]


def test_es003_prepared_entries_stay_inside_contract():
    lots = json.loads((ROOT / 'docs/analysis/es/lots.json').read_text())
    contract = {int(o, 16) for lot in lots if lot['id'] == 'ES-003' for o in lot['offsets']}
    entries = parse_combined(ROOT / 'languages/es-maint/combined_es-maint.txt')
    # La cible sera enrichie par les autres lots : seule cette tranche est inspectée.
    selected = {o: t for o, t in entries.items() if o in contract}
    assert len(contract) == 374
    assert selected
    for offset, text in selected.items():
        raw = TextEncoder.encode_pokemon(text.replace('\\n', '\n'), skip_aliases=SPANISH_GLYPH_CHARS)
        assert len(raw) < 512, hex(offset)
        if 0x23E558 <= offset < 0x23EAC7:
            assert (offset - 0x23E558) % 13 == 0
            assert len(raw) <= 13, (hex(offset), text, len(raw))


def test_es003_corrects_community_scenario_and_effects():
    entries = parse_combined(ROOT / 'languages/es-maint/combined_es-maint.txt')
    assert 'Autovía SES' in entries[0x26D524]
    assert '<0xFA>' in entries[0x26D524]
    assert '<0xFB>' in entries[0x26D524]
    assert 'supereficaz' in entries[0x24F607]
    assert 'mitad' in entries[0x3D5598]
    assert '<0xFD><0x0F>' in entries[0x277A12]


def test_final_report_accounts_for_every_offset_and_only_translated_keys():
    lots = json.loads((ROOT / 'docs/analysis/es/lots.json').read_text())
    contract = {int(o, 16) for lot in lots if lot['id'] == 'ES-003' for o in lot['offsets']}
    report = json.loads((ROOT / 'docs/analysis/es/003_TRAITEMENT.json').read_text())
    records = report['entries']
    offsets = [int(e['offset'], 16) for e in records]
    assert len(offsets) == len(set(offsets)) == 374
    assert set(offsets) == contract
    assert report['counts'] == {'traduit': 221, 'conserve_nom': 17,
                                'conserve_technique': 78, 'exclu_fragment': 8,
                                'exclu_binaire': 50}
    combined = parse_combined(ROOT / 'languages/es-maint/combined_es-maint.txt')
    assert contract & combined.keys() == {
        int(e['offset'], 16) for e in records if e['decision'] == 'traduit'
    }
    for record in records:
        assert record['justification']
        assert record['decision'] in report['counts']
        if record['decision'] == 'traduit':
            assert max(record['widths_px_with_ten_wide_glyph_buffers']) <= 192
            assert record['source_commands'] == record['final_commands']
