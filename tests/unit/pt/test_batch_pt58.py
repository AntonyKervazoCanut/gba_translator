"""PT-58 : périmètre, cellules Pokédex, glossaire et pages d'Antisis."""
import json
from pathlib import Path

import yaml

from scripts.apply_combined_fr import _load_combined
from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt58_audit.json').read_text())


def test_manifest_protections_commands_and_budgets():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-58')
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 300
    assert sum(r['kind'] == 'category' for r in AUDIT['entries']) == 113
    assert sum(r['kind'] == 'dialogue' for r in AUDIT['entries']) == 126
    assert sum(r['status'] == 'exception' for r in AUDIT['entries']) == 61
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        assert row['reason'] and row['source_hex']
        if row['status'] == 'exception':
            assert not row['references'] and off not in texts and row['context_hex']
            continue
        assert texts[off] == guards[off].replace(r'\n', '\n') == row['portuguese'].replace(r'\n', '\n')
        text = texts[off].replace(r'\n', '\n')
        raw = TextEncoder.encode_pokemon(text, strict=True)
        assert raw[-1] == 255 and 255 not in raw[:-1]
        assert len(raw) == row['encoded_bytes']
        assert line_widths(text) == row['line_widths']
        assert max(row['line_widths']) <= row['max_width']
        if row['kind'] == 'category':
            assert len(raw) <= 12
            assert (int(row['consumer_offset'], 16) - 0x1A357CC) % 36 == 0
        else:
            commands = lambda b: [s for s in _extract_control_sequences_from_raw(b) if s[0] != 254]
            assert commands(raw) == commands(bytes.fromhex(row['source_hex']))


def test_antisis_mechanics_and_untruncated_dialogue():
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    assert 'Big Mo entra e assume o comando.' in texts[0x1EDDA75]
    assert 'segurando um item' in texts[0x1EDD9D2]
    assert 'não aprendeu' in texts[0x1EDD58B]
    assert 'não está neste motor' in texts[0x1EDD5BC]
    assert 'de confiança' in texts[0x1EDE32C]
    assert 'dez Poké Balls' in texts[0x1EDE4B9]
    for offset, name in [(0x1EDCD8C, 'Antisis City'), (0x1EDCDB7, 'Antisis Port'),
                         (0x1EDEFF4, 'Antisis Sewers')]:
        assert texts[offset] == name
    assert 'Whirlipede' in texts[0x1EDF45A] and 'Gloom' in texts[0x1EDF6A7]


def test_finalizer_order():
    patches = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert patches.count('batch_58') == 1
    assert all(patches.index(step) < patches.index('batch_58') for step in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))
