"""Le brouillon ES-016 ne peut perdre une clé, une commande ou devenir une preuve finale."""
import json
from pathlib import Path

from scripts.audit_es016_preparation import snapshot
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / 'docs/analysis/es/016_REPRISE.json'


def test_review_covers_the_exact_frozen_selection_without_certifying_injection():
    report = json.loads(REPORT.read_text())
    lots = json.loads((ROOT / 'docs/analysis/es/lots.json').read_text())
    expected = next(lot['offsets'] for lot in lots if lot['id'] == 'ES-016')

    assert [entry['offset'] for entry in report['entries']] == expected
    assert len(set(expected)) == 393
    assert all(entry['injection_certified'] is False for entry in report['entries'])
    assert report['summary'] == {
        'brouillon_non_injecté': 340,
        'conservé_sans_injection': 32,
        'qualification_à_terminer': 21,
    }


def test_every_draft_preserves_full_commands_arguments_and_pagination():
    report = json.loads(REPORT.read_text())
    preparation = json.loads((ROOT / 'docs/analysis/es/016_PREPARATION.json').read_text())
    sources = {entry['offset']: entry['english_snapshot'] for entry in preparation['entries']}

    for entry in report['entries']:
        assert entry['source_raw_hex'] == sources[entry['offset']]['raw_hex']
        if entry['decision'] != 'brouillon_non_injecté':
            assert 'translation' not in entry
            continue
        encoded = TextEncoder.encode_pokemon(
            entry['translation'].replace('\\n', '\n'),
            strict=True, skip_aliases=SPANISH_GLYPH_CHARS,
        )
        actual = [c['hex'] for c in snapshot(encoded, 0)['commands'] if c['hex'] != 'fe']
        expected = [c['hex'] for c in sources[entry['offset']]['commands'] if c['hex'] != 'fe']

        assert actual == expected, entry['offset']
        assert len(encoded) == entry['encoded_bytes_including_ff'] <= 512
        assert entry['qualified_pointers'], entry['offset']


def test_old_table_and_unresolved_fragments_are_never_presented_as_live_translations():
    report = json.loads(REPORT.read_text())
    entries = {entry['offset']: entry for entry in report['entries']}

    assert entries['0x00780E33']['decision'] == 'conservé_sans_injection'
    assert entries['0x00780E33']['active_table_matches'] == []
    for key in ('0x00780CB2', '0x0078117E', '0x0078122B', '0x0078D67B', '0x0078D78D'):
        assert entries[key]['decision'] == 'qualification_à_terminer'
        assert 'translation' not in entries[key]
    assert entries['0x0078000F']['containing_reconstructed_sources'][0]['offset'] == '0x77ffe5'
    assert entries['0x00780119']['containing_reconstructed_sources'][0]['offset'] == '0x7800bd'
