#!/usr/bin/env python3
"""Matérialise localement la ROM d'une publication, version réécrite incluse."""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.core.bps import BpsError, apply_bps_patch
from src.core.patch_bundle import PatchBundleError
from src.core.release_stamp import ReleaseStampError, stamp_release_bundle


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("language", help="Code langue (fr, it, de, indie)")
    parser.add_argument("--release-number", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bundle", type=Path, default=REPO_ROOT / "patches")
    parser.add_argument(
        "--source", type=Path, default=REPO_ROOT / "input/roms/englishrom.gba"
    )
    args = parser.parse_args()
    tag = f"v2.1.{args.release_number}"
    try:
        with tempfile.TemporaryDirectory() as temporary:
            manifest = stamp_release_bundle(
                args.bundle, args.release_number, tag, Path(temporary)
            )
            entry = next(
                (item for item in manifest["languages"] if item["code"] == args.language),
                None,
            )
            if entry is None:
                raise PatchBundleError(f"langue absente du bundle: {args.language}")
            rom = apply_bps_patch(
                args.source.read_bytes(), (Path(temporary) / entry["patch"]).read_bytes()
            )
    except (BpsError, OSError, PatchBundleError, ReleaseStampError) as exc:
        print(f"Erreur: {exc}", file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(rom)
    print(f"✓ {args.output} affiche {entry['version_label']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
