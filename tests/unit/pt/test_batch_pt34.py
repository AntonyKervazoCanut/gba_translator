"""PT-34 : couverture fermée des exceptions, sans fausse traduction livrée."""
import json
from collections import Counter
from pathlib import Path

from scripts.apply_combined_fr import _load_combined

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt34_audit.json').read_text())


def test_exact_manifest_and_documented_exceptions():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    manifest = next(b['offsets'] for b in batches if b['id'] == 'PT-34')
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    rows = AUDIT['entries']
    assert [r['offset'] for r in rows] == manifest
    assert len(rows) == 288
    assert Counter(r['kind'] for r in rows) == {
        'obsolete_move': 133, 'padding_prefix': 101, 'unreferenced_ability': 54,
    }
    for row in rows:
        assert row['status'] == 'exception'
        assert row['reason'] and row['english_reference'] and row['french_reference']
        assert int(row['offset'], 16) not in texts
        assert row['source_hex'].endswith('ff')
        assert sorted(row['legacy_references'] + row['non_text_references']) == row['raw_references']
        if row['kind'] in ('padding_prefix', 'unreferenced_ability'):
            assert row['raw_references'] == []
        if row['kind'] == 'padding_prefix':
            assert row['source_hex'].startswith('00')
            assert int(row['related_copies'][0]['offset'], 16) == int(row['offset'], 16) + 1


def test_live_counterparts_belong_to_other_batches():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    owners = {int(o, 16): b['id'] for b in batches for o in b['offsets']}
    consumers = [c for r in AUDIT['entries'] for c in r['current_move_consumers']]
    assert consumers
    for consumer in consumers:
        assert consumer['batch'] == owners[int(consumer['target'], 16)]
        assert consumer['batch'] in ('PT-37', 'PT-38')
        assert int(consumer['pointer'], 16) == 0x99F190 + 4 * consumer['move_id']
