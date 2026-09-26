"""Inscription du numéro de publication dans les patchs BPS, sans ROM."""

from __future__ import annotations

import hashlib
import json
import random
import shutil
import zlib
from pathlib import Path

import pytest

from languages.fr.patches.version import (
    _NFS_TILESET_PTR_OFF,
    _blit_band_to_tiles,
    _compute_checksum,
    _lz77_compress,
    _read_gba_ptr,
    _render_version_band,
    patch_version,
)
from scripts.verify_version_display import decode_version_string
from src.core import release_stamp
from src.core.bps import apply_bps_patch, create_bps_patch
from src.core.patch_bundle import PatchBundle
from src.core.release_stamp import (
    ReleaseStampError,
    release_version_label,
    stamp_bps_version,
    stamp_release_bundle,
)

ROOT = Path(__file__).resolve().parents[2]
FREE_START = 0xF0000
ROM_SIZE = 0x100000


TILESET = bytes(range(256)) * 30


def _synthetic_source() -> bytes:
    """ROM factice : octets non libres, en-tête GBA et zone 0xFF finale."""
    rng = random.Random(0)
    rom = bytearray(rng.randrange(0, 0xFF) for _ in range(ROM_SIZE))
    rom[FREE_START:] = b"\xFF" * (ROM_SIZE - FREE_START)
    rom[0xB2] = 0x96
    rom[0xBC] = 0x00
    rom[0xBD] = _compute_checksum(rom)
    # Comme dans la ROM anglaise, le pointeur d'origine ne partage aucun octet
    # avec celui que le build écrit vers la zone libre.
    rom[_NFS_TILESET_PTR_OFF:_NFS_TILESET_PTR_OFF + 4] = bytes((0x11, 0x22, 0x33, 0x44))
    return bytes(rom)


def _built_target(source: bytes, build_number: int = 44) -> bytes:
    """Reproduit l'étape ``version`` du build : en-tête et tileset en zone libre."""
    target = bytearray(source)
    patch_version(target, build_number)
    tileset = bytearray(TILESET)
    _blit_band_to_tiles(tileset, _render_version_band(f"FR.2.1.{build_number}"))
    stream = _lz77_compress(bytes(tileset))
    target[FREE_START:FREE_START + len(stream)] = stream
    target[_NFS_TILESET_PTR_OFF:_NFS_TILESET_PTR_OFF + 4] = (
        0x08000000 + FREE_START
    ).to_bytes(4, "little")
    return bytes(target)


@pytest.fixture()
def synthetic(monkeypatch):
    source = _synthetic_source()
    sha = hashlib.sha256(source).hexdigest()
    monkeypatch.setitem(
        release_stamp.PINNED_SOURCE_FREE_RANGES, sha, ((FREE_START, ROM_SIZE),)
    )
    target = _built_target(source)
    return source, sha, target, create_bps_patch(source, target)


def test_stamped_patch_displays_the_publication_number(synthetic) -> None:
    """Sans réécriture, la ROM afficherait toujours le build local 44."""
    source, sha, target, patch = synthetic
    assert decode_version_string(target) == "FR.2.1.44"

    stamped, target_crc = stamp_bps_version(
        patch, source_sha256=sha, label="FR.2.1.156", header_version=156
    )

    rom = apply_bps_patch(source, stamped)
    assert decode_version_string(rom) == "FR.2.1.156"
    assert rom[0xBC] == 156
    assert rom[0xBD] == _compute_checksum(rom)
    assert target_crc == f"{zlib.crc32(rom):08x}"


def test_stamping_only_touches_the_version_bytes(synthetic) -> None:
    source, sha, target, patch = synthetic
    tileset = _read_gba_ptr(bytearray(target), _NFS_TILESET_PTR_OFF)

    stamped, _ = stamp_bps_version(
        patch, source_sha256=sha, label="FR.2.1.1234", header_version=1234
    )

    rom = apply_bps_patch(source, stamped)
    changed = [index for index in range(len(rom)) if rom[index] != target[index]]
    assert changed
    assert all(
        index in (0xBC, 0xBD) or tileset <= index < FREE_START + 0x4000
        for index in changed
    )
    assert _read_gba_ptr(bytearray(rom), _NFS_TILESET_PTR_OFF) == tileset
    # Le patch reste identique à celui que produirait l'encodeur avec la ROM.
    assert create_bps_patch(source, rom) == stamped


def test_stamping_is_deterministic_for_a_rerun(synthetic) -> None:
    _source, sha, _target, patch = synthetic
    options = {"source_sha256": sha, "label": "FR.2.1.156", "header_version": 156}

    assert stamp_bps_version(patch, **options) == stamp_bps_version(patch, **options)


def test_unpinned_source_is_rejected(synthetic) -> None:
    _source, _sha, _target, patch = synthetic

    with pytest.raises(ReleaseStampError, match="non épinglée"):
        stamp_bps_version(patch, source_sha256="0" * 64, label="FR.2.1.1",
                          header_version=1)


def test_bytes_from_an_unknown_source_region_are_rejected(synthetic, monkeypatch) -> None:
    """Sans zone libre connue, un octet SourceRead ne peut pas être deviné."""
    _source, sha, _target, patch = synthetic
    monkeypatch.setitem(release_stamp.PINNED_SOURCE_FREE_RANGES, sha, ())

    with pytest.raises(ReleaseStampError, match="inconnu sans ROM"):
        stamp_bps_version(patch, source_sha256=sha, label="FR.2.1.156",
                          header_version=156)


def test_growth_outside_free_space_is_rejected(synthetic, monkeypatch) -> None:
    _source, sha, target, patch = synthetic
    tileset = _read_gba_ptr(bytearray(target), _NFS_TILESET_PTR_OFF)
    monkeypatch.setitem(
        release_stamp.PINNED_SOURCE_FREE_RANGES, sha, ((FREE_START, tileset + 0x1000),)
    )
    monkeypatch.setattr(
        release_stamp, "_lz77_compress", lambda data: b"\x10" * 0x2000
    )

    with pytest.raises(ReleaseStampError, match="espace libre"):
        stamp_bps_version(patch, source_sha256=sha, label="FR.2.1.156",
                          header_version=156)


@pytest.mark.parametrize(
    ("label", "release", "expected"),
    [("FR.2.1.44", 156, "FR.2.1.156"), ("IN.2.1.0", 7, "IN.2.1.7")],
)
def test_release_version_label_replaces_the_build(label, release, expected) -> None:
    assert release_version_label(label, release) == expected


@pytest.mark.parametrize(("label", "release"), [("FR.2", 5), ("FR.2.1.44", 0),
                                                 ("FR.2.1.44", 10**6)])
def test_release_version_label_rejects_invalid_inputs(label, release) -> None:
    with pytest.raises(ReleaseStampError):
        release_version_label(label, release)


def test_tracked_bundle_is_stamped_without_any_rom(tmp_path) -> None:
    """Le workflow de release réécrit le vrai bundle suivi, sans ROM source."""
    bundle = tmp_path / "patches"
    shutil.copytree(ROOT / "patches", bundle)
    before = {path.name: path.read_bytes() for path in bundle.iterdir()}
    output = tmp_path / "release"

    manifest = stamp_release_bundle(bundle, 156, "v2.1.156", output)

    assert {path.name: path.read_bytes() for path in bundle.iterdir()} == before
    assert manifest["release_number"] == 156
    written = json.loads((output / "RELEASE_MANIFEST.json").read_text(encoding="utf-8"))
    assert written == manifest
    sums = {}
    for line in (output / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ")
        sums[name] = digest
    for entry in manifest["languages"]:
        code = entry["code"]
        assert entry["version_label"] == f"{code[:2].upper()}.2.1.156"
        assert entry["patch"] == f"pokemon_unbound_{code}_v2.1.156.bps"
        stamped = (output / entry["patch"]).read_bytes()
        assert hashlib.sha256(stamped).hexdigest() == entry["patch_sha256"] == sums[entry["patch"]]
        assert len(stamped) == entry["patch_size_bytes"]
        assert int.from_bytes(stamped[-8:-4], "little") == int(entry["target"]["crc32"], 16)
        assert "sha256" not in entry["target"]
        assert entry["stamped_from"]["build_number"] == _bundle_build(before)
        assert stamped != before[f"pokemon_unbound_{code}.bps"]
    assert set(sums) == {entry["patch"] for entry in manifest["languages"]}


def _bundle_build(files: dict[str, bytes]) -> int:
    return json.loads(files["RELEASE_MANIFEST.json"])["build_number"]


def test_stamp_rejects_a_tag_that_does_not_match_the_number(tmp_path) -> None:
    with pytest.raises(ReleaseStampError, match="tag"):
        stamp_release_bundle(ROOT / "patches", 156, "v2.1.155", tmp_path / "out")


def test_tracked_bundle_still_verifies_after_stamping(tmp_path) -> None:
    stamp_release_bundle(ROOT / "patches", 157, "v2.1.157", tmp_path / "out")

    PatchBundle(ROOT / "patches").verify(required_codes={"fr", "it", "de", "indie"})
