"""Régression #219 : la découverte d'une CT conserve ses deux lignes."""
from pathlib import Path

from languages.fr import dedicated_patch_offsets
from languages.fr.patches import meteorite_dialogue
from src.core.dialogue_linewrap import line_width
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
OFFSET = 0x1A63E8
EXPECTED = r"{PLAYER} a trouvé la {STR_VAR_2} !\nElle contient {STR_VAR_1}."


def test_tm_pickup_has_curated_layout() -> None:
    """La source exacte et les deux passes respectent la mise en page dédiée."""
    combined = meteorite_dialogue.load_combined(ROOT / 'languages/fr/combined_fr.txt')

    assert combined[OFFSET] == EXPECTED
    assert OFFSET in dedicated_patch_offsets.GENERIC_TRANSLATION_OFFSETS
    assert OFFSET in dedicated_patch_offsets.INLINE_OVERRIDE_OFFSETS
    assert OFFSET in meteorite_dialogue.LAYOUT_TARGETS


def test_tm_pickup_expanded_lines_fit() -> None:
    """Même un nom joueur long tient avec le numéro et la capacité de CT54."""
    lines = EXPECTED.replace('{PLAYER}', 'WWWWWWWWW').replace(
        '{STR_VAR_2}', 'CT54'
    ).replace('{STR_VAR_1}', 'Faux-Chage').split(r'\n')

    assert len(lines) == 2
    assert all(line_width(line) <= 192 for line in lines)


def test_tm_pickup_preserves_native_buffers_and_newline() -> None:
    """Le codec conserve les variables natives et le retour avant la capacité."""
    source = (ROOT / 'tests/unit/fixtures/tm_pickup.bin').read_bytes()

    encoded = meteorite_dialogue.encode_relocated(EXPECTED, source, 0)

    expected = TextEncoder.encode_pokemon(
        "<0xFD><0x01> a trouvé la <0xFD><0x03> !\nElle contient <0xFD><0x02>."
    )
    assert encoded == expected
    assert encoded.count(b'\xfe') == 1
    assert encoded.endswith(b'\xff')
