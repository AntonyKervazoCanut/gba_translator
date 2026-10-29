"""Guard all live Hindi entries, including control bytes and literal questions."""
import pytest

from scripts.check_indie_encoding import COMBINED, validate_text
from scripts.check_translation_integrity import load_last_wins


def test_all_live_indie_entries_are_encodable():
    entries, _ = load_last_wins(COMBINED)
    assert entries
    for offset, text in entries.items():
        try:
            validate_text(text)
        except ValueError as exc:
            pytest.fail(f'0x{offset:X}: {exc}')


@pytest.mark.parametrize('text', ['Kya? <0xAC> {FDAC} {PLAYER}\\nHaan?', '？', '¿'])
def test_literal_questions_and_control_bytes_are_not_fallbacks(text):
    validate_text(text)


@pytest.mark.parametrize('text', ['? अ', '<0xAC> अ', '{FDAC} अ', '{PLAYER?}', '{ख}'])
def test_unencodable_characters_and_malformed_tokens_fail(text):
    with pytest.raises(ValueError):
        validate_text(text)
