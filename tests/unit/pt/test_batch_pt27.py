"""PT-27 : manifeste fermé, commandes de scène, récompenses et protections."""
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
AUDIT = json.loads((ROOT / 'languages/pt/data/pt27_audit.json').read_text())
TEXTS, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
LIVE = [r for r in AUDIT['entries'] if r['status'] == 'translated']


def test_exact_manifest_and_protection():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-27')
    guards = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protected = {int(e['offset'], 16): e['expected'] for e in guards['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 288 and len(LIVE) == 270
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['source_hex']
        if row['status'] == 'exception':
            assert offset not in TEXTS
            if row['references']:
                assert offset in (0x7E97F3, 0x7EA1FB)
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
    parts = re.split(r'(<0xF[AB]>)', text)
    for index in range(0, len(parts), 2):
        assert parts[index]
        assert parts[index].count('\n') <= (0 if index and parts[index - 1] == '<0xFA>' else 1)


def test_story_names_rewards_and_gender_buffers():
    texts = {offset: text.replace('\n', ' ').replace('<0xFA>', ' ') for offset, text in TEXTS.items()}
    assert 'mil' in texts[0x7D61AD].lower() and 'CINDER VOLCANO' in texts[0x7D61AD]
    assert 'Red Orb' in texts[0x7D742F] and 'primordial' in texts[0x7D742F]
    assert 'Operation Eternal Flower' in texts[0x7DDC4C]
    assert 'Ultimate Weapon' in texts[0x7DDC4C]
    assert 'filho' == texts[0x7DE1E1] and 'filha' == texts[0x7DE1E5]
    assert 'nome de tal' in texts[0x7DD149]
    assert 'um bebê:' in texts[0x7DD149]  # Également correct avec le tampon « filha ».
    assert '¥10000' in texts[0x7E7F5D] and 'Rare Bone' in texts[0x7E7FE2]
    assert 'Thunder Punch' in texts[0x7E7A5C] and 'Yellow Shard' in texts[0x7E7A5C]
    assert 'SES Expressway' in texts[0x7E8EF5]
    assert all(name in texts[0x7E6816] for name in ('Snivy', 'Tepig', 'Oshawott'))
    assert 'quanto ele!' in texts[0x7E9D68] and 'quanto ela!' in texts[0x7EA26A]
    assert 'TM98' in texts[0x7EA1EB] and 'Bicycle' in texts[0x7EA030]
    assert all(TEXTS[o] == t for o, t in zip((0x7D8F91, 0x7D8F94, 0x7D8F98, 0x7D8F9C), ('T', 'S1', 'S2', 'S3')))
    for offset in (0x7DE4DA, 0x7E6B89, 0x7E6D12):
        source = bytes.fromhex(next(r['source_hex'] for r in LIVE if int(r['offset'], 16) == offset))
        encoded = TextEncoder.encode_pokemon(TEXTS[offset], strict=True)
        assert [b for b in encoded if 0x79 <= b <= 0x7C] == [b for b in source if 0x79 <= b <= 0x7C]


def test_finalizer_follows_repairs_and_references_are_disjoint():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_27') == 1 and steps.index('batch_27') > steps.index('repoint_stale')
    refs = {p for row in LIVE for p in row['references']}
    for path in (ROOT / 'languages/pt/data').glob('pt*_audit.json'):
        if path.name == 'pt27_audit.json':
            continue
        other = json.loads(path.read_text())
        assert not refs.intersection(p for r in other.get('entries', []) for p in r.get('references', [])), path.name
