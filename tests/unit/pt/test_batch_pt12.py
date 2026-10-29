"""Contrat PT-12 : périmètre fermé, tokens ROM et vocabulaire des menus."""
from __future__ import annotations

import importlib
import json
import re
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]


def audit() -> dict:
    """Lit les décisions de chaque offset du manifeste."""
    return json.loads((ROOT / 'languages/pt/data/pt12_audit.json').read_text())


def translations() -> dict[int, str]:
    """Résout les occurrences vivantes, sans réécrire les sources."""
    result = {}
    for line in (ROOT / 'languages/pt/combined_pt.txt').read_text().splitlines():
        match = re.match(r'0x([\da-fA-F]+): ?(.*)', line)
        if match:
            result[int(match[1], 16)] = match[2]
    return result


def encoded(row: dict) -> bytes:
    """Encode strictement la valeur contractuelle, sans fallback."""
    return TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)


def test_exact_manifest_and_protection_coverage() -> None:
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    offsets = next(b['offsets'] for b in batches if b['id'] == 'PT-12')
    rows = audit()['entries']
    assert [row['offset'] for row in rows] == offsets
    assert len(rows) == 282
    assert sum(r['status'] == 'translated' for r in rows) == 263
    assert sum(r['status'] == 'exception' for r in rows) == 19
    protected = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protections = {int(r['offset'], 16): r['expected'] for r in protected['entries']}
    actual = translations()
    for row in rows:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['french_reference'], row['offset']
        if row['status'] == 'exception':
            assert offset not in actual and not row['live_sites']
        else:
            assert actual[offset] == protections[offset] == row['portuguese']
            assert row['live_sites']


def test_control_order_pages_and_encoded_budgets() -> None:
    builder = importlib.import_module('src.translators.19_build_translated_rom_generic').TranslatedROMBuilder
    for row in audit()['entries']:
        if row['status'] == 'exception':
            continue
        raw = encoded(row)
        source = bytes.fromhex(row['source_hex'])
        assert builder._extract_control_sequences_from_raw(raw, include_breaks=True) == builder._extract_control_sequences_from_raw(source, include_breaks=True), row['offset']
        assert raw[-1] == 255 and 255 not in raw[:-1]
        assert len(raw) == row['encoded_bytes'] <= 512
        assert line_widths(row['portuguese'].replace(r'\n', '\n')) == row['line_pixels']
        assert max(row['line_pixels']) <= 192, row['offset']


def test_menu_semantics_and_glossary() -> None:
    actual = translations()
    assert actual[0x417674] == 'Ataque'
    assert actual[0x41767b] == 'Defesa'
    assert actual[0x41768d] == 'Velocidade'
    assert actual[0x417914] == 'DRM'
    assert actual[0x417918] == 'QMD'
    assert actual[0x41791c] == 'CNG'
    assert actual[0x417944] == 'BATALHA INDIVIDUAL'
    assert actual[0x417952] == 'BATALHA DUPLA'
    assert actual[0x417be2] == 'EEVEE'
    assert actual[0x417a02] == 'RED SHARD'
    assert actual[0x417df3] == 'ONE ISLAND'
    assert 'Cut' in actual[0x417258] and 'Surf' in actual[0x417270]
    assert 'PS' in actual[0x416f27] and 'quatro movimentos' in actual[0x416df7]
    assert actual[0x417c2d] == 'Fichas'


def test_final_patch_covers_only_contractual_consumers() -> None:
    from languages.pt.patches.batch_12 import definitions

    rows = [r for r in audit()['entries'] if r['status'] == 'translated']
    definitions_ = definitions()
    assert len(definitions_) == len(rows)
    rejected = set(audit()['rejected_sites'])
    for row, definition in zip(rows, definitions_):
        assert definition['offset'] == row['offset']
        assert definition['references'] == [int(s, 16) for s in row['live_sites']]
        assert not rejected.intersection(row['live_sites'])
        assert definition['layout']['preserve_line_count']
    cfg = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())
    assert cfg['patches'].index('batch_12') > max(
        cfg['patches'].index(name) for name in ('repair_lz77', 'repair_localized_lz77', 'repoint_stale')
    )


def test_report_and_binary_evidence_account_for_every_offset() -> None:
    report = (ROOT / 'docs/analysis/28_PT_BR_PT12.md').read_text()
    offsets = re.findall(r'^\| `(0x[\da-f]+)` \|', report, re.MULTILINE)
    data = audit()
    assert offsets == [r['offset'] for r in data['entries']]
    assert len(set(offsets)) == 282
    assert re.fullmatch(r'[0-9a-f]{64}', data['source_sha256'])
    assert re.fullmatch(r'[0-9a-f]{64}', data['built_sha256'])
    assert sum(len(r['targets']) for r in data['entries']) == 426
    assert len(data['rejected_sites']) == 5
