"""PT-41 : couverture fermée, noms du glossaire et cellules fixes."""
import json
from pathlib import Path

import yaml

from scripts.apply_combined_fr import _load_combined
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt41_audit.json').read_text())


def test_manifest_names_protections_and_budgets():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-41')
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    guards = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protected = {int(e['offset'], 16): e['expected'] for e in guards['entries']}
    glossary = yaml.safe_load((ROOT / 'languages/pt/data/official_terminology.yaml').read_text())
    moves = glossary['categories']['moves']
    assert moves['fallback'] == 'preserve_english'
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 282
    assert '0xa42034' not in manifest  # cellule contiguë hors lot
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        expected = moves['entries'].get(row['english'], {}).get('value', row['english'])
        assert row['status'] == 'retained_english' and row['reason']
        assert texts[offset] == protected[offset] == row['portuguese'] == expected
        encoded = TextEncoder.encode_pokemon(expected, strict=True)
        assert len(encoded) == row['encoded_bytes'] <= 13
        assert bytes.fromhex(row['source_hex']).startswith(encoded)
        assert all(c < 0xF7 for c in encoded[:-1])
        assert line_widths(expected) == row['line_widths']
        assert max(row['line_widths']) <= 72
        assert offset == 0xA40A10 + row['move_id'] * 13


def test_unbound_names_are_kept_exactly_including_abbreviations():
    rows = {r['move_id']: r['portuguese'] for r in AUDIT['entries']}
    assert rows[419] == 'Struggle Bug'
    assert rows[521] == 'Metal Burst' and rows[499] == 'Metal Bash'
    assert rows[572] == '1000 Arrows'
    assert rows[678] == 'DMax Cannon'
    assert rows[701] == 'Branch Poke'


def test_shadow_force_keeps_space_instead_of_early_terminator():
    row = next(r for r in AUDIT['entries'] if r['offset'] == '0xa42340')
    assert row['move_id'] == 496
    assert row['portuguese'] == 'Shadow Force'
    cell = bytes.fromhex(row['source_hex'])
    # La passe générique écrivait FF à la place de cet espace ; le nom
    # devenait « Shadow ». La préimage livrée doit garder son unique fin.
    assert cell[6] == 0x00
    assert cell.index(0xFF) == 12
    assert cell == TextEncoder.encode_pokemon('Shadow Force', strict=True)
