"""PT-62 : périmètre, commandes, missions, élevage et noms canoniques."""
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
AUDIT = json.loads((ROOT / 'languages/pt/data/pt62_audit.json').read_text())
LIVE = [r for r in AUDIT['entries'] if r['status'] != 'exception']
TEXTS, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')


def test_exact_manifest_and_protection():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-62')
    guards = {int(e['offset'], 16): e['expected'] for e in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 300 and len(LIVE) == 296
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['reason']
        if row['status'] == 'exception':
            assert not row['references'] and row['active_neighbours']
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
    if row['kind'] == 'mission':
        assert 2 <= len(text.splitlines()) <= 3
        assert not re.search(r'<0xF[AB]>', text)
        assert row['max_width'] == 172
    else:
        parts = re.split(r'(<0xF[AB]>)', text)
        assert all(part.count('\n') <= 1 for part in parts[::2])
        for index in range(2, len(parts), 2):
            if parts[index - 1] == '<0xFA>':
                assert '\n' not in parts[index]


def test_breeding_rules_prices_and_dehara_story():
    texts = {o: t.replace('\n', ' ') for o, t in TEXTS.items()}
    assert '100<0xFC>' in texts[0x1EF8835]
    assert 'família evolutiva' in texts[0x1EF8FED]
    assert 'Glalie e Froslass' in texts[0x1EF939F]
    assert 'Snorunt para Vanillite' in texts[0x1EF939F]
    assert 'CERTEZA ABSOLUTA' in texts[0x1EF8C8E]
    assert 'nunca mais verá' in texts[0x1EF8C8E]
    assert 'Move Deleter' in texts[0x1EF94CE] and 'Epidimy Town' in texts[0x1EF94CE]
    assert '2 Yellow Shards' in texts[0x1EFBA81]
    assert 'Thunder Punch' in texts[0x1EFBA81]
    assert 'dias pares' in texts[0x1EFC330]
    assert 'nesse mesmo dia' in texts[0x1EFD5B1]
    assert 'vencendo o Ginásio' in texts[0x1EFBE01]
    assert len(bytes.fromhex(AUDIT['entries'][190]['source_hex'])) == 607
    assert texts[0x1EF9640] == 'Dehara City'
    assert texts[0x1EF9618] == 'Ocupar espaços livres'
    assert texts[0x1EF962D] == 'Apagar movimentos'
    assert 'Terrestre' in texts[0x1EFBD43] and 'Fogo' in texts[0x1EF9716]
    for offset, item, price in [(0x1EFE6CE, 'Fresh Water', 200),
                                (0x1EFE6E4, 'Soda Pop', 300),
                                (0x1EFE6F7, 'Lemonade', 350)]:
        assert texts[offset].startswith(item)
        assert texts[offset].endswith(f'¥{price}')
        assert '<0xFC><0x13><0x54><0xFC><0x06><0x00>' in texts[offset]


def test_finalizer_order_and_other_batch_isolation():
    patches = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert patches.count('batch_62') == 1
    assert all(patches.index(p) < patches.index('batch_62') for p in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))
    refs = {p for row in LIVE for p in row['references']}
    for file in (ROOT / 'languages/pt/data').glob('pt*_audit.json'):
        if file.name == 'pt62_audit.json':
            continue
        other = json.loads(file.read_text())
        assert not refs.intersection(p for r in other.get('entries', [])
                                     for p in r.get('references', [])), file


def test_pcm_match_is_excluded_from_all_text_references():
    row = AUDIT['entries'][256]
    assert row['offset'] == '0x1efdade'
    assert row['references'] == [0x1E641C3]
    assert row['non_text_matches'][0]['site'] == '0xcbb02d'
    assert 0xCBB02D not in {p for r in LIVE for p in r['references']}
    assert sum(len(r['references']) for r in LIVE) == 354
