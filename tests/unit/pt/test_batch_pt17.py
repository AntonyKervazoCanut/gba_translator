"""PT-17 : couverture fermée, commandes source et sémantique des menus."""
import json
import re
from pathlib import Path

import yaml

from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt17_audit.json').read_text())


def test_manifest_protections_and_source_commands():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    manifest = next(b['offsets'] for b in batches if b['id'] == 'PT-17')
    guards = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protected = {int(e['offset'], 16): e['expected'] for e in guards['entries']}
    values = {int(m[1], 16): m[2] for line in
              (ROOT / 'languages/pt/combined_pt.txt').read_text().splitlines()
              if (m := re.match(r'0x([0-9a-fA-F]+): ?(.*)', line))}
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 281
    assert sum(r['status'] == 'translated' for r in AUDIT['entries']) == 210
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['source_hex'] and row['english'] and row['reason']
        if row['status'] == 'exception':
            assert offset not in values
            assert not row['references']
        else:
            assert values[offset] == protected[offset] == row['portuguese']
            encoded = TextEncoder.encode_pokemon(values[offset].replace(r'\n', '\n'), strict=True)
            assert len(encoded) == row['encoded_bytes']
            assert commands(encoded) == commands(bytes.fromhex(row['source_hex']))
            assert encoded[-1] == 0xFF and 0xFF not in encoded[:-1]


def test_decorations_moves_and_musical_scale():
    values = {int(r['offset'], 16): r.get('portuguese', '') for r in AUDIT['entries']}
    assert all(name in values[offset] for offset, name in [
        (0x454BFD, 'Surf'), (0x454C31, 'Thunder'), (0x454C68, 'Fire Blast'),
        (0x454CA2, 'Powder Snow'), (0x454CDB, 'Attract'),
        (0x454D13, 'Fissure'), (0x454D4A, 'Spikes'),
        (0x454DF2, 'Mudkip'), (0x45503E, 'Jigglypuff'),
    ])
    for offset, note in [(0x454A99, 'dó grave'), (0x454AC8, 'ré'),
                         (0x454AF3, 'mi'), (0x454B1F, 'fá'),
                         (0x454B4B, 'sol'), (0x454B76, 'lá'),
                         (0x454BA2, 'si'), (0x454BCD, 'dó agudo')]:
        assert note in values[offset]
    assert '50' in values[0x454901] and '100' in values[0x454933]
    assert 'Beldum' in values[0x44E199] and 'Groudon' in values[0x44E477]
    assert 'mil anos' in values[0x44E594]
    assert values[0x454254].endswith(r'Poké\nBall.')
    assert values[0x454420].endswith('Poké Ball.')
    assert values[0x454D80].endswith('Poké Balls.')


def test_link_choices_and_dynamic_buffers():
    values = {int(r['offset'], 16): r.get('portuguese', '') for r in AUDIT['entries']}
    for count, offset in enumerate([0x4573F4, 0x457402, 0x457410, 0x45741E], 2):
        assert values[offset] == f'MODO DE\\n{count} JOGADORES'
    assert 'Cartão de Treinador' in values[0x457C48]
    assert 'Ovo' in values[0x457DB8] and '<0xFB>' not in values[0x457DB8]
    assert 'movimento' in values[0x458618]
    assert values[0x4577BC].endswith('<0xB0>')
    for offset, count in ((0x457950, 21), (0x4579BC, 24)):
        assert values[offset].count('<0xFC><0x08><0x0F>') == count
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_17') == 1
    assert steps.index('batch_17') > steps.index('repoint_stale')
