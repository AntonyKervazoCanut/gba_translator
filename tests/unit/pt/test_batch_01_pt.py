"""Contrat PT-01 : couverture, variables et pagination des dialogues."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from src.core.dialogue_linewrap import line_widths
from src.core.fixed_tables import in_fixed_table
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
BATCH = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())[0]
OFFSETS = {int(o, 16) for o in BATCH['offsets']}
EXCEPTIONS = {
    0x1737AF, 0x1762D7, 0x176FBD, 0x179396, 0x17FF49, 0x180AF3,
    0x183387, 0x188111, 0x18D43D, 0x18EA44, 0x18EA65, 0x18EBE5, 0x18ED80,
    0x1904EE, 0x196591,
}


def load_entries(path: Path) -> dict[int, str]:
    """Résout les dernières occurrences sans réécrire les sources."""
    result = {}
    for line in path.read_text().splitlines():
        match = re.match(r'0x([\da-fA-F]+):\s?(.*)', line)
        if match:
            result[int(match[1], 16)] = match[2].replace('\\n', '\n')
    return result


PT = load_entries(ROOT / 'languages/pt/combined_pt.txt')
EN = load_entries(ROOT / 'languages/en/combined_en.txt')


def encode(text: str) -> bytes:
    return TextEncoder.encode_pokemon(text, strict=True)


def controls(raw: bytes) -> list[bytes]:
    # PT-01 n'emploie que FD xx et FC 01 xx (couleur).
    return re.findall(rb'\xfd.|\xfc\x01.|[\xfa\xfb]', raw)


def test_exact_batch_coverage() -> None:
    assert len(OFFSETS) == 277
    assert OFFSETS & PT.keys() == OFFSETS - EXCEPTIONS
    assert EXCEPTIONS.isdisjoint(PT)


@pytest.mark.parametrize('offset', sorted(OFFSETS - EXCEPTIONS), ids=hex)
def test_dialogue_structure_and_width(offset: int) -> None:
    # Ne pas appliquer les alias typographiques aux paramètres du corpus EN.
    source = TextEncoder.encode_pokemon(
        EN[offset], skip_aliases=frozenset(TextEncoder.POKEMON_TABLE), strict=True,
    )
    translated = encode(PT[offset])
    assert controls(translated) == controls(source)
    assert translated[-1] == 0xFF and 0xFF not in translated[:-1]
    text = PT[offset]
    if offset == 0x17CC56:
        # Chronomètre : minutes (3 chiffres), secondes (2), centièmes (2).
        text = text.replace('<0xFD><0x02>', '999').replace(
            '<0xFD><0x03>', '59').replace('<0xFD><0x04>', '99')
    assert max(line_widths(text), default=0) <= 192


def test_official_terms_and_unbound_names() -> None:
    assert 'PS' in PT[0x195BBA] and 'Ataque' in PT[0x195CA0]
    assert 'Poção' in PT[0x190365]
    assert 'Dehara Department Store' in PT[0x17FF4A]
    assert 'The Ruins of Void' in PT[0x187A50]
    assert 'Mirskle' in PT[0x192079]
    assert 'Old Rod' in PT[0x193F81]
    assert 'Coin Case' in PT[0x1969FB]


def test_audit_covers_the_exact_batch_and_excludes_fixed_tables() -> None:
    audit = json.loads((ROOT / 'languages/pt/data/pt01_audit.json').read_text())
    entries = audit['entries']
    assert {int(e['offset'], 16) for e in entries} == OFFSETS
    assert len(entries) == 277
    assert {int(e['offset'], 16) for e in entries if e['status'] == 'exception'} == EXCEPTIONS
    assert sum(len(e['pointers']) for e in entries) == 420
    assert not any(in_fixed_table(offset) for offset in OFFSETS)
    for entry in entries:
        if entry['status'] == 'exception':
            assert entry['reason'] and not entry['pointers']
        else:
            assert entry['pointers']
