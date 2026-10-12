"""Garde les dialogues de Rivapolis neutres et correctement paginés (#207)."""
import re
from pathlib import Path

import pytest

from src.core.dialogue_linewrap import line_width, rewrap

SOURCE = Path(__file__).resolve().parents[1] / 'languages/fr/combined_fr.txt'


@pytest.mark.parametrize('offset', [0x1F9C8B7, 0x7C5F15, 0x1F9C948])
def test_rivapolis_dialogue_has_no_gender_buffer(offset):
    texts = {}
    for line in SOURCE.read_text().splitlines():
        match = re.match(r'^0x([0-9a-fA-F]+): (.*)$', line)
        if match:
            texts[int(match[1], 16)] = match[2]
    text = texts[offset]
    assert '{STR_VAR_' not in text
    assert '<0xFD>' not in text
    assert 'dame' not in text
    if offset == 0x1F9C948:
        assert text == r'Merci !\pElle ressemble à une\n{COLOR}ÉBaigneuse{COLOR}Ç ordinaire.'
    else:
        assert text.endswith(r"\pS'il te plaît, retrouve-la !")
    for page in text.split(r'\p'):
        assert page.strip().endswith(('!', '.', '…')) or r'\n' in page
    wrapped = rewrap(text.replace(r'\n', '\n').replace(r'\p', '<0xFB>'))
    for line in re.split(r'\n|<0xF[AB]>', wrapped):
        plain = re.sub(r'\{COLOR\}.|<0xFC><0x01><0x[0-9A-F]{2}>', '', line)
        assert line_width(plain) <= 192
