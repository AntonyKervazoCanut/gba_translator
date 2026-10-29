"""PT-07 : lexique Easy Chat fermé, mots combinables et budgets de cellule."""
import json
import re
from pathlib import Path

import yaml

from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]


def batch_offsets():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    return {int(x, 16) for b in batches if b['id'] == 'PT-07' for x in b['offsets']}


def translations():
    return {int(m[1], 16): m[2]
            for line in (ROOT / 'languages/pt/combined_pt.txt').read_text().splitlines()
            if (m := re.match(r'(0x[0-9a-f]+): (.*)', line))
            and int(m[1], 16) in batch_offsets()}


def test_closed_batch_and_exact_protections():
    actual = translations()
    protected = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    expected = {int(e['offset'], 16): e['expected'] for e in protected['entries']}
    assert len(actual) == len(batch_offsets()) == 281
    assert actual.keys() == batch_offsets()
    assert all(expected[x] == text for x, text in actual.items())


def test_words_are_encodable_without_controls_or_page_breaks():
    for offset, text in translations().items():
        raw = TextEncoder.encode_pokemon(text, strict=True)
        assert text == text.upper(), hex(offset)
        assert raw[-1] == 0xFF
        assert not set(raw[:-1]) & set(range(0xF7, 0x100)), (hex(offset), text)
        # Le mot anglais le plus long fait 12 glyphes. Garder cette enveloppe
        # conservatrice pour les colonnes du sélecteur, sans couper de mot.
        assert len(raw) <= 13, (hex(offset), text)


def test_persons_and_grammar_keep_the_english_meaning():
    actual = translations()
    assert actual[0x3E92D2] == 'FILHA'  # daughter, pas filleule (FR)
    assert actual[0x3EAA90] == 'PERTO'  # adjectif Close, pas bouton Fermer (FR)
    assert actual[0x3E9258] == 'MÃE' and actual[0x3E9282] == 'IRMÃO'
    assert actual[0x3E9251] == 'VOCÊ TEM' and actual[0x3E924A] == 'VOCÊ É'
    assert actual[0x3EA56D] == 'PENSAR' and actual[0x3EA573] == 'OUVIR'
    assert actual[0x3EA617] == 'CURTIR' and actual[0x3EA61D] == 'CURTE'
    assert actual[0x3EA587] == 'NÃO GOSTAR' and actual[0x3EA5E3] == 'NÃO GOSTA'
