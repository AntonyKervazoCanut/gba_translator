"""ES-005 : liste fermée et décisions lexicales du dictionnaire Easy Chat."""
import json
from pathlib import Path

from scripts.audit_translation_coverage import parse_combined
from src.core.text_codec import SPANISH_GLYPH_TABLE, TextEncoder

ROOT = Path(__file__).resolve().parents[2]


def test_exact_contract_and_decisions():
    lots = json.loads((ROOT / 'docs/analysis/es/lots.json').read_text())
    expected = next(lot['offsets'] for lot in lots if lot['id'] == 'ES-005')
    report = json.loads((ROOT / 'docs/analysis/es/005_TRAITEMENT.json').read_text())
    entries = report['entries']
    assert len(entries) == len({row['offset'] for row in entries}) == 374
    assert [row['offset'] for row in entries] == expected
    actual = parse_combined(ROOT / 'languages/es-maint/combined_es-maint.txt')
    for row in entries:
        offset = int(row['offset'], 16)
        assert actual[offset] == row['value']
        assert row['decision'] and row['zone'].startswith('Easy Chat / ')
        encoded = TextEncoder.encode_pokemon(row['value'], skip_aliases=frozenset(SPANISH_GLYPH_TABLE), strict=True)
        assert encoded.hex() == row['encoded_hex']
        assert not set(encoded[:-1]) & set(range(0xf7, 0x100))
        assert len(encoded) <= 13  # enveloppe du sélecteur : 12 glyphes + FF
        assert row['control_signature'] == [] and row['page_breaks'] == 0
        assert row['spanish_pointer_sites']
    assert {row['group'] for row in entries} == set(range(2, 10))


def test_lexical_senses_and_official_ability_names():
    report = json.loads((ROOT / 'docs/analysis/es/005_TRAITEMENT.json').read_text())
    entries = {int(row['offset'], 16): row for row in report['entries']}
    assert entries[0x3e8ac3]['value'] == 'TALENTO'  # nom commun, pas ability
    assert entries[0x3e8bed]['value'] == 'Movimiento'  # lexique combat, pas PC
    assert entries[0x3e92d2]['value'] == 'HIJA'  # daughter, pas filleule (FR)
    assert entries[0x3e9c22]['value'] == 'FALLAR'  # miss : rater, pas regretter
    assert entries[0x3e8a44]['value'] == 'GANA'  # wins : verbe, pas compteur
    assert entries[0x3e8a77]['value'] == 'NO SOY RIVAL'  # infériorité, pas invincibilité
    assert entries[0x3ea507]['value'] == 'MAREADO'  # giddy : étourdi
    assert entries[0x3e83db]['value'] == 'OJOCOMPUESTO'
    assert entries[0x3e83f5]['value'] == 'SUPERGUARDA'
    assert entries[0x3e8414]['value'] == 'MÁS'
    assert entries[0x3e8467]['value'] == 'MENOS'
    assert entries[0x3e8eef]['value'] == 'Sí'
    kept = {row['value'] for row in entries.values() if row['status'] == 'conservé justifié'}
    assert kept == {'NORMAL', 'RIVAL', 'LALALA', 'TERRIBLE'}
