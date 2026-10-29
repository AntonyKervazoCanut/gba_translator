"""PT-35 : périmètre, protections et sémantique des combats."""
import json
from pathlib import Path

import yaml

from scripts.apply_combined_fr import _load_combined
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt35_audit.json').read_text())


def test_exact_scope_protections_and_commands():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-35')
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 288
    assert sum(r['status'] != 'exception' for r in AUDIT['entries']) == 163
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['source_hex'] and row['french_reference']
        if row['status'] == 'exception':
            assert offset not in texts
            if 'cell_offset' in row:
                assert row['canonical_bytes'] > row['cell_bytes']
            continue
        assert texts[offset] == guards[offset].replace(r'\n', '\n') == row['portuguese'].replace(r'\n', '\n')
        raw = TextEncoder.encode_pokemon(texts[offset].replace(r'\n', '\n'), strict=True)
        assert len(raw) == row['encoded_bytes']
        if 'cell_offset' in row:
            assert len(raw) <= row['cell_bytes'] == 7
            assert row['portuguese'] == row['canonical_portuguese']
        else:
            assert commands(raw) == commands(bytes.fromhex(row['source_hex']))


def test_battle_effects_and_glossary():
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    assert 'muito' not in texts[0x966B67]
    assert 'muito' in texts[0x966B8C] and 'muito' in texts[0x966BB6]
    assert 'PS' in texts[0x96DD81] and 'Poder Z' in texts[0x96DD81]
    for offset, name in [(0x9660A7, 'Heal Block'), (0x9660CD, 'Throat Chop'),
                         (0x9666AE, 'Shell Trap'), (0x96C02D, 'Power Herb')]:
        assert name in texts[offset]
    assert 'Ataque Especial' in texts[0x96C080]
    assert 'Defesa Especial' in texts[0x96C0BB]
    assert '<0xFD><0x10>' in texts[0x96BE0C]
    assert texts[0x965C16] == texts[0x96625D]
    config = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())
    assert config['patches'].count('batch_35') == 1
    assert config['patches'].index('batch_35') > config['patches'].index('repoint_stale')
