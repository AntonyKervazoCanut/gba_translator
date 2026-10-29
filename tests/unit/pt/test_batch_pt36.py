"""Contrat fermé PT-36 : talents, glossaire, budgets et consommateurs."""
import json
from pathlib import Path

import yaml

from scripts.apply_combined_fr import _load_combined
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt36_audit.json').read_text())


def test_manifest_protections_and_exact_token_order():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-36')
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    guards = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protected = {int(e['offset'], 16): e['expected'] for e in guards['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 282
    exceptions = []
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['reason']
        if row['status'] == 'exception':
            exceptions.append(offset)
            assert offset not in texts and not row['references']
            continue
        assert texts[offset] == protected[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(texts[offset], strict=True)
        assert len(raw) == row['encoded_bytes']
        assert line_widths(texts[offset]) == row['line_widths']
        assert max(row['line_widths']) <= (120 if row['kind'] == 'name' else 192)
        # Aucune entrée EN du lot ne contient de contrôle ou de variable.
        assert not set(bytes.fromhex(row['source_hex'])[:-1]).intersection(range(0xF7, 0x100))
        assert not set(raw[:-1]).intersection(range(0xF7, 0x100))
        if row['kind'] == 'name':
            assert offset == 0xA36398 + 17 * row['ability_ids'][0]
            assert len(raw) <= 17
    assert exceptions == [0xA35424, 0xA35811, 0xA35DCF]


def test_names_follow_frozen_glossary_without_invented_translations():
    glossary = yaml.safe_load((ROOT / 'languages/pt/data/official_terminology.yaml').read_text())
    category = glossary['categories']['abilities']
    assert category['fallback'] == 'preserve_english'
    changed = []
    for row in AUDIT['entries']:
        if row['kind'] != 'name':
            continue
        expected = category['entries'].get(row['english'], {}).get('value', row['english'])
        assert row['portuguese'] == expected
        if expected != row['english']:
            changed.append(expected)
    assert changed == ['Supercrescimento', 'Incêndio', 'Dilúvio']


def test_domain_semantics_and_shared_descriptions():
    rows = {int(r['offset'], 16): r for r in AUDIT['entries']}
    # Weak Armor atteint le porteur ; Gooey réduit la Vitesse de l'attaquant.
    assert rows[0xA35B16]['portuguese'] == 'Atingido: Velocidade +, Defesa -.'
    assert rows[0xA353EF]['portuguese'] == 'Atingido: Velocidade do alvo -.'
    # Filter et Solid Rock partagent une description ; les deux restent couverts.
    assert rows[0xA351BA]['ability_ids'] == [101, 166]
    assert len(rows[0xA351BA]['references']) == 2
    assert rows[0xA34F4C]['ability_ids'] == [40]
    assert rows[0xA36320]['references'] == [0x9A9440]
    assert rows[0xA36343]['references'] == [0x9A9438]
    assert rows[0xA3635F]['references'] == [0x9A943C]
    assert rows[0xA36375]['references'] == [0x9A9444]
