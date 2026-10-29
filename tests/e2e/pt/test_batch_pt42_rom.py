"""PT-42 : préimages, pointeurs exhaustifs et texte réellement injecté."""
import hashlib
import json
import re
from pathlib import Path

import pytest

from languages.pt.patches.batch_42 import make_patch

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt42_audit.json').read_text())
pytestmark = pytest.mark.rom


def test_source_and_built_rom_all_283_offsets():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    targets = {int(row['offset'], 16): [] for row in AUDIT['entries']}
    for match in re.finditer(b'[\x08\x09]', source):
        ref = match.start() - 3
        if ref >= 0:
            target = int.from_bytes(source[ref:ref + 4], 'little') - 0x08000000
            if target in targets:
                targets[target].append(ref)
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        assert targets[offset] == row['references']
    rom = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    make_patch(source).verify(rom)
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            offset = int(row['offset'], 16)
            raw = bytes.fromhex(row['source_hex'])
            assert rom[offset:offset + len(raw)] == raw
