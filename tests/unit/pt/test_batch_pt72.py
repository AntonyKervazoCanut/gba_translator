"""PT-72 : manifeste fermé, répliques complètes, commandes et menus."""
import json
import re
from pathlib import Path

import pytest
import yaml

from scripts.apply_combined_fr import _load_combined, _normalize_text
from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt72_audit.json').read_text())
LIVE = [r for r in AUDIT['entries'] if r['status'] != 'exception']
TEXTS, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')


def test_exact_manifest_and_protection():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-72')
    guards = {int(e['offset'], 16): e['expected'] for e in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 300 and len(LIVE) == 299
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['reason']
        if row['status'] == 'exception':
            assert row['offset'] == '0x1f454a2' and not row['references']
            assert offset not in TEXTS and offset not in guards
        else:
            assert TEXTS[offset] == _normalize_text(guards[offset])
            assert guards[offset] == row['portuguese']
            assert row['references'] or row['consumer_references']


@pytest.mark.parametrize('row', LIVE, ids=lambda r: r['offset'])
def test_commands_pages_and_pixel_budgets(row):
    text = TEXTS[int(row['offset'], 16)]
    raw = TextEncoder.encode_pokemon(text, strict=True)
    source = bytes.fromhex(row['source_hex'])
    def commands(data):
        return [s for s in _extract_control_sequences_from_raw(data) if s[0] != 0xFE]
    assert commands(raw) == commands(source)
    assert all(str(command[1]) in row['buffers'] for command in commands(raw)
               if command[0] == 0xFD)
    assert len(raw) == row['encoded_bytes']
    assert raw[-1] == 255 and 255 not in raw[:-1]
    assert line_widths(text) == row['line_widths']
    assert max(row['line_widths']) <= row['max_width']
    if row['status'] == 'retained_english':
        assert raw == source
    if row['kind'] == 'dialogue':
        parts = re.split(r'(<0xF[AB]>)', text)
        assert all(part.count('\n') <= 1 for part in parts[::2])
        assert all('\n' not in parts[i] for i in range(2, len(parts), 2)
                   if parts[i - 1] == '<0xFA>')


def test_story_rules_canonical_names_and_complete_long_speeches():
    text = {o: t.replace('\n', ' ') for o, t in TEXTS.items()}
    assert 'Ultimate Weapon' in text[0x1F4A574]
    assert 'Distortion World' in text[0x1F4639B]
    assert 'Sticky Hold' in text[0x1F49330]
    assert 'Batalha Dupla' in text[0x1F4B5B6]
    assert 'Redwood Village' in text[0x1F4AD47]
    assert text[0x1F4AD47].endswith('quando chegar ao topo!')
    assert text[0x1F4B80A].endswith('Me siga!')
    assert text[0x1F4BEF9].endswith('terei uma Missão para você.')
    assert text[0x1F4C2ED].endswith('na sua Pokédex.')
    assert text[0x1F4D8C4] == 'Newmoon Island'
    assert 'Fullmoon Island' in text[0x1F4D924]
    assert text[0x1F4DA71] == 'HMs rápidas'
    assert text[0x1F4DA7B] == 'Pular cenas'
    assert text[0x1F4DA8A] == 'Avisos p/salvar'


def test_finalizer_order_and_other_batch_isolation():
    patches = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert patches.count('batch_72') == 1
    assert all(patches.index(p) < patches.index('batch_72') for p in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))
    refs = {p for row in LIVE for p in row.get('consumer_references', row['references'])}
    for file in (ROOT / 'languages/pt/data').glob('pt*_audit.json'):
        if file.name != 'pt72_audit.json':
            assert not refs.intersection(p for r in json.loads(file.read_text()).get('entries', [])
                                         for p in r.get('references', [])), file
    assert sum(len(r['non_text_references']) for r in LIVE) == 1


def test_context_buffers_are_local_and_gender_safe():
    assert len(AUDIT['context_buffers']) == 3
    assert [b['text'] for b in AUDIT['context_buffers'][:2]] == ['seu', 'jovem']
    assert AUDIT['context_buffers'][2]['male'] == 'meu filho'
    assert AUDIT['context_buffers'][2]['female'] == 'minha filha'
    assert 'Surpresa' not in TEXTS[0x1F4BEF9]
    assert 'meu <0xFD>' not in TEXTS[0x1F4C2ED]
    assert '3000 anos atrás' in TEXTS[0x1F49B96]
