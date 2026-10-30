"""PT-48 : sources réelles, couverture exacte et sens des descriptions d'objets."""
import json
from pathlib import Path

import yaml

from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt48_audit.json').read_text())


def test_exact_manifest_protection_and_layout():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-48')
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    live = entries()
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 282
    assert sum(r['status'] == 'translated' for r in AUDIT['entries']) == 137
    assert sum(r['status'] == 'retained_english' for r in AUDIT['entries']) == 36
    for row in AUDIT['entries']:
        assert row['reason']
        if row['status'] == 'exception':
            assert int(row['offset'], 16) not in live
            continue
        text = row['portuguese']
        assert live[int(row['offset'], 16)] == guards[int(row['offset'], 16)] == text
        raw = TextEncoder.encode_pokemon(text.replace(r'\n', '\n'), strict=True)
        assert len(raw) == row['encoded_bytes']
        assert line_widths(text.replace(r'\n', '\n')) == row['line_widths']
        assert max(row['line_widths']) <= 192
        assert _extract_control_sequences_from_raw(raw) == _extract_control_sequences_from_raw(
            bytes.fromhex(row['source_hex']))
        assert row['references']
        if row['status'] == 'retained_english':
            assert text == row['english_rom']
        else:
            assert all((p - 0x876088) % 44 == 0 for p in row['references'])
            assert len(row['line_widths']) <= 3


def test_item_effects_and_glossary_are_not_stale_french():
    texts = entries()
    for offset, stat in [(0xEB23F0, 'Ataque'), (0xEB244C, 'Defesa'),
                         (0xEB24A9, 'Velocidade'), (0xEB2504, 'Ataque Especial'),
                         (0xEB2561, 'Defesa Especial'), (0xEB25BE, 'Precisão')]:
        assert stat in texts[offset]
        assert 'retirado' in texts[offset]
        assert 'base' not in texts[offset]
    assert 'geluras' in texts[0xEB23B6]
    assert '1/4 dos PS' in texts[0xEB2D73]
    assert 'Habilidade Oculta' in texts[0xEB267C]
    assert 'KBT' in texts[0xEB1CB6] and '<0xF8>Â' in texts[0xEB1CB6]
    assert 'Professor Log' in texts[0xEB20E8]
    assert 'Natural Gift' in texts[0xEB3083]
    assert 'atacante sai' in texts[0xEB4374]
    assert 'portador sai' in texts[0xEB3F98]
    assert 'Dragão e Fantasma' in texts[0xEB487E]
