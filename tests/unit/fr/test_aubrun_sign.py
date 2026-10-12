"""Régression du panneau à flèche du Chenal Aubrun (#220)."""

from languages.fr.patches.worldmap_junction_panels import (
    DEFAULT_COMBINED,
    TARGETS,
    encode_relocated,
    load_combined,
)


def test_aubrun_sign_is_owned_by_pokemon_encoded_junction_patch():
    # Arrange : texte existant, dont la flèche initiale était prise pour ASCII.
    offset = 0x1F7128C
    combined = load_combined(DEFAULT_COMBINED)
    # Act
    encoded = encode_relocated(combined[offset], b"", offset)
    # Assert : le pipeline générique doit laisser ce panneau au patch dédié.
    assert offset in TARGETS
    assert encoded == bytes.fromhex("7900bddcd9e2d5e000bbe9d6e6e9e2ff")


def test_delivered_bps_contains_pokemon_encoded_aubrun_sign():
    """Le correctif doit atteindre le bundle livré, pas seulement le build."""
    import struct
    from pathlib import Path

    from src.core.release_stamp import _KnownTarget, _parse

    # Arrange : pointeur vivant du script du panneau dans le patch livré.
    root = Path(__file__).resolve().parents[3]
    target = _KnownTarget(_parse((root / "patches/pokemon_unbound_fr.bps").read_bytes()), ())
    # Act
    offset = struct.unpack("<I", target.read(0x1E931EA, 4))[0] - 0x08000000
    actual = target.read(offset, 15)
    # Assert : flèche et texte Pokémon ; le terminateur est vérifié en E2E.
    assert actual == bytes.fromhex("7900bddcd9e2d5e000bbe9d6e6e9e2")
