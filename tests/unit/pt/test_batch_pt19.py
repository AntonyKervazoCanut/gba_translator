"""PT-19 : périmètre exact, protection et structure des 282 entrées."""
import json
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_width
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
ROWS = json.loads((ROOT / 'languages/pt/data/pt19_audit.json').read_text())['entries']


def test_manifest_and_exact_protection():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    offsets = next(b['offsets'] for b in batches if b['id'] == 'PT-19')
    protected = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    guards = {int(r['offset'], 16): r.get('expected_raw', r['expected']) for r in protected['entries']}
    texts = entries()
    assert [r['offset'] for r in ROWS] == offsets
    assert len(ROWS) == 282
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
    assert 'Centro' in texts[0x48422E]
    assert 'PS' in texts[0x484398]
    assert 'Habilidade' in texts[0x4870DD]
    assert 'dois a seis' in texts[0x48649F].replace(r'\n', ' ')
    assert 'Leech Seed' in texts[0x486532].replace(r'\n', ' ')
    assert all(r['portuguese'].count(r'\n') == 3 for r in ROWS[:255])
    config = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())
    for step in ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale'):
        assert config['patches'].index(step) < config['patches'].index('batch_19')


def test_full_stat_names_and_accuracy_meaning():
    texts = entries()
    assert 'Ataque Especial' in texts[0x486E37].replace(r'\n', ' ')
    assert 'Defesa Especial' in texts[0x487E30].replace(r'\n', ' ')
    assert 'sem errar' in texts[0x484A15].replace(r'\n', ' ')
    assert 'Salta' in texts[0x484BEB]
