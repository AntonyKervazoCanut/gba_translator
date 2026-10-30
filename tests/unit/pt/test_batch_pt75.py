"""PT-75 : périmètre fermé, structure, énigmes et règles de jeu."""
import json
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt75_audit.json').read_text())


def test_manifest_protections_controls_and_budgets():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-75')
    texts = entries()
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert len(manifest) == 300
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['scene'] and row['full_english']
        if row['status'] == 'exception':
            assert row['index'] in (26, 68, 143, 258)
            assert not row['references']
            assert offset not in texts and offset not in guards
            continue
        text = texts[offset]
        assert text == guards[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(text.replace(r'\n', '\n'), strict=True)
        assert len(raw) == row['encoded_bytes']
        assert raw[-1] == 0xFF and 0xFF not in raw[:-1]
        assert [c for c in commands(raw) if c != b'\xfe'] == [
            c for c in commands(bytes.fromhex(row['source_hex'])) if c != b'\xfe']
        widths = line_widths(text.replace(r'\n', '\n'))
        assert widths == row['line_widths'] and max(widths) <= 192
        assert row.get('consumer_references', row['references'])
        if row['layout'] == 'dialogue':
            for page in raw.split(b'\xfb'):
                assert page.split(b'\xfa')[0].count(b'\xfe') <= 1
                assert all(b'\xfe' not in part for part in page.split(b'\xfa')[1:])


def test_regi_riddles_keep_their_static_layout_and_instructions():
    for index, lines, required in [(13, 4, ('CENTRO', 'CRIE')),
                                   (17, 4, ('GELO', 'PURO')),
                                   (20, 5, ('NATUREZA', 'GIRE', 'CRISTAIS'))]:
        text = AUDIT['entries'][index]['portuguese']
        assert len(text.split(r'\n')) == lines
        assert all(word in text for word in required)
        # Même fenêtre native pour les trois inscriptions : EN atteint 14 cellules.
        budget = max(len(line) for i in (13, 17, 20)
                     for line in AUDIT['entries'][i]['full_english'].splitlines())
        assert all(len(line) <= budget for line in text.split(r'\n'))
        assert text.isascii() and all(line == line.upper() for line in text.split(r'\n'))
    assert len(AUDIT['entries'][25]['portuguese'].split(r'\n')) == 4


def test_gameplay_rules_names_and_gender_buffers():
    rows = AUDIT['entries']
    assert 'Luck Incense' in rows[3]['portuguese'] and 'dobrar' in rows[3]['portuguese']
    assert 'Soak' in rows[12]['portuguese'] and 'Net Ball' in rows[12]['portuguese']
    assert 'Macho Brace' in rows[45]['portuguese']
    assert 'pontos de esforço' in rows[48]['portuguese'].replace(r'\n', ' ')
    assert 'Nature\'s Madness' in rows[74]['portuguese']
    assert 'uma vez por batalha' in rows[113]['portuguese'].replace(r'\n', ' ')
    assert 'Devon Scope' in rows[260]['portuguese']
    assert 'KBT Expressway' in rows[239]['portuguese']
    assert 'Crater Town' in rows[239]['portuguese'] and 'Tehl Town' in rows[239]['portuguese']
    assert [rows[i]['portuguese'] for i in (41, 42)] == ['menino', 'menina']
    assert 'simples <0xFD><0x02>' in rows[33]['portuguese'].replace(r'\n', ' ')
    assert 'Terrestre' in rows[244]['portuguese']
    assert 'Drizzle' in rows[248]['portuguese'] and 'Sweet Scent' in rows[251]['portuguese']


def test_finalizer_and_pcm_classification():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_75') == 1
    assert all(steps.index(p) < steps.index('batch_75') for p in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))
    pcm_rows = [r for r in AUDIT['entries'] if r.get('pcm_matches')]
    assert [r['index'] for r in pcm_rows] == [230, 258, 284, 288]
    for row in pcm_rows:
        assert {p['site'] for p in row['pcm_matches']} == set(row['non_text_references'])
        assert not set(row['references']).intersection(row['non_text_references'])
