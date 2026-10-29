"""PT-38 : couverture exacte et sémantique des descriptions de mouvements."""
import json
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_width
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt38_audit.json').read_text())
ROWS = AUDIT['entries']


def test_exact_manifest_protection_and_layout():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    offsets = next(b['offsets'] for b in batches if b['id'] == 'PT-38')
    protected = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    guards = {int(r['offset'], 16): r['expected'] for r in protected['entries']}
    texts = entries()
    assert [r['offset'] for r in ROWS] == offsets
    assert len(ROWS) == AUDIT['translated'] == 283
    assert AUDIT['exceptions'] == 0
    for row in ROWS:
        offset = int(row['offset'], 16)
        assert row['status'] == 'translated' and row['move_ids'] and row['references']
        assert texts[offset] == guards[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(texts[offset].replace(r'\n', '\n'), strict=True)
        assert len(raw) == row['encoded_bytes'] < 512
        assert raw[-1] == 0xFF and 0xFF not in raw[:-1]
        assert raw.count(0xFE) == bytes.fromhex(row['source_hex']).count(0xFE)
        assert not any(c in raw[:-1] for c in range(0xF7, 0xFE))
        widths = [line_width(l) for l in texts[offset].split(r'\n')]
        assert widths == row['line_widths']
        assert len(widths) <= 5 and max(widths) <= 122


def test_mechanics_follow_english_instead_of_french():
    texts = {int(r['offset'], 16): r['portuguese'].replace(r'\n', ' ') for r in ROWS}
    assert 'escalar paredes' in texts[0xA388F4]
    assert 'ulceração por frio' in texts[0xA393E1]
    assert 'ulceração por frio' in texts[0xA3A6D6]
    assert 'confundem' in texts[0xA3BC34]
    assert 'queimadura' in texts[0xA3B892]
    assert 'PS máximos' in texts[0xA389C2]
    assert 'Insomnia' in texts[0xA39F84]
    assert 'Light Screen e Reflect' in texts[0xA3CA1F]
    assert 'Water Pledge' in texts[0xA3D286]
    assert all('Atq.' not in t and 'Def.' not in t for t in texts.values())
    config = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())
    steps = config['patches']
    assert steps.count('batch_38') == 1
    # Les lots indépendants suivants peuvent finaliser leurs propres offsets.
    for prerequisite in ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale'):
        assert steps.index(prerequisite) < steps.index('batch_38')
