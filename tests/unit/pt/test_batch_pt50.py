"""PT-50 : périmètre fermé, sources réelles et protections exactes."""
import json
from pathlib import Path

import yaml

from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt50_audit.json').read_text())


def test_manifest_protection_and_control_contract():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    offsets = next(b['offsets'] for b in batches if b['id'] == 'PT-50')
    texts = entries()
    guards = {int(r['offset'], 16): r.get('expected_raw', r['expected']) for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == offsets
    assert len(offsets) == 299
    assert sum(r['status'] == 'exception' for r in AUDIT['entries']) == 117
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        assert row['reason'] and row['source_hex']
        assert 'english_reference' in row and 'french_reference' in row
        if row['status'] == 'exception':
            assert off not in texts and off not in guards
            assert not row['references'] and row['context_hex']
            continue
        assert texts[off] == guards[off] == row['portuguese']
        raw = TextEncoder.encode_pokemon(texts[off].replace(r'\n', '\n'), strict=True)
        assert len(raw) == row['encoded_bytes']
        assert raw[-1] == 0xFF and 0xFF not in raw[:-1]
        assert raw.count(b'\xfe') == bytes.fromhex(row['source_hex']).count(b'\xfe')
        assert 1 <= raw.count(b'\xfe') <= 2
        assert not any(c in raw for c in range(0xF7, 0xFE))
        assert max(row['line_widths']) <= row['max_width'] == 224


def test_english_rom_meaning_over_contaminated_corpus():
    texts = {r['offset']: r['portuguese'].replace(r'\n', ' ')
             for r in AUDIT['entries'] if r['status'] == 'translated'}
    # Le FR historique raconte d'autres faits : ne pas le traduire aveuglément.
    for off, words in {
        '0x165c4c4': ['orgulhoso', 'comida', 'frio'],
        '0x165c685': ['feroz', 'maiores'],
        '0x165d0df': ['atormentar', 'felicidade'],
        '0x165d8ad': ['180 graus', 'pontos cegos'],
        '0x165efd1': ['pesadelos', 'devora'],
        '0x165f36f': ['nariz'],
        '0x165f81d': ['próprias roupas', 'estilistas'],
        '0x1660251': ['lixo', 'gás venenoso'],
        '0x165d54c': ['108', 'Odd Keystone'],
        '0x165e4f2': ['Distortion World'],
        '0x165f5f5': ['Conkeldurr', '2.000'],
    }.items():
        assert all(word in texts[off] for word in words)


def test_finalizer_after_repairs():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_50') == 1
    assert all(steps.index(s) < steps.index('batch_50') for s in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))
