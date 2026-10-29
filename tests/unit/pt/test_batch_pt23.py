"""PT-23 : périmètre, ruptures, noms et mécanique des zones Borrius."""
import json
import re
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_width
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt23_audit.json').read_text())


def test_exact_manifest_protection_and_control_flow():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    offsets = next(b['offsets'] for b in batches if b['id'] == 'PT-23')
    rows = AUDIT['entries']
    texts = entries()
    guards = {int(r['offset'], 16): r.get('expected_raw', r['expected']) for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in rows] == offsets
    assert len(rows) == 288
    assert sum(r['status'] == 'translated' for r in rows) == 262
    for row in rows:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['source_hex']
        if row['status'] == 'exception':
            assert offset not in texts and not row['references']
            continue
        assert texts[offset] == guards[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(texts[offset].replace(r'\n', '\n'), strict=True)
        assert len(raw) == row['encoded_bytes'] <= 512
        assert raw[-1] == 0xFF and 0xFF not in raw[:-1]
        assert commands(raw) == commands(bytes.fromhex(row['source_hex']))
        widths = [line_width(line) for line in re.split(r'<0xF[AB]>|\\n', texts[offset])]
        assert widths == row['line_widths']
        assert max(widths) <= 192


def test_domain_mechanics_and_retained_names():
    texts = entries()
    for offset, word in [(0x792504, '10 por cento'), (0x7929CD, '50 por cento'),
                         (0x792A1D, 'temporária'), (0x78EAFE, '50'),
                         (0x78EB95, 'Aerial Ace'), (0x7A823B, 'Electrizer'),
                         (0x7A29F4, 'SES Expressway'), (0x78D43E, 'Cinder Volcano')]:
        assert word in texts[offset].replace(r'\n', ' ')
    inverse = texts[0x7A36CA].replace(r'\n', ' ')
    assert 'Água fica fraca contra Fogo' in inverse and 'resiste a Planta' in inverse
    assert [texts[o] for o in (0x793D11, 0x793D18, 0x793D1F, 0x793D26)] == [
        'Primavera', 'Verão', 'Outono', 'Inverno']
    assert texts[0x78C364].startswith('Oi, Treinador das ondas!')
    assert 'National Science Society' in texts[0x793C67]
    assert texts[0x78D717] == 'Dehara City'
    assert texts[0x7A2565] == 'Tarmigan Town'
    assert 'Link Stone' in texts[0x7A81DA] and 'por troca' in texts[0x7A81DA]
    config = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())
    assert config['patches'].count('batch_23') == 1
    for step in ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale'):
        assert config['patches'].index(step) < config['patches'].index('batch_23')
