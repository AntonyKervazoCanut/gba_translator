"""PT-25 : périmètre fermé, histoire, pages et protections exactes."""
import json
import re
from pathlib import Path

import pytest
import yaml

from scripts.apply_combined_fr import _load_combined
from scripts.apply_inline_overrides_fr import (
    _extract_control_sequences_from_raw,
    _normalize_text,
)
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt25_audit.json').read_text())
TEXTS, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
LIVE = [row for row in AUDIT['entries'] if row['status'] == 'translated']


def test_exact_manifest_and_protection():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-25')
    guards = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protected = {int(e['offset'], 16): e['expected'] for e in guards['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 288 and len(LIVE) == 272
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['reason']
        if row['status'] == 'exception':
            assert not row['references']
            assert offset not in TEXTS
        else:
            assert TEXTS[offset] == _normalize_text(row['portuguese'])
            assert protected[offset] == row['portuguese']
            assert row['references']


@pytest.mark.parametrize('row', LIVE, ids=lambda r: r['offset'])
def test_control_order_pages_and_pixel_budgets(row):
    text = TEXTS[int(row['offset'], 16)]
    raw = TextEncoder.encode_pokemon(text, strict=True)
    source = bytes.fromhex(row['source_hex'])
    def commands(data):
        return [s for s in _extract_control_sequences_from_raw(data) if s[0] != 0xFE]
    assert commands(raw) == commands(source)
    assert len(raw) == row['encoded_bytes']
    assert raw[-1] == 0xFF and 0xFF not in raw[:-1]
    assert line_widths(text) == row['line_widths']
    assert max(line_widths(text), default=0) <= row['max_width']
    assert all(part.count('\n') <= 1 for part in re.split(r'<0xF[AB]>', text))
    parts = re.split(r'(<0xF[AB]>)', text)
    for index in range(2, len(parts), 2):
        if parts[index - 1] == '<0xFA>':
            assert '\n' not in parts[index]  # Un scroll n'ajoute qu'une ligne.


def test_story_rewards_and_names():
    texts = {offset: text.replace('\n', ' ') for offset, text in TEXTS.items()}
    assert all(term in texts[0x7BC6EF] for term in ('Sandslash', 'amigos', 'família'))
    assert 'cinco Revives' in texts[0x7BCA5F].replace('\n', ' ')
    assert 'Terror Granbull' in texts[0x7C1783]
    assert 'SES Expressway' in texts[0x7C0B71]
    assert 'East Borrius' in texts[0x7C1E03]
    assert '70' in texts[0x7C13E2] and 'Hidden Power' in texts[0x7C13E2]
    assert 'nível 70' in texts[0x7C42A8]
    assert 'Sankren fimbulvetr!' in texts[0x7C590D]
    assert '¥4000' in texts[0x7C67A0]
    assert 'Graveler esqueceu Dig' in texts[0x7C6AAD]
    assert '4 dias' in texts[0x7C5BAC]
    assert 'Mega Ring' not in texts[0x7C4D1A]  # Le fragment vivant est la conclusion.
    assert TEXTS[0x7C182C].startswith('Sou presidente')
    assert texts[0x7C5FA5].endswith('<0xFC><0x01><0x06>menina de boia<0xFC><0x01><0x04>.')


def test_finalizer_after_repairs_and_disjoint_from_other_batches():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_25') == 1
    assert steps.index('batch_25') > steps.index('repoint_stale')
    other = json.loads((ROOT / 'languages/pt/data/pt20_audit.json').read_text())
    refs = {p for row in LIVE for p in row['references']}
    assert not refs.intersection(p for row in other['entries'] for p in row['references'])
