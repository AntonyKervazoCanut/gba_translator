"""PT-45 : manifeste fermé, protections, pages et mécanique de combat."""
import json
import re
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_width
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt45_audit.json').read_text())


def test_manifest_protections_pages_and_control_order():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    offsets = next(b['offsets'] for b in batches if b['id'] == 'PT-45')
    texts = entries()
    guards = {int(r['offset'], 16): r.get('expected_raw', r['expected']) for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == offsets
    assert len(offsets) == 283
    assert sum(r['status'] == 'exception' for r in AUDIT['entries']) == 1
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        assert row['reason'] and row['english_reference'] and row['source_hex']
        if row['status'] == 'exception':
            assert off not in texts and not row['references']
            continue
        assert texts[off] == guards[off] == row['portuguese']
        encoded = TextEncoder.encode_pokemon(texts[off].replace(r'\n', '\n'), strict=True)
        assert len(encoded) == row['encoded_bytes'] < 1000
        assert encoded[-1] == 0xFF and 0xFF not in encoded[:-1]
        assert [c for c in commands(encoded) if c[0] != 0xFE] == [
            c for c in commands(bytes.fromhex(row['source_hex'])) if c[0] != 0xFE]
        widths = [line_width(t) for t in re.split(r'<0xF[AB]>|\\n', texts[off])]
        assert widths == row['line_widths'] and max(widths) <= row['max_width']
        for page in texts[off].split('<0xFB>'):
            assert page.count(r'\n') <= 1


def test_domain_effects_and_glossary():
    texts = entries()
    for off, words in {
        0xA4A0B1: ['Skeli', 'Pokémon Unbound'], 0xA4A18E: ['Golche'],
        0xA4A28F: ['Thanasis'], 0xA4A34B: ['Lixdel'], 0xA4A45C: ['Cynthia'],
        0xA4A727: ['Candice', 'concentração'], 0xA49477: ['Moomoo Milk'],
        0xA4AA0B: ['Defesa', 'Def. Esp.', 'invertem'],
        0xA4AA55: ['itens equipados', 'perdem o efeito'],
        0xA4ACCF: ['Lucky Chant'],
    }.items():
        for word in words:
            assert word in texts[off].replace(r'\n', ' ')
    assert 'supereficaz' in texts[0xA4A8E0]
    assert 'pouco eficaz' in texts[0xA4A922]
    assert 'Não teve efeito' in texts[0xA4A96A]
    assert 'acertos críticos' in texts[0xA4ACCF]
    assert 'Habilidade suprimida' in texts[0xA4AD14].replace(r'\n', ' ')
    for off, name in [(0xA4AAD5, 'Gravity'), (0xA4ACA8, 'Tailwind'),
                      (0xA4AD67, 'Infestation'), (0xA4ADAB, 'Sky Drop'),
                      (0xA4ADCB, 'Crafty Shield'), (0xA4AE24, 'Quick Guard'),
                      (0xA4AE43, 'Wide Guard')]:
        assert name in texts[off]


def test_finalizer_after_all_generic_repairs():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_45') == 1
    for step in ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale'):
        assert steps.index(step) < steps.index('batch_45')
