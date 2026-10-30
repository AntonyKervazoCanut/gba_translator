"""PT-55 : noms canoniques, manifeste fermé et budgets des cellules fixes."""
import json
from pathlib import Path

import yaml

from scripts.apply_combined_fr import _load_combined
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt55_audit.json').read_text())


def test_manifest_names_protections_and_budgets():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-55')
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    guards = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protected = {int(e['offset'], 16): e['expected'] for e in guards['entries']}
    glossary = yaml.safe_load((ROOT / 'languages/pt/data/official_terminology.yaml').read_text())
    assert glossary['categories']['species']['fallback'] == 'preserve_english'
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 299
    assert AUDIT['table_base'] == '0x166a98c' and len(AUDIT['table_references']) == 42
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        assert row['status'] == 'retained_english' and row['reason']
        assert texts[off] == protected[off] == row['portuguese'] == row['english']
        encoded = TextEncoder.encode_pokemon(texts[off], strict=True)
        assert len(encoded) == row['encoded_bytes'] <= 11
        assert bytes.fromhex(row['source_hex']).startswith(encoded)
        assert not any(c >= 0xF7 for c in encoded[:-1])
        assert line_widths(texts[off]) == row['line_widths']
        assert max(row['line_widths']) <= 60
        assert off == 0x166A98C + row['species_id'] * 11


def test_form_names_and_contaminated_reference_are_not_translated_from_french():
    rows = {r['offset']: r for r in AUDIT['entries']}
    assert rows['0x166cb10']['english_reference'] == 'Cabriolain'
    assert rows['0x166cb10']['portuguese'] == 'Skiddo'
    assert rows['0x166d40b']['portuguese'] == 'Type: Null'
    assert rows['0x166d49a']['portuguese'] == 'Tapu Koko'
    assert rows['0x166d7d3']['portuguese'] == 'Blacphalon'


def test_finalizer_after_repairs():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_55') == 1
    assert all(steps.index(s) < steps.index('batch_55') for s in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))
