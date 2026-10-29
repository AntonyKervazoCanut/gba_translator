"""PT-05 : descriptions d'objets, cellules bornées et exceptions documentées."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt05_audit.json').read_text())
ROWS = AUDIT['entries']
BATCH = next(b for b in json.loads(
    (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-05')
PT = {}
for line in (ROOT / 'languages/pt/combined_pt.txt').read_text().splitlines():
    match = re.match(r'0x([\da-fA-F]+):\s?(.*)', line)
    if match:
        PT[int(match[1], 16)] = match[2].replace('\\n', '\n')


def test_manifest_coverage_and_exceptions() -> None:
    assert [e['offset'] for e in ROWS] == BATCH['offsets']
    assert len(ROWS) == 281
    assert sum(e['status'] == 'translated' for e in ROWS) == 180
    for row in ROWS:
        offset = int(row['offset'], 16)
        if row['status'] == 'exception':
            assert offset not in PT
            assert row['reason'] and not row['pointers']
        else:
            assert offset in PT and row['pointers']


@pytest.mark.parametrize('row', [e for e in ROWS if e['status'] == 'translated'],
                         ids=lambda e: e['offset'])
def test_item_cell_budget_and_structure(row: dict) -> None:
    text = PT[int(row['offset'], 16)]
    original = bytes.fromhex(row['source_hex'])
    encoded = TextEncoder.encode_pokemon(text, strict=True)
    assert len(encoded) <= len(original)
    assert encoded[-1] == 0xFF and 0xFF not in encoded[:-1]
    assert encoded.count(0xFE) == original.count(0xFE)
    assert not set(encoded) & {0xF7, 0xF8, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD}
    assert max(line_widths(text)) <= 192
    assert len(encoded) == row['pt_bytes']
    assert max(line_widths(text)) == row['max_line_pixels']


def test_item_effects_and_official_terms() -> None:
    for offset, amount in [(0x3D52B2, 20), (0x3D54B5, 200), (0x3D5503, 50),
                           (0x3D562B, 50), (0x3D567E, 60), (0x3D56C2, 80),
                           (0x3D5706, 100), (0x3D574F, 50), (0x3D579E, 200)]:
        assert f'{amount} PS' in PT[offset]
    for offset, steps in [(0x3D62DF, 200), (0x3D6318, 250), (0x3D639C, 100)]:
        assert f'{steps} passos' in PT[offset]
    assert 'eleva' in PT[0x3D5A6A] and 'Reduz' in PT[0x3D5AB8]
    assert 'Ataque Especial' in PT[0x3D75DE]
    assert 'Defesa Especial' in PT[0x3D761D]
    assert 'Terrestre' in PT[0x3D7FD5]
    assert 'The Shadows' in PT[0x3D90D7]
    assert 'Silph Co.' in PT[0x3D856E]
    assert 'Devon Corp.' in PT[0x3D936F]
    assert 'Clamperl' in PT[0x3D7BE5] and 'Chansey' in PT[0x3D86C0]
