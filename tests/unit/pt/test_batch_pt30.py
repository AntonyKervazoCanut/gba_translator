"""PT-30 : couverture exacte, glossaire et isolation des cellules d'objets."""
import json
from pathlib import Path

import pytest

from languages.pt.patches.batch_30 import apply_patches
from scripts.apply_combined_fr import _load_combined
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt30_audit.json').read_text())
ROWS = AUDIT['entries']
TEXTS, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')


def test_scope_glossary_and_exceptions():
    batch = next(b for b in json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
                 if b['id'] == 'PT-30')
    assert [r['offset'] for r in ROWS] == batch['offsets']
    assert len(ROWS) == 288
    assert sum(r['status'] == 'exception' for r in ROWS) == 5
    for row in ROWS:
        off = int(row['offset'], 16)
        if row['status'] == 'exception':
            assert off not in TEXTS
            assert row['reason'] and not row['pointer_byte_matches']
            # Un suffixe exclu reste strictement dans le champ nom de sa cellule.
            assert 0 < off - int(row['cell'], 16) < 14
        else:
            expected = 'Poção' if row['source_text'] == 'Potion' else row['source_text']
            assert TEXTS[off] == expected == row['expected']
            assert row['pt_bytes'] == len(TextEncoder.encode_pokemon(expected, strict=True)) <= 14
            assert row['max_pixels'] == max(line_widths(expected)) <= 78


def fixture_rom():
    # Les cellules sont un extrait réel versionné dans l'audit, sans ROM synthétique textuelle.
    rom = bytearray(0x879600)
    rom[0x9A8C0:0x9A8DC] = bytes.fromhex(AUDIT['accessor_hex'])
    for row in ROWS:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        rom[offset:offset + len(raw)] = raw
    return rom


def test_patch_is_bounded_atomic_and_idempotent():
    rom = fixture_rom()
    before = bytes(rom)
    assert apply_patches(rom) == 1
    changed = {i for i, (a, b) in enumerate(zip(before, rom)) if a != b}
    assert changed and changed <= set(range(0x87643C, 0x876443))
    for row in ROWS:
        if row['status'] != 'exception':
            offset = int(row['offset'], 16)
            encoded = TextEncoder.encode_pokemon(row['expected'], strict=True)
            assert rom[offset:offset + len(encoded)] == encoded
    assert apply_patches(rom) == 0
    rom[0x9A8D8] ^= 1
    before = bytes(rom)
    with pytest.raises(ValueError, match='Lecteur'):
        apply_patches(rom)
    assert rom == before
