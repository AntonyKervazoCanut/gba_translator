"""PT-49 : descriptions gItems, glossaire et couverture exacte du manifeste."""
import json
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_width
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt49_audit.json').read_text())
ROWS = AUDIT['entries']


def test_manifest_protection_layout_and_no_binary_translation():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    offsets = next(b['offsets'] for b in batches if b['id'] == 'PT-49')
    guards = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protected = {int(r['offset'], 16): r['expected'] for r in guards['entries']}
    texts = entries()
    assert [r['offset'] for r in ROWS] == offsets
    assert len(ROWS) == 283
    assert (AUDIT['translated'], AUDIT['retained'], AUDIT['exceptions']) == (210, 33, 40)
    for row in ROWS:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['english'] and row['source_hex']
        if row['status'] != 'translated':
            assert offset not in texts
            continue
        assert texts[offset] == protected[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(texts[offset].replace(r'\n', '\n'), strict=True)
        assert len(raw) == row['encoded_bytes'] < 512
        assert raw[-1] == 0xFF and 0xFF not in raw[:-1]
        source = bytes.fromhex(row['source_hex'])
        assert raw.count(0xFE) == source.count(0xFE)
        assert not any(0xF7 <= c < 0xFE for c in raw[:-1])
        widths = [line_width(l) for l in texts[offset].split(r'\n')]
        assert widths == row['line_widths']
        assert len(widths) == row['layout']['max_lines']
        assert max(widths) <= row['layout']['max_width']


def test_mechanics_and_canonical_names():
    texts = {int(r['offset'], 16): r.get('portuguese', '').replace(r'\n', ' ') for r in ROWS}
    assert 'uma vez' in texts[0xEB4946]
    assert 'Techno Blast' in texts[0xEB5007]
    assert 'Necrozma, que precisa de luz, com Solgaleo' in texts[0xEB575A]
    assert 'Megaevolução' in texts[0xEB5C8B]
    assert 'PS máximos' in texts[0xEB8732]
    assert 'Ataque Especial' in texts[0xEB8865]
    assert 'Defesa Especial' in texts[0xEB88CC]
    assert 'Trick Room' in texts[0xEB8A65]
    assert 'quatro' not in texts[0xEB8D15] and '4 a 5 turnos' in texts[0xEB8D15]
    assert 'não pode fugir' in texts[0xEB8D15]
    assert 'cinco turnos' in texts[0xEB902D] and 'granizo' in texts[0xEB902D]
    assert 'não pode atacar' in texts[0xEB9089]
    glossary = yaml.safe_load((ROOT / 'languages/pt/data/official_terminology.yaml').read_text())
    for row in ROWS[:18]:
        english_type = row['english'].split('-type')[0].split()[-1].replace(r'\n', '')
        assert glossary['categories']['types']['entries'][english_type]['value'] in row['portuguese']
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_49') == 1
    assert all(steps.index(p) < steps.index('batch_49') for p in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale'))
