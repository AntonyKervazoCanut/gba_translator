"""PT-65 : périmètre, commandes, pages, budgets et mécanique du scénario."""
import json
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt65_audit.json').read_text())


def test_manifest_protections_pages_and_budgets():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    manifest = next(b['offsets'] for b in batches if b['id'] == 'PT-65')
    texts = entries()
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 299
    assert sum(r['status'] == 'exception' for r in AUDIT['entries']) == 6
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['source_hex'] and row['english_full']
        if row['status'] == 'exception':
            assert offset not in texts and not row['references']
            assert row['owner_sites']
            continue
        assert texts[offset] == guards[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(texts[offset].replace(r'\n', '\n'), strict=True)
        source = bytes.fromhex(row['source_hex'])
        assert len(raw) == row['encoded_bytes']
        assert raw[-1] == 0xFF and 0xFF not in raw[:-1]
        assert commands(raw) == commands(source), row['offset']
        assert line_widths(texts[offset].replace(r'\n', '\n')) == row['line_widths']
        assert max(row['line_widths']) <= row['max_width']
        if row['layout'] == 'mission':
            assert texts[offset].count(r'\n') <= 2


def test_rewards_randomizers_and_story_mechanics():
    texts = {o: t.replace(r'\n', ' ').replace('<0xFA>', ' ') for o, t in entries().items()}
    for offset, terms in {
        0x1f0ca95: ['Antidote', 'Poké Mart'],
        0x1f0e744: ['Cloud Burst', '3000', 'único dia'],
        0x1f0ebe7: ['uma hora', 'duas vezes', 'dobro'],
        0x1f0f004: ['6 Pokémon', 'Egg Moves', 'Z-Crystals', 'EVs', 'IVs', 'BP', 'Seaport City', 'Crater Town'],
        0x1f108b4: ['PS', '600', 'Shedinja', 'Huge Power'],
        0x1f10a07: ['100%', 'HMs', 'NÃO', 'Especialista', 'Insana', 'LIMITADO', 'Battle Tower'],
        0x1f11ea8: ['Great Desert'],
        0x1f1206e: ['Undying Lucario', 'batalhas'],
        0x1f126ce: ['Scizorite', 'Scyther', 'Scizor'],
        0x1f12d0f: ['Rufflet', 'segundas'],
        0x1f12dce: ['Vullaby', 'quintas'],
        0x1f130dc: ['Cut', 'panquecas'],
    }.items():
        for term in terms:
            assert term in texts[offset], (hex(offset), term)
    assert texts[0x1f0f842] == 'Cor do cinto e das botas.'
    # Le récit EN ne nomme pas Kalos : aucune inférence reprise du français.
    assert 'Kalos' not in texts[0x1f1129a]
    # Le titre propre reste intact et son faux préfixe ne devient pas une entrée.
    assert texts[0x1f12ff4] == 'Grim Woods' and 0x1f12ff3 not in texts


def test_finalizer_runs_after_repairs():
    patches = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert patches.count('batch_65') == 1
    for step in ('inline', 'font', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale'):
        assert patches.index(step) < patches.index('batch_65')
