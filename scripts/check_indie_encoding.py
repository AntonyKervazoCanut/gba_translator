#!/usr/bin/env python3
"""Reject unsupported characters in the live Hindi romanisation entries."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.check_translation_integrity import load_last_wins
from src.core.text_codec import TextEncoder

COMBINED = Path(__file__).resolve().parents[1] / 'languages/indie/combined_indie.txt'
# Named placeholders are resolved against the English control sequences by the
# builder; raw hex tokens are parsed by the encoder itself. Do not hide malformed
# placeholders or their contents from the strict encoder.
NAMED_TOKEN = re.compile(r'\{[A-Z][A-Z0-9_]*\}')


def validate_text(text: str) -> None:
    text = text.replace('\\n', '\n').replace('\\l', '<0xFA>').replace('\\p', '<0xFB>')
    text = NAMED_TOKEN.sub(
        lambda match: match.group() if TextEncoder._parse_brace_token(match.group(), 0) else '',
        text,
    )
    TextEncoder.encode_pokemon(text, strict=True)


def main() -> int:
    entries, _ = load_last_wins(COMBINED)
    errors = []
    for offset, text in entries.items():
        try:
            validate_text(text)
        except ValueError as exc:
            errors.append(f'0x{offset:X}: {exc}')
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'Indie : {len(entries)} entrées vivantes encodables')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
