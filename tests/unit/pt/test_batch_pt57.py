"""Couverture exacte, protections et cellules structurées du manifeste PT-57."""
import json
from pathlib import Path

import yaml

from scripts.apply_combined_fr import _load_combined
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextDecoder, TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt57_audit.json').read_text())


def test_manifest_protections_and_category_budgets():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-57')
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    guards = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protected = {int(r['offset'], 16): r['expected'] for r in guards['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    translated = [r for r in AUDIT['entries'] if r['status'] == 'translated']
    assert len(manifest) == 299 and len(translated) == 166
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['reason'] and 'english_reference' in row and 'french_reference' in row
        if row['status'] == 'exception':
            assert row['references'] == [] and offset not in texts
            assert row['source_hex'] and row['context_hex']
            continue
        assert texts[offset] == protected[offset] == row['portuguese']
        encoded = TextEncoder.encode_pokemon(texts[offset], strict=True)
        assert len(encoded) == row['encoded_bytes'] <= 12
        assert row['line_widths'] == line_widths(texts[offset])
        assert max(row['line_widths']) <= 66
        assert TextDecoder.decode_pokemon(bytes.fromhex(row['source_hex'])) == row['english']
        assert TextDecoder.decode_pokemon(encoded) == texts[offset]
        assert all(c < 0xF7 for c in encoded[:-1])
        assert int(row['cell_offset'], 16) == 0x1A357CC + row['dex_index'] * 36
        assert row['source_delta'] in (2, 6)


def test_corrupt_extraction_prefixes_are_not_rendered():
    rows = {r['offset']: r for r in AUDIT['entries']}
    assert rows['0x1a363de']['portuguese'] == 'Leão-do-mar'
    assert rows['0x1a36816']['portuguese'] == 'Dragão'
    assert rows['0x1a378d2']['portuguese'] == 'Pintor'
    assert all(rows[o]['source_delta'] == 6 for o in ('0x1a363de', '0x1a36816', '0x1a378d2'))
