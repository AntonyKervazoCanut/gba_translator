"""PT-54 : manifeste fermé et noms internationaux, sans fuite du corpus FR."""
import json
from pathlib import Path

import yaml

from scripts.apply_combined_fr import _load_combined
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt54_audit.json').read_text())


def test_manifest_names_protections_and_budgets():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-54')
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    guards = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protected = {int(e['offset'], 16): e['expected'] for e in guards['entries']}
    glossary = yaml.safe_load((ROOT / 'languages/pt/data/official_terminology.yaml').read_text())
    assert glossary['categories']['species']['fallback'] == 'preserve_english'
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 300
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        name = row['portuguese']
        assert row['status'] == 'retained_english' and row['reason']
        assert texts[off] == protected[off] == name
        raw = TextEncoder.encode_pokemon(name, strict=True)
        assert len(raw) == row['encoded_bytes'] <= 11
        assert bytes.fromhex(row['source_hex']).startswith(raw)
        assert all(c < 0xF7 for c in raw[:-1])
        assert line_widths(name) == row['line_widths']
        assert max(row['line_widths']) <= 60
        assert off == 0x166A98C + row['species_id'] * 11


def test_names_and_forms_are_not_translated_from_french():
    rows = {r['offset']: r['portuguese'] for r in AUDIT['entries']}
    assert rows['0x166be21'] == 'Drifblim'
    assert rows['0x166beb0'] == 'Mime Jr.'
    assert rows['0x166c2ba'] == 'Gurdurr'
    assert rows['0x166c7e2'] == 'Warrior'
    assert rows['0x166caef'] == 'Flabébé'
    assert rows['0x166cafa'] == 'Floette'
    assert sum(name == 'Rotom' for name in rows.values()) == 6
    assert sum(name == 'Arceus' for name in rows.values()) == 17


def test_fixed_cell_finalizer_runs_after_generic_repairs():
    patches = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert patches.count('batch_54') == 1
    for step in ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'):
        assert patches.index(step) < patches.index('batch_54')
