#!/usr/bin/env python3
"""Prépare les assets BPS d'une publication affichant son numéro en jeu."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.core.patch_bundle import PatchBundleError
from src.core.release_stamp import ReleaseStampError, stamp_release_bundle


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path, help="bundle canonique (patches/)")
    parser.add_argument("--release-number", type=int, required=True)
    parser.add_argument("--version-tag", required=True, help="ex. v2.1.155")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        manifest = stamp_release_bundle(
            args.bundle, args.release_number, args.version_tag, args.output
        )
    except (PatchBundleError, ReleaseStampError, OSError) as exc:
        print(f"Erreur: {exc}", file=sys.stderr)
        return 1
    for entry in manifest["languages"]:
        print(f"✓ {entry['patch']} affiche {entry['version_label']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
