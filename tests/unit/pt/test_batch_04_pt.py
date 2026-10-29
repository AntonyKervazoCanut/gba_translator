"""PT-04 : texte, cellules fixes, périmètre et conservation des contrôles."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt04_audit.json').read_text())
ROWS = AUDIT['entries']


def translations() -> dict[int, str]:
    """Résout le combined cumulatif, sans modifier la source."""
    result = {}
    for line in (ROOT / 'languages/pt/combined_pt.txt').read_text().splitlines():
        match = re.match(r'0x([\da-fA-F]+):\s?(.*)', line)
        if match:
            result[int(match[1], 16)] = match[2].replace('\\n', '\n')
    return result


def controls(raw: bytes) -> list[bytes]:
    """Consomme les paramètres sans confondre une valeur et un opcode."""
    result = []
    index = 0
    while index < len(raw):
        if raw[index] in (0xFA, 0xFB):
            result.append(raw[index:index + 1])
            index += 1
        elif raw[index] in (0xFC, 0xFD, 0xF7, 0xF8, 0xF9):
            # PT-04 : uniquement FC 03 xx (fond) et FD xx (variable).
            assert raw[index] == 0xFD or raw[index:index + 2] == b"\xfc\x03"
            size = 2 if raw[index] == 0xFD else 3
            result.append(raw[index:index + size])
            index += size
        else:
            index += 1
    return result


def test_manifest_is_exhaustively_accounted_for() -> None:
    batch = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())[3]
    assert len(ROWS) == len({e['offset'] for e in ROWS}) == 277
    assert {e['offset'] for e in ROWS} == set(batch['offsets'])
    for entry in ROWS:
        if entry['status'] != 'translated':
            assert entry['reason']


@pytest.mark.parametrize('entry', [e for e in ROWS if e['status'] == 'translated'],
                         ids=lambda e: e['offset'])
def test_source_translation_controls_and_budgets(entry: dict) -> None:
    text = translations()[int(entry['offset'], 16)]
    encoded = TextEncoder.encode_pokemon(text, strict=True)
    assert controls(encoded) == controls(bytes.fromhex(entry['source_hex']))
    assert encoded[-1] == 255 and 255 not in encoded[:-1]
    assert max(line_widths(text), default=0) <= 192
    if 0x24F3C4 <= int(entry['offset'], 16) <= 0x24FABE:
        assert '\n' not in text  # Résumé : une seule ligne.
    if entry['delivery'] == 'fixed_cell':
        assert len(TextEncoder.encode_pokemon(text.lstrip(), strict=True)) - entry.get('prefix_bytes', 0) <= entry['cell_bytes']


def test_fixed_patch_bounds_and_idempotence() -> None:
    from languages.pt.patches.batch_04 import apply

    # Vraies cellules de ROM consignées dans l’audit, pas de faux ROMReader.
    fixed = [e for e in ROWS if e.get('delivery') == 'fixed_cell']
    end = max(int(e['cell_offset'], 16) + e['cell_bytes'] for e in fixed) + 16
    source = bytearray(b'\xff' * end)
    for entry in fixed:
        at = int(entry['offset'], 16)
        raw = bytes.fromhex(entry['source_hex'])
        source[at:at + len(raw)] = raw
        at = int(entry['cell_offset'], 16)
        source[at:at + entry['cell_bytes']] = bytes.fromhex(entry['source_cell_hex'])
    rom = bytearray(source)
    before = bytes(rom)
    assert apply(rom, bytes(source)) == len(fixed)
    allowed = {i for e in fixed for i in range(int(e['offset'], 16),
               int(e['cell_offset'], 16) + e['cell_bytes'])}
    assert all(i in allowed for i, (a, b) in enumerate(zip(before, rom)) if a != b)
    for entry in fixed:
        at = int(entry['cell_offset'], 16)
        expected = TextEncoder.encode_pokemon(translations()[int(entry['offset'], 16)].lstrip())
        expected = expected[entry.get('prefix_bytes', 0):]
        assert rom[at:at + entry['cell_bytes']] == expected.ljust(entry['cell_bytes'], b'\0')
    assert apply(rom, bytes(source)) == 0


def test_glossary_and_real_zones() -> None:
    pt = translations()
    assert 'Habilidade' in pt[0x24F3C4]
    assert 'PS' in pt[0x24F4B3]
    assert pt[0x24F1F4] == 'Planta'
    assert pt[0x24FF96].strip() == 'Incêndio'
    assert pt[0x24FFA0].strip() == 'Dilúvio'
    assert 'SES\\nExpressway'.replace('\\n', '\n') in pt[0x26D524]
    assert 'Challenge Road' in pt[0x26D5DC]
    assert 'Great Desert' in pt[0x270FA1]
    assert 'Minus' in pt[0x24F90F] and 'Plus' in pt[0x24F925]


def test_binary_prefix_is_not_an_independent_ability_description() -> None:
    by_offset = {int(e['offset'], 16): e for e in ROWS}
    prefix = by_offset[0x24F3C1]
    canonical = by_offset[0x24F3C4]
    assert prefix['status'] == 'alias'
    assert prefix['canonical_offset'] == canonical['offset']
    assert prefix['prefix_hex'] == '050000'
    assert not prefix['all_pointer_occurrences']
    # La traduction du suffixe vivant change aussi la fin de l’extraction
    # précédente ; seul le préfixe binaire doit rester inchangé.
    assert bytes.fromhex(prefix['source_hex'])[3:] == bytes.fromhex(canonical['source_hex'])
