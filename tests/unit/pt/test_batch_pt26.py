"""PT-26 : périmètre fermé, histoire, pages et protections exactes."""
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
AUDIT = json.loads((ROOT / 'languages/pt/data/pt26_audit.json').read_text())
TEXTS, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
LIVE = [row for row in AUDIT['entries'] if row['status'] == 'translated']


def test_exact_manifest_and_protection():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-26')
    guards = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protected = {int(e['offset'], 16): e['expected'] for e in guards['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 288 and len(LIVE) == 276
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['reason']
        if row['status'] == 'exception':
            assert not row['references'] or offset == 0x7C6E34
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
    assert 'TM92' in texts[0x7C70CA] and 'Volt Switch' in texts[0x7C70CA]
    assert 'TM28' in texts[0x7C78A0] and 'Dig' in texts[0x7C78A0]
    assert 'SES Expressway' in texts[0x7C88FD]
    assert 'um passo' in texts[0x7C8456] and 'Boa sorte' in texts[0x7C8456]
    assert 'Sankren thoron!' in texts[0x7C8FB3]
    assert 'Mega Ring' in texts[0x7CE767] and 'Successor Maxima' in texts[0x7CE767]
    assert 'Looker, desligando.' in texts[0x7CFD04]
    assert 'concluir a libertação!' in texts[0x7D4ABB]
    assert 'Frozen Heights' in texts[0x7D5E59]
    assert 'JULGAMENTO' in texts[0x7D617A]


def test_finalizer_after_repairs_and_disjoint_from_other_batches():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_26') == 1
    assert steps.index('batch_26') > steps.index('repoint_stale')
    other = json.loads((ROOT / 'languages/pt/data/pt20_audit.json').read_text())
    refs = {p for row in LIVE for p in row['references']}
    assert not refs.intersection(p for row in other['entries'] for p in row['references'])


def test_visual_probe_samples_complete_messages_without_runtime_buffers():
    samples = [TEXTS[offset] for offset in (0x7C73CF, 0x7CDEC1)]
    assert all(text.count('\n') == 1 for text in samples)
    assert all(not re.search(r'<0xF[ABCD]>', text) for text in samples)
    assert 'coincidência' in samples[0]
    assert 'força' in samples[1]
