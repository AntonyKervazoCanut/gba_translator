"""Contrat fermé PT-39 : manifeste, protections, glossaire et budgets."""
import json
from pathlib import Path

import yaml

from scripts.apply_combined_fr import _load_combined
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt39_audit.json').read_text())


def test_manifest_protections_and_control_order():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    manifest = next(b['offsets'] for b in batches if b['id'] == 'PT-39')
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    guards = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protected = {int(e['offset'], 16): e['expected'] for e in guards['entries']}

    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 282
    assert sum(r['kind'] == 'description' for r in AUDIT['entries']) == 149
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        text = texts[off]
        assert text.replace('\n', r'\n') == protected[off] == row['portuguese']
        raw = TextEncoder.encode_pokemon(text, strict=True)
        assert len(raw) == row['encoded_bytes']
        assert line_widths(text) == row['line_widths']
        assert max(line_widths(text)) <= 122
        assert [b for b in raw if b >= 0xF7] == [
            b for b in bytes.fromhex(row['source_hex']) if b >= 0xF7]
        assert text.count('\n') < 5
        if row['kind'] == 'name':
            assert off == 0xA40A10 + 13 * row['move_ids'][0]
            assert len(raw) <= 13
        else:
            assert row['references']
            assert all(0x99F190 + 4 * i in row['references'] for i in row['move_ids'])


def test_names_follow_glossary_and_source_discrepancies_are_explicit():
    glossary = yaml.safe_load((ROOT / 'languages/pt/data/official_terminology.yaml').read_text())
    category = glossary['categories']['moves']
    assert category['fallback'] == 'preserve_english'
    for row in AUDIT['entries']:
        if row['kind'] == 'name':
            assert row['portuguese'] == category['entries'].get(
                row['english'], {}).get('value', row['english'])
        if row['english_reference'] != row['english']:
            assert 'ROM anglaise propre' in row['source_resolution']
    assert AUDIT['exceptions'] == 0


def test_domain_semantics_shared_pointers_and_extended_gmax_slots():
    rows = {r['offset']: r for r in AUDIT['entries']}
    flat = lambda off: rows[off]['portuguese'].replace(r'\n', ' ')
    assert 'dinheiro' in flat('0xa3e0a0') and 'dobra' in flat('0xa3e0a0')
    assert 'Aumenta sua Velocidade e reduz sua Defesa' in flat('0xa3ecc8')
    assert '3 PP do último movimento do alvo' in flat('0xa3f377')
    assert 'lesão por frio' in flat('0xa3f296')  # pas le gel décrit par le corpus EN contaminé
    assert 'envenenado' in flat('0xa3f832') and 'dobra' in flat('0xa3f832').lower()
    assert 'quatro a cinco turnos' in flat('0xa4073b')
    assert rows['0xa3e065']['references'] == [0x87AC28, 0x99FC0C]
    assert rows['0xa4062f']['move_ids'] == [895, 896]
    assert rows['0xa409be']['move_ids'] == [921, 922]
    assert 'Single Strike' in flat('0xa4096e')
    assert 'Rapid Strike' in flat('0xa409be')
    assert all('Max Guard' in flat(o) for o in ('0xa4096e', '0xa409be'))
