"""PT-56 : périmètre, politique des noms et exclusions graphiques explicites."""
import json
from pathlib import Path

import yaml

from scripts.apply_combined_fr import _load_combined
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt56_audit.json').read_text())


def test_exact_manifest_and_protections():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-56')
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    guards = {int(e['offset'], 16): e['expected'] for e in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 300
    names = [r for r in AUDIT['entries'] if r['status'] == 'retained_english']
    assert len(names) == 216
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['reason']
        if row['status'] == 'exception_binary':
            assert offset not in texts and offset not in guards
            assert row['owners'] and row['references'] == []
            continue
        assert texts[offset] == guards[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(texts[offset], strict=True)
        assert len(raw) == row['encoded_bytes'] <= 11
        assert bytes.fromhex(row['source_hex']).startswith(raw)
        assert all(c < 0xF7 for c in raw[:-1])
        assert max(row['font_widths']) <= 60
        assert offset == 0x166A98C + row['species_id'] * 11


def test_species_policy_and_existing_game_abbreviations():
    glossary = yaml.safe_load((ROOT / 'languages/pt/data/official_terminology.yaml').read_text())
    assert glossary['categories']['species']['fallback'] == 'preserve_english'
    names = {r['offset']: r['portuguese'] for r in AUDIT['entries'] if 'portuguese' in r}
    assert names['0x166d80a'] == 'Lycanroc'
    assert names['0x166d96a'] == 'Corvsquire'
    assert names['0x166d975'] == 'Corvknight'
    assert names['0x166daa9'] == 'Centskorch'
    assert names['0x166df6e'] == names['0x166df79'] == 'Basculegon'
    assert names['0x166db43'] == "Sirfetch'd"


def test_finalizer_runs_after_generic_passes():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_56') == 1
    assert all(steps.index(p) < steps.index('batch_56') for p in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))
