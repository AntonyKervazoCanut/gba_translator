#!/usr/bin/env python3
"""Publier les notes d'une release GitHub via un secret webhook Discord."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def _truncate(text: str, limit: int) -> str:
    """Limiter aussi les caractères hors BMP, comptés sur deux unités UTF-16."""
    encoded = text.encode("utf-16-le")
    if len(encoded) <= limit * 2:
        return text
    return encoded[: (limit - 1) * 2].decode("utf-16-le", errors="ignore") + "…"


def build_payload(release: dict) -> dict:
    """Créer un message borné dont le titre mène aux notes complètes."""
    return {
        "allowed_mentions": {"parse": []},
        "embeds": [{
            "title": _truncate(release.get("name") or release["tagName"], 256),
            "description": _truncate(
                release.get("body") or "Les patchs sont disponibles sur la release GitHub.",
                4096,
            ),
            "url": release["url"],
        }],
    }


def publish(webhook: str, release: dict) -> None:
    """Attendre la confirmation Discord sans divulguer le secret en cas d'erreur."""
    if not re.fullmatch(r"https://discord\.com/api/webhooks/[0-9]+/[\w-]+", webhook):
        raise ValueError("DISCORD_RELEASE_WEBHOOK_URL absent ou invalide.")
    request = Request(
        webhook + "?wait=true",
        data=json.dumps(build_payload(release), ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "Unbound-release-notifier"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=30):
            pass
    except HTTPError as exc:
        raise RuntimeError(f"Échec de notification Discord (HTTP {exc.code}).") from None
    except (URLError, OSError):
        raise RuntimeError("Échec de connexion à Discord.") from None


def main() -> int:
    """Lire le JSON produit par gh release view et envoyer la notification."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("release_json", type=Path)
    args = parser.parse_args()
    try:
        release = json.loads(args.release_json.read_text(encoding="utf-8"))
        publish(os.environ.get("DISCORD_RELEASE_WEBHOOK_URL", ""), release)
    except (ValueError, KeyError, OSError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("Notes de version publiées sur Discord.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
