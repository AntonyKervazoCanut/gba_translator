"""PT-67 : périmètre fermé, règles des Ginásios, tampons et tablettes."""
import json
import re
from pathlib import Path

import pytest
import yaml

from scripts.apply_combined_fr import _load_combined
from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt67_audit.json').read_text())
LIVE = [r for r in AUDIT['entries'] if r['status'] != 'exception']
TEXTS, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')


def test_exact_manifest_and_protection():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-67')
    guards = {int(e['offset'], 16): e['expected'] for e in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 300 and len(LIVE) == 298
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['reason']
        if row['status'] == 'exception':
            assert not row['references'] and row['owner_references']
            assert int(row['owner_offset'], 16) == offset + 1
            assert offset not in TEXTS and offset not in guards
        else:
            assert TEXTS[offset] == guards[offset].replace(r'\n', '\n')
            assert guards[offset] == row['portuguese']
            assert row['references']


@pytest.mark.parametrize('row', LIVE, ids=lambda r: r['offset'])
def test_commands_pages_and_pixel_budgets(row):
    text = TEXTS[int(row['offset'], 16)]
    raw = TextEncoder.encode_pokemon(text, strict=True)
    source = bytes.fromhex(row['source_hex'])
    def commands(data):
        return [s for s in _extract_control_sequences_from_raw(data) if s[0] != 0xFE]
    assert commands(raw) == commands(source)
    assert len(raw) == row['encoded_bytes']
    assert raw[-1] == 255 and 255 not in raw[:-1]
    assert line_widths(text) == row['line_widths']
    assert max(row['line_widths']) <= row['max_width']
    if row['status'] == 'retained_english':
        assert raw == source
    if row['kind'] in ('dialogue', 'gym_sign'):
        parts = re.split(r'(<0xF[AB]>)', text)
        assert all(part.count('\n') <= 1 for part in parts[::2])
        assert all('\n' not in parts[i] for i in range(2, len(parts), 2)
                   if parts[i - 1] == '<0xFA>')
    if row['kind'] == 'mission':
        assert len(text.splitlines()) <= 3 and row['max_width'] == 172


def test_gym_rules_story_and_canonical_names():
    texts = {o: t.replace('\n', ' ') for o, t in TEXTS.items()}
    assert 'Spikes' in texts[0x1F1A75B]
    assert 'Toucannon' in texts[0x1F1AB71] and 'Alakazam' in texts[0x1F1AB71]
    assert '100<0xFC>' in texts[0x1F1B45C]
    assert 'peso' in texts[0x1F1B67A] and 'Habilidades' in texts[0x1F1B67A]
    assert 'Magic Guard' in texts[0x1F1C3FC] and 'Oblivious' in texts[0x1F1C3FC]
    assert 'Electric Terrain' in texts[0x1F1D819]
    assert 'dois primeiros' in texts[0x1F1E1A5]
    assert 'não ganham' in texts[0x1F1E688] and 'Exp.' in texts[0x1F1E688]
    assert 'nocauteado como Caterpie' in texts[0x1F1E688]
    assert '6 Full Restores, 5 Revives' in texts[0x1F20544]
    assert '6 Max Elixirs' in texts[0x1F20544]
    assert 'Safety' in texts[0x1F20AD0] and 'Goggles' in texts[0x1F20AD0]
    assert 'Rattata' in texts[0x1F229D5] and 'Ratatta' not in texts[0x1F229D5]
    assert 'Chesto' in texts[0x1F20CF2] and 'Berries' in texts[0x1F20CF2]
    assert '50%' not in texts[0x1F21124] and 'metade' in texts[0x1F21124]
    assert texts[0x1F1F844] == 'Icicle Cave'
    assert texts[0x1F21738] == 'Icy Hole'
    assert texts[0x1F21C80] == 'KBT Expressway'
    assert texts[0x1F21ADC] == 'Ovos:<0x00>'
    assert texts[0x1F20F14] == 'envenenados'
    assert texts[0x1F20F25] == 'adormecidos'
    assert 'B1F' in texts[0x1F202AE] and 'Route 6' in texts[0x1F202AE]
    assert 'vermelho, amarelo e azul' in texts[0x1F203EB]
    buffers = AUDIT['entries'][150]['context_buffers']
    assert [b['portuguese'] for b in buffers] == ['está', 'estava']


def test_finalizer_order_and_other_batch_isolation():
    patches = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert patches.count('batch_67') == 1
    assert all(patches.index(p) < patches.index('batch_67') for p in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))
    refs = {p for row in LIVE for p in row['references']}
    for file in (ROOT / 'languages/pt/data').glob('pt*_audit.json'):
        if file.name != 'pt67_audit.json':
            assert not refs.intersection(p for r in json.loads(file.read_text()).get('entries', [])
                                         for p in r.get('references', [])), file
    assert sum(len(r['non_text_matches']) for r in LIVE) == 6
