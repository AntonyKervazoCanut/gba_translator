"""Contrat fermé PT-53 : espèces, formes, budgets et protections exactes."""
import json
from pathlib import Path

import yaml

from scripts.apply_combined_fr import _load_combined
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextDecoder, TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt53_audit.json').read_text())


def test_manifest_glossary_protections_and_budgets():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-53')
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    guards = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protected = {int(e['offset'], 16): e['expected'] for e in guards['entries']}
    glossary = yaml.safe_load((ROOT / 'languages/pt/data/official_terminology.yaml').read_text())
    assert glossary['categories']['species']['fallback'] == 'preserve_english'
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(set(manifest)) == 300
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        english = TextDecoder.decode_pokemon(bytes.fromhex(row['source_hex']))
        expected = {'Egg': 'Ovo', 'Bad Egg': 'Ovo ruim'}.get(english, english)
        assert texts[offset] == protected[offset] == row['portuguese'] == expected
        assert TextDecoder.decode_pokemon(bytes.fromhex(row['final_hex'])) == expected
        encoded = TextEncoder.encode_pokemon(expected, strict=True)
        assert len(encoded) == row['encoded_bytes'] <= 11
        assert all(c < 0xF7 for c in encoded[:-1])
        assert line_widths(expected) == row['line_widths']
        assert max(row['line_widths']) <= 60
        assert offset == 0x166A98C + row['species_id'] * 11
        assert row['reason'] and row['pointer']


def test_species_forms_and_system_labels_are_not_french():
    rows = {r['offset']: r for r in AUDIT['entries']}
    assert rows['0x166b040']['portuguese'] == 'Quilava'
    assert rows['0x166b040']['english_corpus'] == 'Feurisson'
    assert rows['0x166b460']['portuguese'] == 'Ovo'
    assert rows['0x166bb40']['portuguese'] == 'Ovo ruim'
    assert rows['0x166bb4b']['portuguese'] == 'Unown B'
    assert rows['0x166bc5e']['portuguese'] == 'Unown !'
    assert rows['0x166be16']['portuguese'] == 'Drifloon'
