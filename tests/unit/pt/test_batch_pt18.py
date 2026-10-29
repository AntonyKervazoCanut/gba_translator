"""PT-18 : périmètre fermé, tableaux, placeholders et glossaire."""
import json
import re
from pathlib import Path

import yaml

from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands

ROOT = Path(__file__).resolve().parents[3]
ROWS = json.loads((ROOT / 'languages/pt/data/pt18_audit.json').read_text())['entries']


def values():
    """Lit les dernières occurrences sans supprimer les espaces de concaténation."""
    return {int(m[1], 16): m[2] for line in
            (ROOT / 'languages/pt/combined_pt.txt').read_text().splitlines()
            if (m := re.match(r'0x([0-9a-fA-F]+): ?(.*)', line))}


def test_closed_manifest_exact_guards_and_commands():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    manifest = next(b['offsets'] for b in batches if b['id'] == 'PT-18')
    guards = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protected = {int(e['offset'], 16): e['expected'] for e in guards['entries']}
    texts = values()
    assert len(ROWS) == len(manifest) == 282
    assert [r['offset'] for r in ROWS] == manifest
    for row in ROWS:
        offset = int(row['offset'], 16)
        assert row['source_hex'] and row['reason']
        if row['status'] in ('exception', 'retained_inline'):
            assert offset not in texts
            assert not row['references']
            if 'replacement' in row:
                assert row['replacement']['references']
            continue
        assert texts[offset] == protected[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(texts[offset].replace(r'\n', '\n'), strict=True)
        assert raw[-1] == 0xFF and 0xFF not in raw[:-1]
        assert len(raw) == row['encoded_bytes']
        assert commands(raw) == commands(bytes.fromhex(row['source_hex']))


def test_natures_and_keyboard_are_preserved_according_to_glossary():
    texts = values()
    natures = [r for r in ROWS if 0x463DBC <= int(r['offset'], 16) <= 0x463E57]
    assert len(natures) == 25
    assert [texts[int(r['offset'], 16)] for r in natures] == [r['english'] for r in natures]
    assert texts[0x47AAC1] == 'ABCDE' and texts[0x47AAFD] == 'abcde'
    assert 'Batalha Individual' in texts[0x459000]
    assert 'Batalha Dupla' in texts[0x459030]
    assert texts[0x4593E2] == 'Wonder Cards'
    assert texts[0x4593F1] == 'Wonder News'


def test_descriptions_keep_quantities_effects_and_source_semantics():
    texts = values()
    assert '20 PS' in texts[0x4834A8].replace(r'\n', ' ')
    assert '40 PS' in texts[0x483D6B].replace(r'\n', ' ')
    assert 'dois a cinco turnos' in texts[0x483DB0].replace(r'\n', ' ')
    assert 0x483B57 not in texts
    old = next(r for r in ROWS if r['offset'] == '0x483b57')
    assert old['exception_kind'] == 'obsolete_description'
    assert 'Attack' in old['replacement']['english']
    assert 'Sp. Atk' in old['replacement']['english']
    assert 'Defesa Especial' in texts[0x484098].replace(r'\n', ' ')
    # L'export « anglais » est historiquement vide/FR ; la préimage ROM prime.
    row = next(r for r in ROWS if r['offset'] == '0x483606')
    assert 'ally party' in row['english']
    assert 'névoa' in texts[0x483606] and 'água' not in texts[0x483606]


def test_dedicated_finalizer_follows_all_generic_repairs():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_18') == 1
    for step in ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale'):
        assert steps.index(step) < steps.index('batch_18')
