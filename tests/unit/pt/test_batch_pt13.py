"""PT-13 : périmètre fermé et structure exacte des menus et résumés."""
import json
from pathlib import Path

import yaml

from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
ROWS = json.loads((ROOT / 'languages/pt/data/pt13_audit.json').read_text())['entries']


def test_scope_and_exact_protection():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    offsets = next(b['offsets'] for b in batches if b['id'] == 'PT-13')
    texts = entries()
    protected = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    guards = {int(e['offset'], 16): e.get('expected') for e in protected['entries']}
    assert [r['offset'] for r in ROWS] == offsets
    assert len(ROWS) == 281
    assert sum(r['status'] == 'translated' for r in ROWS) == 276
    for row in ROWS:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['source_hex']
        if row['status'] == 'exception':
            assert offset not in texts and not row['references']
            continue
        assert texts[offset] == row['portuguese'] == guards[offset]
        encoded = TextEncoder.encode_pokemon(texts[offset].replace(r'\n', '\n'), strict=True)
        assert len(encoded) == row['encoded_bytes'] <= 512
        assert encoded[-1] == 0xFF and 0xFF not in encoded[:-1]
        assert commands(encoded) == commands(bytes.fromhex(row['source_hex']))


def test_system_terminology_and_shop_positions():
    texts = entries()
    assert texts[0x4184C9] == 'Bolsa'
    assert texts[0x41854A] == 'Centro Pokémon'
    assert texts[0x418468] == 'Cancelar'
    assert 'HM' in texts[0x419CB9]
    assert texts[0x419CEF] == 'Pokédex'
    assert texts[0x4181A4] == 'VIT.<0xFC><0x13><0x30>DER.<0xFC><0x13><0x60>EMP.'
    for row in ROWS:
        if 0x4180A7 <= int(row['offset'], 16) <= 0x418163:
            # Noms sans attestation officielle conservés ; tarifs et colonnes identiques.
            assert TextEncoder.encode_pokemon(texts[int(row['offset'], 16)], strict=True).hex() == row['source_hex']
    assert texts[0x4183BA] == '<0xB0> <0xB0> <0xB0> <0xB0> <0xB0>!'


def test_floors_and_finalizer_contract():
    texts = entries()
    assert [texts[o] for o in range(0x41803A, 0x418055, 3)] == [f'{n}º' for n in range(1, 10)]
    assert [texts[o] for o in (0x418055, 0x418059)] == ['10º', '11º']
    assert [texts[o] for o in (0x41805D, 0x418061, 0x418065, 0x418069)] == ['S1', 'S2', 'S3', 'S4']
    config = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())
    assert config['patches'].count('batch_13') == 1
    for step in ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale'):
        assert config['patches'].index(step) < config['patches'].index('batch_13')
