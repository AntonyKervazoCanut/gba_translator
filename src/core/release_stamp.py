"""Inscription du numéro de publication dans les patchs BPS, sans ROM.

Les patchs suivis sous ``patches/`` affichent en jeu le numéro du build local
qui les a produits (``FR.2.1.<build>``), alors que chaque publication GitHub
reçoit son propre numéro ``v2.1.<release>``. Ce module réécrit, directement
dans le flux BPS, les octets cibles qui portent la version :

- l'octet de version logicielle de l'en-tête GBA (``0xBC``) et son checksum
  complémentaire (``0xBD``) ;
- le tileset LZ77 de l'écran NOT FOR SALE, dont la bande ``v2.1.1.1`` est
  repeinte avec ``<PREFIXE>.<MAJEUR>.<MINEUR>.<release>``.

Notre encodeur n'émet que ``SourceRead`` et ``TargetRead`` : tout octet cible
différent de la source est donc littéral dans le patch. Les seuls octets
``SourceRead`` touchés se trouvent dans une zone libre (``0xFF``) de la ROM
source épinglée par son SHA-256, déclarée dans ``PINNED_SOURCE_FREE_RANGES``.
Le CRC32 de la cible se met à jour par linéarité, sans reconstruire la ROM.
"""

from __future__ import annotations

import bisect
import copy
import hashlib
import json
import struct
import zlib
from dataclasses import dataclass
from pathlib import Path

from languages.fr.patches.version import (
    _NFS_TILESET_PTR_OFF,
    _VER_GRID_COLS,
    _VER_GRID_ROWS,
    _VER_TILE_START,
    _blit_band_to_tiles,
    _lz77_compress,
    _lz77_decompress,
    _render_version_band,
)
from src.core.bps import (
    BPS_MAGIC,
    FOOTER_SIZE,
    SOURCE_READ,
    TARGET_READ,
    BpsError,
    _decode_number,
    _emit_action,
    _encode_number,
    inspect_bps_patch,
)
from src.core.patch_bundle import CHECKSUMS_NAME, MANIFEST_NAME, PatchBundle

# Plages [début, fin) valant 0xFF dans la ROM source épinglée : la zone libre
# qui accueille le tileset NOT FOR SALE recompressé par le build. Vérifiée
# contre la ROM locale par ``tests/test_release_stamp_rom.py``.
PINNED_SOURCE_FREE_RANGES: dict[str, tuple[tuple[int, int], ...]] = {
    "7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7": (
        (0x163BA9, 0x16582F),
    ),
}

_GBA_BASE = 0x08000000
_HEADER_VERSION_OFF = 0xBC
_HEADER_CHECKSUM_OFF = 0xBD
_MAX_LABEL_LENGTH = (_VER_GRID_COLS * 8) // 4


class ReleaseStampError(ValueError):
    """Signale un patch dont la version ne peut pas être réécrite sans ROM."""


@dataclass(frozen=True)
class _Segment:
    start: int
    length: int
    payload: bytes | None  # ``None`` pour une action SourceRead.


@dataclass(frozen=True)
class _ParsedPatch:
    source_size: int
    target_size: int
    metadata: bytes
    segments: list[_Segment]
    source_crc: int
    target_crc: int


def _parse(patch: bytes) -> _ParsedPatch:
    inspect_bps_patch(patch)
    footer_start = len(patch) - FOOTER_SIZE
    cursor = len(BPS_MAGIC)
    source_size, cursor = _decode_number(patch, cursor, footer_start)
    target_size, cursor = _decode_number(patch, cursor, footer_start)
    metadata_size, cursor = _decode_number(patch, cursor, footer_start)
    metadata = patch[cursor:cursor + metadata_size]
    cursor += metadata_size
    segments = []
    offset = 0
    while offset < target_size:
        value, cursor = _decode_number(patch, cursor, footer_start)
        length = (value >> 2) + 1
        if value & 3 == TARGET_READ:
            segments.append(_Segment(offset, length, patch[cursor:cursor + length]))
            cursor += length
        else:
            segments.append(_Segment(offset, length, None))
        offset += length
    return _ParsedPatch(
        source_size,
        target_size,
        metadata,
        segments,
        int.from_bytes(patch[-12:-8], "little"),
        int.from_bytes(patch[-8:-4], "little"),
    )


class _KnownTarget:
    """Vue en lecture seule des octets cibles déductibles sans la source."""

    def __init__(self, parsed: _ParsedPatch, free_ranges: tuple[tuple[int, int], ...]):
        self._segments = parsed.segments
        self._starts = [segment.start for segment in parsed.segments]
        self._free_ranges = free_ranges
        self._size = parsed.target_size

    def __len__(self) -> int:
        return self._size

    def source_byte(self, position: int) -> int | None:
        """Retourne l'octet source connu (zone libre épinglée) ou ``None``."""
        if any(start <= position < end for start, end in self._free_ranges):
            return 0xFF
        return None

    def is_source_read(self, position: int) -> bool:
        return self._segment(position).payload is None

    def _segment(self, position: int) -> _Segment:
        if not 0 <= position < self._size:
            raise ReleaseStampError(f"offset cible 0x{position:X} hors ROM")
        return self._segments[bisect.bisect_right(self._starts, position) - 1]

    def __getitem__(self, position: int) -> int:
        segment = self._segment(position)
        if segment.payload is not None:
            return segment.payload[position - segment.start]
        known = self.source_byte(position)
        if known is None:
            raise ReleaseStampError(
                f"octet cible 0x{position:X} issu de la source, inconnu sans ROM"
            )
        return known

    def read(self, position: int, length: int) -> bytes:
        return bytes(self[position + index] for index in range(length))


def release_version_label(version_label: str, release_number: int) -> str:
    """Remplace le build d'un libellé ``FR.2.1.44`` par la publication."""
    if isinstance(release_number, bool) or release_number <= 0:
        raise ReleaseStampError("le numéro de publication doit être positif")
    parts = [part for part in version_label.split(".") if part]
    if len(parts) < 3:
        raise ReleaseStampError(f"libellé de version invalide: {version_label!r}")
    label = f"{'.'.join(parts[:3])}.{release_number}"
    if len(label) > _MAX_LABEL_LENGTH:
        raise ReleaseStampError(f"libellé {label!r} trop long pour l'écran d'intro")
    return label


def _version_edits(
    known: _KnownTarget, label: str, header_version: int
) -> dict[int, int]:
    edits: dict[int, int] = {}

    old_version = known[_HEADER_VERSION_OFF]
    old_checksum = known[_HEADER_CHECKSUM_OFF]
    new_version = header_version & 0xFF
    edits[_HEADER_VERSION_OFF] = new_version
    edits[_HEADER_CHECKSUM_OFF] = (old_checksum - (new_version - old_version)) & 0xFF

    pointer = struct.unpack("<I", known.read(_NFS_TILESET_PTR_OFF, 4))[0]
    if pointer < _GBA_BASE:
        raise ReleaseStampError("pointeur du tileset NOT FOR SALE invalide")
    tileset_offset = pointer - _GBA_BASE
    decoded = _lz77_decompress(known, tileset_offset)
    if decoded is None:
        raise ReleaseStampError("tileset NOT FOR SALE illisible dans le patch")
    tileset, old_length = decoded
    if len(tileset) < (_VER_TILE_START + _VER_GRID_COLS * _VER_GRID_ROWS) * 32:
        raise ReleaseStampError("tileset NOT FOR SALE trop court pour la bande")
    tileset = bytearray(tileset)
    _blit_band_to_tiles(tileset, _render_version_band(label))
    stream = _lz77_compress(bytes(tileset))

    for index in range(old_length, len(stream)):
        position = tileset_offset + index
        # Croissance uniquement sur des octets libres jamais écrits par le build.
        if not known.is_source_read(position) or known.source_byte(position) != 0xFF:
            raise ReleaseStampError(
                f"aucun espace libre connu pour agrandir le tileset (0x{position:X})"
            )
    for index in range(max(old_length, len(stream))):
        edits[tileset_offset + index] = stream[index] if index < len(stream) else 0xFF
    return edits


def _encode(parsed: _ParsedPatch, segments: list[tuple[int, int, bytes | None]],
            target_crc: int) -> bytes:
    patch = bytearray(BPS_MAGIC)
    patch.extend(_encode_number(parsed.source_size))
    patch.extend(_encode_number(parsed.target_size))
    patch.extend(_encode_number(len(parsed.metadata)))
    patch.extend(parsed.metadata)
    for _start, length, payload in segments:
        if payload is None:
            _emit_action(patch, SOURCE_READ, length)
        else:
            _emit_action(patch, TARGET_READ, length)
            patch.extend(payload)
    patch.extend(parsed.source_crc.to_bytes(4, "little"))
    patch.extend(target_crc.to_bytes(4, "little"))
    patch.extend(zlib.crc32(patch).to_bytes(4, "little"))
    return bytes(patch)


def _rewrite(parsed: _ParsedPatch, known: _KnownTarget, edits: dict[int, int]
             ) -> tuple[list[tuple[int, int, bytes | None]], int]:
    """Applique ``edits`` au flux d'actions et calcule le nouveau CRC cible."""
    positions = sorted(edits)
    delta = bytearray(parsed.target_size)
    for position in positions:
        delta[position] = known[position] ^ edits[position]
    target_crc = (
        parsed.target_crc
        ^ zlib.crc32(delta)
        ^ zlib.crc32(bytes(parsed.target_size))
    )

    runs: list[tuple[int, int, bytes | None]] = []

    def push(start: int, length: int, payload: bytes | None) -> None:
        if length <= 0:
            return
        if runs:
            previous_start, previous_length, previous_payload = runs[-1]
            if (previous_payload is None) == (payload is None):
                merged = None if payload is None else previous_payload + payload
                runs[-1] = (previous_start, previous_length + length, merged)
                return
        runs.append((start, length, payload))

    for segment in parsed.segments:
        end = segment.start + segment.length
        first = bisect.bisect_left(positions, segment.start)
        last = bisect.bisect_left(positions, end)
        if first == last:
            push(segment.start, segment.length, segment.payload)
            continue
        cursor = segment.start
        for position in positions[first:last]:
            if position > cursor:
                prefix = (
                    None
                    if segment.payload is None
                    else segment.payload[cursor - segment.start:position - segment.start]
                )
                push(cursor, position - cursor, prefix)
            value = edits[position]
            if known.source_byte(position) == value:
                push(position, 1, None)
            else:
                push(position, 1, bytes((value,)))
            cursor = position + 1
        if cursor < end:
            suffix = (
                None if segment.payload is None
                else segment.payload[cursor - segment.start:]
            )
            push(cursor, end - cursor, suffix)
    return runs, target_crc


def stamp_bps_version(
    patch: bytes, *, source_sha256: str, label: str, header_version: int
) -> tuple[bytes, str]:
    """Réécrit la version affichée par la ROM cible d'un patch BPS.

    Args:
        patch: Patch BPS1 produit par :func:`src.core.bps.create_bps_patch`.
        source_sha256: SHA-256 de la ROM source déclarée par le manifeste.
        label: Libellé à peindre sur l'écran NOT FOR SALE (``FR.2.1.155``).
        header_version: Valeur dont l'octet bas remplit l'en-tête GBA ``0xBC``.

    Returns:
        Le nouveau patch et le CRC32 hexadécimal de sa ROM cible.

    Raises:
        ReleaseStampError: Si un octet nécessaire n'est pas déductible sans ROM.
    """
    free_ranges = PINNED_SOURCE_FREE_RANGES.get(source_sha256)
    if free_ranges is None:
        raise ReleaseStampError("ROM source non épinglée pour l'inscription de version")
    try:
        parsed = _parse(patch)
    except BpsError as exc:
        raise ReleaseStampError(f"patch BPS invalide: {exc}") from exc
    known = _KnownTarget(parsed, free_ranges)
    edits = _version_edits(known, label, header_version)
    runs, target_crc = _rewrite(parsed, known, edits)
    stamped = _encode(parsed, runs, target_crc)
    info = inspect_bps_patch(stamped)
    return stamped, info.target_crc32


def stamp_release_bundle(
    bundle: Path, release_number: int, version_tag: str, output: Path
) -> dict:
    """Écrit les assets d'une publication dont la ROM affiche ``release_number``.

    Le bundle canonique est vérifié puis laissé intact. ``output`` reçoit
    ``pokemon_unbound_<code>_<version_tag>.bps``, un ``RELEASE_MANIFEST.json``
    décrivant ces patchs et un ``SHA256SUMS.txt`` utilisant leurs noms publiés.
    """
    if not version_tag.endswith(f".{release_number}"):
        raise ReleaseStampError("le tag de version ne correspond pas à la publication")
    manifest = PatchBundle(bundle).verify()
    published = copy.deepcopy(manifest)
    published["release_number"] = release_number
    output.mkdir(parents=True, exist_ok=True)
    checksums = []
    for entry in published["languages"]:
        patch = (bundle / entry["patch"]).read_bytes()
        label = release_version_label(entry["version_label"], release_number)
        stamped, target_crc = stamp_bps_version(
            patch,
            source_sha256=entry["source"]["sha256"],
            label=label,
            header_version=release_number,
        )
        name = f"{Path(entry['patch']).stem}_{version_tag}.bps"
        (output / name).write_bytes(stamped)
        digest = hashlib.sha256(stamped).hexdigest()
        base_target = entry["target"]
        entry["version_label"] = label
        entry["patch"] = name
        entry["patch_sha256"] = digest
        entry["patch_size_bytes"] = len(stamped)
        # Le SHA-256 cible exige la ROM complète : seul le CRC32 est recalculé.
        entry["target"] = {
            "file": base_target["file"],
            "crc32": target_crc,
            "size_bytes": base_target["size_bytes"],
        }
        entry["stamped_from"] = {
            "build_number": manifest["build_number"],
            "patch_sha256": hashlib.sha256(patch).hexdigest(),
            "target_sha256": base_target["sha256"],
        }
        checksums.append(f"{digest}  {name}")
    (output / MANIFEST_NAME).write_text(
        json.dumps(published, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (output / CHECKSUMS_NAME).write_text("\n".join(checksums) + "\n", encoding="utf-8")
    return published
