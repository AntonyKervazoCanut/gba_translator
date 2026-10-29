"""PT-03 : structure, budgets et couverture du manifeste explicite."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from scripts.apply_combined_fr import _load_combined
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt03_audit.json').read_text())
ENTRIES = AUDIT['entries']
PT, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')


def controls(raw: bytes) -> list[bytes]:
    """Reconnaît les commandes réellement rencontrées dans ce lot."""
    return re.findall(rb'\xfd.|\xfc\x13.|\xfc\x06.|\xfc\x09|[\xfa\xfb]', raw)


def test_exact_manifest_and_exception_justifications() -> None:
    batch = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())[2]
    assert len(ENTRIES) == len(batch['offsets']) == 277
    assert {e['offset'] for e in ENTRIES} == set(batch['offsets'])
    for entry in ENTRIES:
        if entry['status'] == 'exception':
            assert entry['reason'] and not entry['pointers']
            assert int(entry['offset'], 16) not in PT
        else:
            assert entry['pointers'] or entry.get('table_pointers')


@pytest.mark.parametrize('entry', [e for e in ENTRIES if 'pt_bytes' in e], ids=lambda e: e['offset'])
def test_encoded_controls_and_pixel_budgets(entry: dict) -> None:
    offset = int(entry['offset'], 16)
    text = PT[offset]
    encoded = TextEncoder.encode_pokemon(text, strict=True)
    source = bytes.fromhex(entry['source_hex'])
    assert controls(encoded) == controls(source)
    assert encoded[-1] == 0xFF and 0xFF not in encoded[:-1]
    assert len(encoded) == entry['pt_bytes']
    limit = 122 if 0x236632 <= offset <= 0x237253 else 192
    assert max(line_widths(text), default=0) <= limit
    if 'cell_bytes' in entry:
        assert len(encoded) <= entry['cell_bytes']
        assert max(line_widths(text), default=0) <= 80
    if 0x236632 <= offset <= 0x237253:
        assert len(text.split('\n')) <= 3
    if offset == 0x1C5AEB:
        assert '\n\n' in text


def test_frozen_terms_and_complete_names() -> None:
    assert 'Strength' in PT[0x1BE1FA]
    assert 'Rock Smash' in PT[0x1BE09D]
    assert PT[0x238D6A] == 'Cancelar'
    assert 'Centro Pokémon' in PT[0x1C0EF7]
    assert 'movimentos Aço' in PT[0x236EEA]
    assert PT[0x23E705] == 'Dragon Tamer'  # Pas de troncature en cellule de 13 octets.
    assert PT[0x23E7A1] == 'Black Emboar'


def test_intro_does_not_consume_the_adjacent_fragment() -> None:
    assert len(TextEncoder.encode_pokemon(PT[0x1C59D5], strict=True)) <= 0x1C59F7 - 0x1C59D5
