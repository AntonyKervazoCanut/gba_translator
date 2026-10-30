"""PT-51 : périmètre fermé, protections et faits des descriptions Pokédex."""
import json
from pathlib import Path

import yaml

from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt51_audit.json').read_text())


def test_exact_manifest_protections_controls_and_budgets():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-51')
    texts = entries()
    guards = {int(e['offset'], 16): e['expected'] for e in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    rows = AUDIT['entries']
    assert len(rows) == 300
    assert [r['offset'] for r in rows] == manifest
    for row in rows:
        offset = int(row['offset'], 16)
        assert row['status'] == 'translated'
        assert texts[offset] == guards[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(texts[offset].replace(r'\n', '\n'), strict=True)
        assert len(raw) == row['encoded_bytes']
        assert raw[-1] == 0xFF and 0xFF not in raw[:-1]
        assert raw.count(b'\xfe') == bytes.fromhex(row['source_hex']).count(b'\xfe')
        assert raw.count(b'\xfe') <= 2
        assert not any(c in raw for c in range(0xF7, 0xFE))
        assert max(row['max_font_widths']) <= 232
        assert row['references'] and row['reason']


def test_real_english_facts_and_glossary():
    texts = {r['offset']: r['portuguese'].replace(r'\n', ' ') for r in AUDIT['entries']}
    assert 'gás venenoso' in texts['0x16647d0']
    assert 'máscara de controle' in texts['0x1664dfa']
    assert 'almofadas especiais' in texts['0x1665d78']  # pas le liquide mauve du faux EN
    assert 'Karrablast' in texts['0x16613ac']
    assert 'Shelmet' in texts['0x166098e']
    assert 'Reuniclus' in texts['0x1660637']
    assert 'Team Plasma' in texts['0x1661fa8']
    assert 'Soul-Heart' in texts['0x166589f']
    assert 'Treinadores' in texts['0x166291f']
    assert 'movimentos de Gelo' in texts['0x1661299']
    assert 'frio' not in texts['0x166074a']  # EN réel : agréable à embrasser, pas le souffle à -50
    assert 'abraçar' in texts['0x166074a']
    assert 'Milcery' in texts['0x166741c'] and 'confeitaria' in texts['0x166741c']


def test_finalizer_follows_repairs():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_51') == 1
    assert all(steps.index(s) < steps.index('batch_51') for s in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))
