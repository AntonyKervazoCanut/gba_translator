"""Preuve locale : les patchs publiés affichent leur numéro sur la vraie ROM."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.verify_version_display import decode_version_string, verify
from src.core.bps import apply_bps_patch, create_bps_patch
from src.core.release_stamp import PINNED_SOURCE_FREE_RANGES, stamp_release_bundle

pytestmark = pytest.mark.rom

ROOT = Path(__file__).resolve().parents[1]
EN_ROM = ROOT / "input" / "roms" / "englishrom.gba"


@pytest.fixture(scope="module")
def source() -> bytes:
    if not EN_ROM.exists():
        pytest.skip("ROM anglaise locale absente")
    payload = EN_ROM.read_bytes()
    manifest = json.loads((ROOT / "patches/RELEASE_MANIFEST.json").read_text("utf-8"))
    if hashlib.sha256(payload).hexdigest() != manifest["languages"][0]["source"]["sha256"]:
        pytest.skip("ROM anglaise locale différente de la source épinglée")
    return payload


def test_pinned_free_ranges_are_blank_in_the_source(source: bytes) -> None:
    sha = hashlib.sha256(source).hexdigest()

    for start, end in PINNED_SOURCE_FREE_RANGES[sha]:
        assert source[start:end] == b"\xFF" * (end - start)


def test_published_patches_display_the_publication_number(source, tmp_path) -> None:
    manifest = stamp_release_bundle(ROOT / "patches", 156, "v2.1.156", tmp_path)

    for entry in manifest["languages"]:
        code = entry["code"]
        stamped = (tmp_path / entry["patch"]).read_bytes()
        base = apply_bps_patch(source, (ROOT / f"patches/pokemon_unbound_{code}.bps").read_bytes())
        rom = apply_bps_patch(source, stamped)

        assert decode_version_string(rom) == entry["version_label"]
        assert verify(rom, 156, code) == []
        assert create_bps_patch(source, rom) == stamped
        assert entry["stamped_from"]["target_sha256"] == hashlib.sha256(base).hexdigest()
