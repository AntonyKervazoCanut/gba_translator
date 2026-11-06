"""Les dialogues paginés ne partagent pas un plafond implicite de fenêtre ES."""
import importlib

import pytest

from src.core.text_codec import TextEncoder


@pytest.mark.parametrize('max_bytes', [None, 512, 1024])
def test_layout_enforces_only_its_declared_total_byte_budget(max_bytes):
    """Une longue suite de pages reste valide sans budget total explicite."""
    builder_type = importlib.import_module(
        'src.translators.19_build_translated_rom_generic').TranslatedROMBuilder
    builder = builder_type.__new__(builder_type)
    builder.english_texts = None
    text = '<0xFB>'.join(['Uma longa conversa.'] * 30)
    raw = TextEncoder.encode_pokemon(text, strict=True)
    assert len(raw) > 512
    layout = {'max_lines': 2, 'max_width': 192}
    if max_bytes is not None:
        layout['max_bytes'] = max_bytes
    item = {'translation': text, 'english_raw_bytes': raw.hex(),
            'layout': layout, 'encoding': 'pokemon'}

    if max_bytes == 512:
        with pytest.raises(ValueError, match='budget en octets'):
            builder._normalize_translation_item(0x100, item)
    else:
        result = builder._normalize_translation_item(0x100, item)
        assert result['translation'] == text
