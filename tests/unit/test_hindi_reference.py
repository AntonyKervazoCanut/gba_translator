"""Vérifie le référentiel HI sans masquer une perte par le fallback du codec."""

import json
import re
from pathlib import Path

import pytest

from src.core.text_codec import TextEncoder

REFERENCE = json.loads(
    (Path(__file__).resolve().parents[2] / 'languages/indie/data/glossary_v1.json')
    .read_text(encoding='utf-8')
)
ENTRIES = REFERENCE['entries']
EXAMPLES = REFERENCE['examples']
ALPHABET = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,!?'-():/\n")


def test_reference_is_versioned_and_covers_all_domains() -> None:
    """Les lots partagent une convention identifiée et les neuf domaines requis."""
    assert REFERENCE['version'] == '1.1.0'
    assert REFERENCE['convention'] == 'HI-LATIN-1'
    assert {entry['domain'] for entry in ENTRIES} == {
        'types', 'statuts', 'statistiques', 'menus', 'combat', 'objets',
        'attaques', 'talents', 'narration',
    }
    keys = [(entry['domain'], entry['en']) for entry in ENTRIES]
    assert len(keys) == len(set(keys))
    assert len([entry for entry in ENTRIES if entry['domain'] == 'types']) == 18


@pytest.mark.parametrize('entry', ENTRIES, ids=lambda e: f"{e['domain']}/{e['en']}")
def test_terms_have_provenance_and_encode_exactly(entry: dict) -> None:
    """Chaque forme est traçable et produit ses octets sans alias ni fallback."""
    assert entry['source'] in REFERENCE['sources']
    assert entry['status'] in {'editorial-hi', 'editorial-retained-en'}
    for field in ('hi', 'short'):
        value = entry[field]
        assert value and value == value.strip()
        assert set(value) <= ALPHABET
        expected = bytes(TextEncoder.POKEMON_TABLE[char] for char in value) + b'\xff'
        assert TextEncoder.encode_pokemon(value) == expected


@pytest.mark.parametrize('example', EXAMPLES, ids=lambda e: e['en'])
def test_examples_keep_controls_and_fit_declared_budgets(example: dict) -> None:
    """Mesure aussi les séquences FD et FE, pas la longueur des tokens écrits."""
    text = example['hi']
    chunks = re.split(r'(<0x[0-9A-F]{2}>)', text)
    expected = bytearray()
    for chunk in chunks:
        if re.fullmatch(r'<0x[0-9A-F]{2}>', chunk):
            expected.append(int(chunk[3:5], 16))
        else:
            assert set(chunk) <= ALPHABET
            for char in chunk:
                expected.append(0xFE if char == '\n' else TextEncoder.POKEMON_TABLE[char])
    expected.append(0xFF)

    encoded = TextEncoder.encode_pokemon(text)

    assert encoded == bytes(expected)
    assert len(encoded) <= example['max_bytes']
    controls = re.findall(rb'\xfd[\x00-\xff]', encoded)
    assert [value.hex().upper() for value in controls] == example.get('controls', [])


def test_reference_does_not_claim_official_hindi_equivalents() -> None:
    """Une source officielle EN ne transforme pas une décision HI en terme officiel."""
    assert all(entry['status'].startswith('editorial-') for entry in ENTRIES)
    for source in REFERENCE['sources'].values():
        assert source['scope']
        assert source.get('url', '').startswith('https://') or source.get('path')
