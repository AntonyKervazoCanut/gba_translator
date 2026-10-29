"""Les quatre tildes PT ont des slots exclusifs, sans translittération."""
from src.core.text_codec import POKEMON_TABLE, TextDecoder, TextEncoder
from src.text.charmap_data import BYTE_TO_CHAR, CHAR_TO_BYTE, CONTROL_CODES


def test_tildes_round_trip_and_unique_slots():
    expected = {'ã': 0x60, 'õ': 0x61, 'Ã': 0x62, 'Õ': 0x63}
    for char, slot in expected.items():
        assert POKEMON_TABLE.get(char) == slot
        assert CHAR_TO_BYTE[char] == slot
        assert BYTE_TO_CHAR[slot] == char
        assert [c for c, b in CHAR_TO_BYTE.items() if b == slot] == [char]
        assert slot not in CONTROL_CODES and slot < 0xF1
        assert TextEncoder.encode_pokemon(char) == bytes([slot, 0xFF])
        assert TextDecoder.decode_pokemon(bytes([slot, 0xFF])) == char


def test_secondary_italian_charmap_has_no_stale_german_slots():
    from languages.it.patches.pokedex_categories import CHAR_TO_BYTE as secondary
    for char in 'ãõÃÕÄÖÜäöü':
        assert secondary[char] == CHAR_TO_BYTE[char]


def test_all_portuguese_accents_and_widths():
    from src.core.dialogue_linewrap import GLYPH_WIDTHS
    for char in 'ãõâêôáéíóúàçÃÕÂÊÔÁÉÍÓÚÀÇ':
        encoded = TextEncoder.encode_pokemon(char)
        assert encoded == bytes([CHAR_TO_BYTE[char], 0xFF])
        assert TextDecoder.decode_pokemon(encoded) == char
    for accented, base in zip('ãõÃÕ', 'aoAO'):
        assert GLYPH_WIDTHS[CHAR_TO_BYTE[accented]] == GLYPH_WIDTHS[CHAR_TO_BYTE[base]]


def test_control_arguments_are_not_reinterpreted_as_tildes():
    # FC 13 63 = CLEAR_TO x=99, pas le glyphe Õ.
    assert TextEncoder.encode_pokemon('<0xFC><0x13><0x63>') == bytes([0xFC, 0x13, 0x63, 0xFF])


def test_pokedex_consumer_accepts_portuguese_tildes():
    from src.core.pokedex import is_description
    assert is_description('Um Pokémon com ação. Ã Õ ã õ.')


def test_tildes_surrounding_a_position_control_keep_their_order():
    encoded = TextEncoder.encode_pokemon('ã<0xFC><0x13><0x63>õ')
    assert encoded == bytes([0x60, 0xFC, 0x13, 0x63, 0x61, 0xFF])
