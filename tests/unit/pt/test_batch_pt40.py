"""PT-40 : contrat des noms conservés, sans traduire le corpus périmé."""
import json
from pathlib import Path

import yaml

from scripts.apply_combined_fr import _load_combined
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt40_audit.json').read_text())


def test_exact_manifest_and_fixed_cell_budgets():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-40')
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 283
    for row in AUDIT['entries']:
        assert int(row['offset'], 16) == 0xA40A10 + row['move_id'] * 13
        raw = bytes.fromhex(row['source_hex'])
        encoded = TextEncoder.encode_pokemon(row['expected'], strict=True)
        assert len(raw) == 13
        assert raw.startswith(encoded)
        assert len(encoded) == row['encoded_bytes'] <= 13
        assert not set(encoded[:-1]).intersection(range(0xF7, 0x100))
        assert line_widths(row['expected']) == row['line_widths']
        assert max(row['line_widths']) <= 80


def test_names_follow_glossary_and_no_conflicting_translation():
    glossary = yaml.safe_load((ROOT / 'languages/pt/data/official_terminology.yaml').read_text())
    moves = glossary['categories']['moves']
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    en, _ = _load_combined(ROOT / 'languages/en/combined_en.txt')
    fr, _ = _load_combined(ROOT / 'languages/fr/combined_fr.txt')
    assert moves['fallback'] == 'preserve_english'
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        name = row['expected']
        assert moves['entries'].get(name, {}).get('value', name) == name
        assert texts.get(offset, name) == name
        assert row['status'] == 'verified_retained'
        assert row['corpus_en'] == en.get(offset)
        assert row['comparison_fr'] == fr.get(offset)
        assert row['reason']
