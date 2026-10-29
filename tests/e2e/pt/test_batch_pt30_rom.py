"""Vérifie les 283 noms réellement livrés et les cinq suffixes exclus."""
import json
from pathlib import Path

import pytest

from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
pytestmark = pytest.mark.rom


def test_built_pt30_fixed_item_names():
    audit = json.loads((ROOT / 'languages/pt/data/pt30_audit.json').read_text())
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    rom = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    assert rom[0x9A8C0:0x9A8DC] == bytes.fromhex(audit['accessor_hex'])
    for row in audit['entries']:
        off = int(row['offset'], 16)
        if row['status'] == 'exception':
            end = int(row['cell'], 16) + 14
            assert rom[off:end] == source[off:end]
        else:
            encoded = TextEncoder.encode_pokemon(row['expected'], strict=True)
            assert rom[off:off + len(encoded)] == encoded, row['offset']
            # Identifiant, prix, effet, pointeurs fonction : jamais écrits par notre patch.
            assert rom[off + 14:off + 20] == source[off + 14:off + 20]
