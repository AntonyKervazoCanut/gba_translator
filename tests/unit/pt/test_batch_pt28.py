"""PT-28 : périmètre fermé, histoire, pages et protections exactes."""
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
AUDIT = json.loads((ROOT / 'languages/pt/data/pt28_audit.json').read_text())
TEXTS, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
LIVE = [row for row in AUDIT['entries'] if row['status'] == 'translated']


def test_exact_manifest_and_protection():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-28')
    guards = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protected = {int(e['offset'], 16): e['expected'] for e in guards['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 288 and len(LIVE) == 277
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
    texts = {o: t.replace('\n', ' ') for o, t in TEXTS.items()}
    for offset, letter in [(0x7F270E, 'A'), (0x7F2A66, 'K'),
                           (0x7F2D3F, 'L'), (0x7F32C7, 'O'), (0x7F37BF, 'V')]:
        assert f'<0xFC><0x01><0x06>{letter}' in texts[offset]
    assert 'última letra é E' in texts[0x7F46A3]
    assert '5 Hard Stones' in texts[0x7EED2A]
    assert 'Pearl String' in texts[0x7EEDAE]
    assert 'Lapras' in texts[0x7EE8F6] and 'Ditto' in texts[0x7EF4EE]
    assert 'The Shadows' in texts[0x7F4EBA]
    assert 'minha esposa' in texts[0x7F4CBB]
    assert 'ele' in texts[0x7F47CE] and 'ela' in texts[0x7F47FE]
    assert TEXTS[0x7F1533] == 'Derrubar todos!'
    assert TEXTS[0x7F1543] == 'Escalar!'
    assert TEXTS[0x7F3223] == 'Curar Pokémon'
    assert 'Fichas' in TEXTS[0x7EC6D1]
    assert '4 000' in TEXTS[0x7EC760]
    assert '2 000' in TEXTS[0x7EC7B0]


def test_finalizer_after_repairs_and_disjoint_from_other_batches():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_28') == 1
    assert steps.index('batch_28') > steps.index('repoint_stale')
    other = json.loads((ROOT / 'languages/pt/data/pt20_audit.json').read_text())
    refs = {p for row in LIVE for p in row['references']}
    assert not refs.intersection(p for row in other['entries'] for p in row['references'])


def test_visual_probe_samples_complete_messages_without_runtime_buffers():
    """Deux messages entiers permettent la vérification OCR dans mGBA."""
    samples = [TEXTS[offset] for offset in (0x7ED7FC, 0x7EE8F6)]
    assert all(text.count('\n') == 1 for text in samples)
    assert all(not re.search(r'<0xF[ABCD]>', text) for text in samples)
    assert 'Lapras' in samples[1]
