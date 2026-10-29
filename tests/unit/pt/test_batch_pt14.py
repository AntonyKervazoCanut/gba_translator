"""PT-14 : périmètre fermé, protections et sémantique des systèmes."""
import json
import re
from pathlib import Path

import yaml

from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands

ROOT = Path(__file__).resolve().parents[3]
ROWS = json.loads((ROOT / 'languages/pt/data/pt14_audit.json').read_text())['entries']


def texts() -> dict[int, str]:
    """Résout les valeurs vivantes sans supprimer les espaces de concaténation."""
    return {int(m[1], 16): m[2] for line in
            (ROOT / 'languages/pt/combined_pt.txt').read_text().splitlines()
            if (m := re.match(r'0x([0-9a-fA-F]+): ?(.*)', line))}


def test_manifest_and_exact_protections():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    manifest = next(b['offsets'] for b in batches if b['id'] == 'PT-14')
    guards = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protected = {int(e['offset'], 16): e['expected'] for e in guards['entries']}
    values = texts()
    assert len(ROWS) == len(manifest) == 282
    assert [r['offset'] for r in ROWS] == manifest
    assert sum(r['status'] == 'exception' for r in ROWS) == 32
    for row in ROWS:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['source_hex'] and row['english']
        if row['status'] == 'exception':
            assert offset not in values
            assert not row['references']
            assert row['replacement']['references']
        else:
            assert values[offset] == protected[offset] == row['portuguese']
            encoded = TextEncoder.encode_pokemon(values[offset].replace(r'\n', '\n'), strict=True)
            assert len(encoded) == row['encoded_bytes']
            assert encoded[-1] == 0xFF and 0xFF not in encoded[:-1]
            assert commands(encoded) == commands(bytes.fromhex(row['source_hex']))


def test_tutorials_keep_move_identity_and_source_tail():
    values = texts()
    assert 'Focus Punch' in values[0x41C693]
    assert 'Water Pulse' in values[0x41C587]
    assert 'Bullet Seed' in values[0x41C587]
    assert 'PLANTA' in values[0x41BE76] and 'ÁGUA' in values[0x41BE76]
    assert values[0x41BE76].endswith('POKé DUDE SHOW!')
    assert 'Teachy TV' in values[0x41C994] and 'Select' in values[0x41C994]


def test_loss_destinations_and_buffer_order():
    values = texts()
    assert 'Centro Pokémon' in values[0x41B554]
    assert 'casa' in values[0x41B5B6] and 'Centro Pokémon' not in values[0x41B5B6]
    assert values[0x41B285].startswith('<0x00>')
    assert values[0x41B295].startswith('<0x00>')
    assert values[0x41B524] == 'Batalha'
    assert values[0x41B836] == 'Cancelar'
    assert 'Batalha Individual' in values[0x41A422]
    assert 'Batalha Dupla' in values[0x41A477]
    assert 'PS' in values[0x41A8E0] and 'SOFTBOILED' in values[0x41A8E0]
    assert '<0xFC><0x17><0xFC><0x0B><0x01><0x01>' in values[0x41CEA8]
    assert '<0xFC><0x18><0xFB>' in values[0x41CEA8]


def test_finalizer_runs_after_generic_repairs():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_14') == 1
    for earlier in ['inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale']:
        assert steps.index(earlier) < steps.index('batch_14')
