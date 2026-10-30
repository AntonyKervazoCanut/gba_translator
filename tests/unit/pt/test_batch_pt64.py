"""PT-64 : périmètre, commandes, méthodes d’évolution et objectifs des missions."""
import json
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt64_audit.json').read_text())


def test_closed_manifest_protections_and_commands():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-64')
    texts = entries()
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 300
    assert sum(r['status'] == 'retained' for r in AUDIT['entries']) == 8
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['references'] and row['scene'] and row['reason']
        assert row['english_reference'] and row['english_full']
        assert texts[offset] == guards[offset] == row['portuguese']
        text = texts[offset].replace(r'\n', '\n')
        raw = TextEncoder.encode_pokemon(text, strict=True)
        assert len(raw) == row['encoded_bytes']
        assert raw[-1] == 0xFF and 0xFF not in raw[:-1]
        # FE peut être déplacé pour les lignes PT ; pages et scrolls sont exacts.
        assert [c for c in commands(raw) if c != b'\xfe'] == [
            c for c in commands(bytes.fromhex(row['source_hex'])) if c != b'\xfe']
        assert line_widths(text) == row['line_widths']
        assert max(row['expanded_widths']) <= row['pixel_budget']
        if '<0xFB>' in text or '<0xFA>' in text:
            for page in text.split('<0xFB>'):
                for index, segment in enumerate(page.split('<0xFA>')):
                    assert segment.count('\n') <= (1 if index == 0 else 0)


def test_evolution_conditions_and_glossary():
    rows = AUDIT['entries']
    assert 'Ataque maior que Defesa' in rows[37]['portuguese']
    assert 'Ataque igual à Defesa' in rows[38]['portuguese']
    assert 'Ataque menor que Defesa' in rows[39]['portuguese']
    assert 'Poké Ball extra' in rows[40]['portuguese']
    assert 'fora de batalha' in rows[53]['portuguese']
    assert '3 golpes críticos' in rows[61]['portuguese']
    assert 'segurando' in rows[64]['portuguese']
    assert 'Fogo' in rows[71]['portuguese'] and 'Planta' in rows[71]['portuguese']
    assert 'Lutador' in rows[228]['portuguese'] and 'Dragão' in rows[234]['portuguese']
    assert 'Magmarizer' in rows[10]['portuguese'] and 'Electirizer' in rows[11]['portuguese']
    assert 'Thursday' in rows[254]['english_full'] and 'quinta-feira' in rows[254]['portuguese']


def test_missions_and_full_dialogue_tails():
    rows = AUDIT['entries']
    for index in (81, 102, 103, 104, 105, 106, 118, 134, 142, 150, 159, 168, 177, 205):
        row = rows[index]
        assert row['pixel_budget'] == 172
        assert len(row['portuguese'].split(r'\n')) <= 3
    assert '4 dias diferentes' in rows[107]['portuguese']
    assert 'mínimo' in rows[121]['portuguese'] and '70' in rows[121]['portuguese']
    assert 'não foi você' in rows[131]['portuguese']
    assert 'Safari Zone' in rows[151]['portuguese']
    assert 'três' in rows[206]['portuguese'] and 'sete' in rows[206]['portuguese']
    assert '42 itens' in rows[279]['portuguese']
    assert '<0xF8><0x02>' in rows[279]['portuguese'] and '<0xF8><0x03>' in rows[279]['portuguese']
    assert rows[85]['english_full'].endswith(' Missions.')
    assert 'presente de adeus' in rows[279]['portuguese']
    for index in (138, 146, 163, 181):
        assert 'vez<0xFD>' not in rows[index]['portuguese']
    # La lettre plein écran garde toutes ses lignes et ses lignes vides.
    assert rows[284]['portuguese'].count(r'\n') == rows[284]['english_full'].count('<0xFE>')


def test_finalizer_runs_after_generic_repairs():
    patches = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert patches.count('batch_64') == 1
    for earlier in ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'):
        assert patches.index(earlier) < patches.index('batch_64')
