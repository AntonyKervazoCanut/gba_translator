"""Contrat exhaustif PT-08 : lexique Easy Chat, protections et exceptions."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.apply_combined_fr import _load_combined
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt08_audit.json').read_text())
ROWS = AUDIT['entries']


def test_manifest_and_exceptions() -> None:
    batch = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())[7]
    assert len(ROWS) == len({e['offset'] for e in ROWS}) == 282
    assert {e['offset'] for e in ROWS} == set(batch['offsets'])
    exceptions = {e['offset']: e for e in ROWS if e['status'] == 'exception'}
    assert set(exceptions) == {'0x3eb61b', '0x3eb621'}
    assert exceptions['0x3eb61b']['pointers'] == ['0x3eb82c']
    assert exceptions['0x3eb621']['pointers'] == []
    assert exceptions['0x3eb621']['interior_target'] == '0x3eb622'
    assert all(e['reason'] for e in exceptions.values())


@pytest.mark.parametrize('entry', [e for e in ROWS if e['status'] == 'translated'],
                         ids=lambda e: e['offset'])
def test_words_have_no_controls_and_fit(entry: dict) -> None:
    translations = _load_combined(ROOT / 'languages/pt/combined_pt.txt')[0]
    text = translations[int(entry['offset'], 16)]
    encoded = TextEncoder.encode_pokemon(text, strict=True)
    assert encoded[-1] == 255 and not any(b >= 0xF7 for b in encoded[:-1])
    assert not any(b >= 0xF7 for b in bytes.fromhex(entry['source_hex'])[:-1])
    assert len(encoded) == entry['encoded_bytes']
    assert max(entry['widths'].values()) <= entry['pixel_budget']
    assert len(entry['all_font_widths']) == 5
    assert max(entry['all_font_widths']) <= entry['pixel_budget']
    assert entry['portuguese'] == text
    assert entry['encoded_hex'] == encoded.hex()
    assert len(entry['live_targets']) == len(entry['pointers'])
    assert 10 <= entry['group_index'] <= 16
    assert entry['pointers']


def test_glossary_and_easy_chat_context() -> None:
    pt = _load_combined(ROOT / 'languages/pt/combined_pt.txt')[0]
    assert pt[0x3EB127] == 'SER NOCAUTEADO'  # Subir le K.O., pas le provoquer.
    assert pt[0x3EB12D] == 'NOCAUTEADO'
    assert pt[0x3EC086] == 'CONFUSO'
    assert pt[0x3EB5D4] == 'Festa'  # Quotidien, pas l’équipe Pokémon du menu.
    assert pt[0x3EB866] == 'BRINCADEIRA'
    assert pt[0x3EAB51] == 'PERÍCIA'  # Skill générique, pas Ability.
    assert pt[0x3EBC55] == 'AMANHÃ'
