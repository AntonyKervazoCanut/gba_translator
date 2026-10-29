"""PT-31 : noms d’objets conservés et faux textes après terminateur."""
import json
from pathlib import Path

import yaml

from scripts.apply_combined_fr import _load_combined
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt31_audit.json').read_text())


def test_closed_manifest_and_exact_protections():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-31')
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    guards = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protected = {int(e['offset'], 16): e['expected'] for e in guards['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 288
    exceptions = []
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['reason']
        if row['status'] == 'exception':
            exceptions.append(offset)
            assert offset not in texts and not row['references']
        else:
            assert texts[offset] == protected[offset] == row['english'] == row['portuguese']
            assert offset == 0x876200 + row['item_id'] * 44
    assert exceptions == [0x879E88, 0x87A0EC]


def test_glossary_and_fixed_cell_budgets():
    glossary = yaml.safe_load((ROOT / 'languages/pt/data/official_terminology.yaml').read_text())
    # Le schéma est testé indépendamment ; retrouver la catégorie sans supposer sa racine.
    categories = glossary.get('categories', glossary.get('terminology', glossary))
    assert categories['items']['fallback'] == 'preserve_english'
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            continue
        raw = TextEncoder.encode_pokemon(row['portuguese'], strict=True)
        assert raw.hex() == row['source_hex']
        assert len(raw) == row['encoded_bytes'] <= 13
        assert not set(raw[:-1]).intersection(range(0xF7, 0x100))
        assert line_widths(row['portuguese']) == row['line_widths']
        assert max(row['line_widths']) <= 78
