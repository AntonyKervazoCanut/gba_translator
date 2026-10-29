"""PT-15 : périmètre exact, protection et structure des 281 entrées."""
import json
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_width
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
ROWS = json.loads((ROOT / 'languages/pt/data/pt15_audit.json').read_text())['entries']


def test_manifest_and_exact_protection():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    offsets = next(b['offsets'] for b in batches if b['id'] == 'PT-15')
    protected = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    guards = {int(r['offset'], 16): r.get('expected_raw', r['expected']) for r in protected['entries']}
    texts = entries()
    assert [r['offset'] for r in ROWS] == offsets
    assert len(ROWS) == 281
    assert sum(r['status'] == 'translated' for r in ROWS) == 273
    for row in ROWS:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['source_hex']
        if row['status'] == 'exception':
            assert not row['references'] and offset not in texts
            continue
        assert texts[offset] == guards[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(texts[offset].replace(r'\n', '\n'), strict=True)
        assert len(raw) == row['encoded_bytes'] <= 512
        assert raw[-1] == 0xFF and 0xFF not in raw[:-1]
        assert commands(raw) == commands(bytes.fromhex(row['source_hex']))
        widths = [line_width(line) for page in texts[offset].split('<0xFB>')
                  for line in page.split(r'\n')]
        assert widths == row['line_widths']
        assert max(widths) <= row['layout']['max_width']


def test_domain_contract_and_glossary():
    texts = entries()
    assert texts[0x41e234] == 'De '
    assert texts[0x41e0b9] == 'Cancelar'
    assert texts[0x41e0d2] == 'Resumo'
    assert 'movimento' in texts[0x41e50c]
    assert texts[0x41e5ed] == 'DAISY'
    assert texts[0x41ee2b] == 'APAGAR<0xFC><0x13><0x57>CANCELAR<0xFC><0x13><0xA4>OK'
    dex = [r for r in ROWS if int(r['offset'], 16) >= 0x444C35]
    assert len(dex) == 86
    assert all(r['portuguese'].count(r'\n') == 2 for r in dex)
    assert 'Geodude' in texts[0x446664]
    config = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())
    for step in ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale'):
        assert config['patches'].index(step) < config['patches'].index('batch_15')
