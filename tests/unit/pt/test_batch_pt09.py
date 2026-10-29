"""PT-09 : couverture fermée, vocabulaire et structure des messages de combat."""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_widths
from src.core.fixed_tables import in_fixed_table
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]


def entries() -> list[dict]:
    """Lit les 281 décisions documentées du lot."""
    return json.loads((ROOT / 'languages/pt/data/pt09_audit.json').read_text())['entries']


def translations() -> dict[int, str]:
    """Résout les dernières occurrences sans réécrire le combined."""
    result = {}
    for line in (ROOT / 'languages/pt/combined_pt.txt').read_text().splitlines():
        match = re.match(r'0x([\da-fA-F]+): ?(.*)', line)
        if match:
            result[int(match[1], 16)] = match[2]
    return result


def controls(raw: bytes) -> list[bytes]:
    """Isole les contrôles et les sauts avec leurs paramètres exacts."""
    result = []
    pos = 0
    while pos < len(raw):
        if raw[pos] >= 0xF7 and raw[pos] != 0xFF:
            # Le lot contient FD xx, FC 08 xx, FC 0A et FA/FB/FE.
            if raw[pos] == 0xFD:
                size = 2
            elif raw[pos] == 0xFC:
                assert raw[pos + 1] in (0x08, 0x0A)
                size = 3 if raw[pos + 1] == 0x08 else 2
            else:
                assert raw[pos] in (0xFA, 0xFB, 0xFE)
                size = 1
            result.append(raw[pos:pos + size])
            pos += size
        else:
            pos += 1
    return result


def test_manifest_coverage_and_exact_protections() -> None:
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    offsets = {int(o, 16) for b in batches if b['id'] == 'PT-09' for o in b['offsets']}
    rows = entries()
    assert len(rows) == len(offsets) == 281
    assert {int(e['offset'], 16) for e in rows} == offsets
    actual = translations()
    protection = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protected = {int(e['offset'], 16): e['expected'] for e in protection['entries']}
    assert sum(e['status'] == 'exception' for e in rows) == 15
    for row in rows:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['french_reference']
        if row['status'] == 'exception':
            assert offset not in actual
            assert not row['live_sites']
        else:
            assert actual[offset] == protected[offset] == row['portuguese']
            assert row['live_sites']
            assert not in_fixed_table(offset)


def test_controls_pages_encoding_and_widths() -> None:
    for row in entries():
        if row['status'] == 'exception':
            continue
        text = translations()[int(row['offset'], 16)].replace(r'\n', '\n')
        encoded = TextEncoder.encode_pokemon(text, strict=True)
        assert encoded[-1] == 255 and 255 not in encoded[:-1], row['offset']
        assert controls(encoded) == controls(bytes.fromhex(row['source_hex'])), row['offset']
        assert len(encoded) == row['encoded_bytes']
        assert line_widths(text) == row['line_pixels']
        budget = 102 if int(row['offset'], 16) < 0x3eed08 else 192
        assert max(line_widths(text), default=0) <= budget, row['offset']


def test_glossary_and_battle_meaning() -> None:
    actual = translations()
    assert actual[0x3ecaac] == 'Cancelar'
    assert actual[0x3ecaa4] == 'DESTINO'
    for row in entries():
        offset = int(row['offset'], 16)
        if 0x3eed08 <= offset < 0x3fb219 and row['status'] != 'exception':
            assert actual[offset] == row['english']  # Noms propres F-759.
    assert 'nocauteado' in actual[0x3fb400]
    assert 'Terrestres' in actual[0x3fb3af]
    assert 'PS' in actual[0x3fb935]
    assert 'Safeguard' in actual[0x3fb9d9]
    assert 'Leech Seed' in actual[0x3fbc99]
    assert 'movimentos' in actual[0x3fb2d1]
    assert actual[0x3fb283].startswith('<0x00>')  # Espace du tampon concaténé.
