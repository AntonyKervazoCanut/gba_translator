"""PT-78 : périmètre fermé, pages, élevage, navigation et noms canoniques."""
import json
from pathlib import Path

import pytest
import yaml

from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt78_audit.json').read_text())
ROWS = AUDIT['entries']
LIVE = [r for r in ROWS if r['status'] != 'exception']


def test_exact_scope_and_protection():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-78')
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    texts = entries()
    assert [r['offset'] for r in ROWS] == manifest
    assert len(ROWS) == 299 and len(LIVE) == 297
    for row in ROWS:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['scene']
        if row['status'] == 'exception':
            assert not row['references'] and offset not in texts and offset not in guards
        else:
            assert texts[offset] == guards[offset] == row['portuguese']
            assert row['references']


@pytest.mark.parametrize('row', LIVE, ids=lambda r: r['offset'])
def test_commands_pages_and_budgets(row):
    text = row['portuguese'].replace(r'\n', '\n')
    raw = TextEncoder.encode_pokemon(text, strict=True)
    assert [c for c in commands(raw) if c != b'\xfe'] == [
        c for c in commands(bytes.fromhex(row['source_hex'])) if c != b'\xfe']
    assert raw[-1] == 255 and 255 not in raw[:-1]
    assert len(raw) == row['encoded_bytes']
    assert line_widths(text) == row['line_widths']
    assert max(row['line_widths']) <= row['max_width']
    assert max(row['expanded_widths']) <= row['pixel_budget'] == 192
    assert all(str(c[1]) in row['buffers'] for c in commands(raw) if c[0] == 0xFD)
    if row['layout'] == 'dialogue':
        for page in text.split('<0xFB>'):
            for n, segment in enumerate(page.split('<0xFA>')):
                assert segment.count('\n') <= (1 if n == 0 else 0)
    if row['layout'] == 'fixed_window':
        assert text.count('\n') <= 2
        assert '<0xFA>' not in text and '<0xFB>' not in text
        assert max(row['expanded_widths']) <= 172
    if row['status'] == 'retained_english':
        assert raw == bytes.fromhex(row['source_hex'])


def test_breeding_and_travel_rules():
    text = {r['index']: r.get('portuguese', '').replace(r'\n', ' ') for r in ROWS}
    assert all(term in text[40] for term in ('Destiny', 'Knot', 'cinco', 'três'))
    assert all(term in text[48] for term in ('Pikachu', 'Light Ball', 'Volt Tackle'))
    assert all(term in text[52] for term in ('mãe', 'pai', 'filhote'))
    assert '250000' in text[85] and '999999999' in text[147]
    assert 'segundas' in text[138] and 'sextas' in text[138]
    assert 'Cinco apitos' in text[135] and 'Não pode usar itens' in text[135]
    assert 'dois' in text[155] and 'Ember' in text[155] and 'Water Gun' in text[155]
    assert 'Air Balloon' in text[163]
    assert text[224].endswith('batalhas Pokémon.')  # source EN tronquée dans le corpus
    assert text[291] == 'Tarmigan Mansion<0xFB>Conquiste o poder da Megaevolução!'
    for row in ROWS[116:133]:
        assert row['status'] == 'retained_english'  # noms d'objets non attestés : F-759
    assert 'Tehl Town' in text[274]  # orthographe de la ROM source vivante


def test_shard_buffer_starts_on_second_line_and_floor_label_fits():
    assert r'entregou:\n<0xFD><0x0C>' in ROWS[113]['portuguese']
    assert r'precisa de:\n<0xFC><0x01><0x06><0xFD><0x0C>' in ROWS[115]['portuguese']
    assert ROWS[77]['buffers']['3'] == ROWS[81]['buffers']['3'] == '65535'
    assert ROWS[198]['portuguese'] == 'Tér.'
    assert max(ROWS[198]['expanded_widths']) <= 32


def test_finalizer_and_reference_isolation():
    patches = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert patches.count('batch_78') == 1
    assert all(patches.index(p) < patches.index('batch_78') for p in
               ('inline', 'font', 'repoint_stale', 'repair_lz77', 'repair_localized_lz77'))
    refs = {p for r in LIVE for p in r['references']}
    assert len(refs) == sum(len(r['references']) for r in LIVE)
    for file in (ROOT / 'languages/pt/data').glob('pt*_audit.json'):
        if file.name != 'pt78_audit.json':
            assert not refs.intersection(p for r in json.loads(file.read_text()).get('entries', [])
                                         for p in r.get('references', [])), file
