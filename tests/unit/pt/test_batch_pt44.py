"""PT-44 : périmètre, protections et répliques de Dresseurs."""
import json
import re
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_width
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt44_audit.json').read_text())


def test_manifest_protection_controls_and_budgets():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-44')
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    texts = entries()
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 282
    assert sum(r['status'] == 'translated' for r in AUDIT['entries']) == 249
    for row in AUDIT['entries']:
        offset, text = int(row['offset'], 16), row['portuguese']
        if row['status'] == 'translated':
            assert texts[offset] == guards[offset] == text
        else:
            assert text == row['english'] == texts.get(offset, text)
        encoded = TextEncoder.encode_pokemon(text.replace(r'\n', '\n'), strict=True)
        assert len(encoded) == row['encoded_bytes'] < 512
        assert [b for b in encoded if b >= 0xF7] == [
            b for b in bytes.fromhex(row['source_hex']) if b >= 0xF7]
        widths = [line_width(s) for s in re.split(r'\\n|<0xFA>|<0xFB>', text)]
        assert widths == row['line_widths'] and max(widths) <= 204
        assert row['references'] and row['reason']


def test_meaning_names_and_glossary():
    texts = entries()
    assert '3%' in texts[0xA45C6E]
    assert 'percentil 97' in texts[0xA45DD0]
    assert 'Pickpocket' in texts[0xA462CA]
    assert 'Treinador honesto' in texts[0xA46275]
    assert 'rinite alérgica' in texts[0xA45EF3]
    assert 'ladrão honesto' in texts[0xA463FF]
    assert 'séries de vitórias' in texts[0xA4634A]
    names = {r['offset']: r['portuguese'] for r in AUDIT['entries'][:33]}
    assert names['0xa4524b'] == 'Big Mo'
    assert names['0xa45252'] == 'Galavan'
    assert names['0xa4527b'] == 'Tessy'
