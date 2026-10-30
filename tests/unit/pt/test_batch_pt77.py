"""PT-77 : périmètre fermé, pages, commandes, Safari et missions."""
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
AUDIT = json.loads((ROOT / 'languages/pt/data/pt77_audit.json').read_text())
LIVE = [r for r in AUDIT['entries'] if r['status'] != 'exception']
TEXTS, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')


def test_exact_manifest_and_protections():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-77')
    guards = {int(e['offset'], 16): e['expected'] for e in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 300 and len(LIVE) == 298
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['reason']
        if row['status'] == 'exception':
            assert row['offset'] in ('0x1f65e5b', '0x1f6a89d')
            assert not row['references']
            assert offset not in TEXTS and offset not in guards
        else:
            assert TEXTS[offset] == _normalize_text(guards[offset])
            assert guards[offset] == row['portuguese']
            assert row['references']


@pytest.mark.parametrize('row', LIVE, ids=lambda r: r['offset'])
def test_exact_controls_and_layout(row):
    text = TEXTS[int(row['offset'], 16)]
    raw = TextEncoder.encode_pokemon(text, strict=True)
    commands = lambda data: [s for s in _extract_control_sequences_from_raw(data) if s[0] != 0xFE]
    assert commands(raw) == commands(bytes.fromhex(row['source_hex']))
    assert len(raw) == row['encoded_bytes'] and raw[-1] == 255 and 255 not in raw[:-1]
    assert line_widths(text) == row['line_widths']
    assert max(row['line_widths']) <= row['max_width']
    if row['kind'] == 'dialogue':
        parts = re.split(r'(<0xF[AB]>)', text)
        assert all(p.count('\n') <= 1 for p in parts[::2])
        assert all('\n' not in parts[i] for i in range(2, len(parts), 2)
                   if parts[i - 1] == '<0xFA>')
    if row['status'] == 'retained_english':
        assert raw == bytes.fromhex(row['source_hex'])


def test_safari_rules_and_complete_speeches():
    text = {o: t.replace('\n', ' ') for o, t in TEXTS.items()}
    assert all('movimentos' in text[o] for o in (0x1F64A2F, 0x1F64A71))
    assert 'Natureza' in text[0x1F64B99]
    assert 'PS' in text[0x1F64AF4] and 'Figy Berries' in text[0x1F64AF4]
    assert 'Batalha Dupla' in text[0x1F654BD]
    assert 'Flame Body' in text[0x1F65A35] and 'Magma Armor' in text[0x1F65A35]
    assert 'Link Stone' in text[0x1F672ED]
    assert 'Entrar' == text[0x1F687A1]
    assert 'três' in text[0x1F68D0D]
    assert '30' in text[0x1F691C7]
    assert text[0x1F6A078].endswith('Sharpedo<0xFC><0x01><0x08>.')
    assert '20' in text[0x1F6AAD5] and '7' in text[0x1F6AD2C]


def test_finalizer_after_repairs_and_other_batches_disjoint():
    patches = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert patches.count('batch_77') == 1
    assert all(patches.index(p) < patches.index('batch_77') for p in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))
    refs = {p for row in LIVE for p in row['references']}
    for file in (ROOT / 'languages/pt/data').glob('pt*_audit.json'):
        if file.name != 'pt77_audit.json':
            assert not refs.intersection(p for r in json.loads(file.read_text()).get('entries', [])
                                         for p in r.get('references', [])), file
