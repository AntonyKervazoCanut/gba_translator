"""PT-87 : manifeste exact, pagination, missions et possessif contextuel."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml

from scripts.apply_combined_fr import _load_combined, _normalize_text
from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]


def audit():
    return json.loads((ROOT / 'languages/pt/data/pt87_audit.json').read_text())


def test_exact_manifest_protections_and_scope():
    data = audit()
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-87')
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    guards = {int(e['offset'], 16): e['expected'] for e in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in data['entries']] == manifest
    assert len(manifest) == 300
    assert [r['index'] for r in data['entries'] if r['status'] == 'exception'] == [43, 44, 90, 151, 194, 199]
    for row in data['entries']:
        offset = int(row['offset'], 16)
        assert row['reason']
        if row['status'] == 'exception':
            assert not row['references']
            assert offset not in texts and offset not in guards
        else:
            assert texts[offset] == _normalize_text(row['portuguese'])
            assert guards[offset] == row['portuguese']
            assert row['references']


@pytest.mark.parametrize('index', range(300))
def test_exact_commands_and_layout(index):
    row = audit()['entries'][index]
    if row['status'] == 'exception':
        assert row['reason']
        return
    text = row['portuguese'].replace(r'\n', '\n')
    raw = TextEncoder.encode_pokemon(text, strict=True)
    def commands(data):
        return [c for c in _extract_control_sequences_from_raw(data) if c[0] != 0xFE]
    assert commands(raw) == commands(bytes.fromhex(row['source_hex']))
    assert raw[-1] == 255 and 255 not in raw[:-1]
    assert len(raw) == row['encoded_bytes']
    assert line_widths(text) == row['line_widths']
    assert max(row['line_widths']) <= row['max_width']
    parts = re.split(r'(<0xF[AB]>)', text)
    if row['kind'] in ('mission_description', 'description'):
        assert len(parts) == 1 and text.count('\n') <= 2
        assert row['max_width'] == 172
    else:
        assert all(p.count('\n') <= 1 for p in parts[::2])
        assert all('\n' not in parts[j] for j in range(2, len(parts), 2) if parts[j - 1] == '<0xFA>')
    if row['status'] == 'retained_english':
        assert raw == bytes.fromhex(row['source_hex'])


def test_domain_rules_and_untruncated_dialogue_endings():
    rows = audit()['entries']
    prose = lambda i: rows[i]['portuguese'].replace(r'\n', ' ')
    assert 'Ferrothorn' in prose(24) and 'enfeite!' in prose(24)
    assert 'melhores Pokémon' in prose(28) and 'o que me diz?' in prose(28)
    assert 'orbe raro' in prose(143) and 'Dialga' in prose(143)
    assert 'conhecimento' in prose(139) and 'emoção' in prose(139) and 'força de vontade' in prose(139)
    for i, number in ((124, '3'), (125, '2')):
        assert number in prose(i) and 'Cave of Being' in prose(i)
    assert 'Gelo' in prose(240) and 'Fada' in prose(240) and 'armazém oeste' in prose(240)
    assert 'Moomoo Milk' in prose(166) and 'um ano' in prose(166)
    assert 'não tem volta' in prose(282).lower() and 'outra saída' in prose(282)
    assert 'Graveler' in prose(280) and 'esqueceu Dig' in prose(280)
    assert 'movimento novo' in prose(280)
    assert prose(150) == 'Dialga desapareceu no tempo.'
    assert 'chorar' in prose(177) and 'mãe' in prose(177)
    assert 'não causariam' not in prose(188)
    assert 'e a mim' in prose(223)
    assert rows[45]['portuguese'].startswith('<0x00>')
    assert not rows[46]['portuguese'].startswith('<0x00>')


def test_female_possessive_is_contextual_and_uses_protected_source():
    data = audit()
    override = data['contextual_possessive']
    assert override['pointer'] == 0x1EAB936
    assert override['source_offset'] == '0x1fa7652'
    assert override['translation_offset'] == '0x1fa7656'
    assert data['entries'][191]['portuguese'] == 'ela'
    assert data['entries'][192]['portuguese'] == 'sua'
    assert 'mãe' in data['entries'][177]['portuguese']


def test_shared_title_preimage_and_translations_keep_the_same_prefix():
    data = audit()
    prefix, suffix = data['entries'][45:47]
    assert data['shared_title']['prefix_offset'] == prefix['offset']
    assert data['shared_title']['suffix_offset'] == suffix['offset']
    assert bytes.fromhex(prefix['source_hex']) == b'\x00' + bytes.fromhex(suffix['source_hex'])
    assert TextEncoder.encode_pokemon(prefix['portuguese'], strict=True) == b'\x00' + TextEncoder.encode_pokemon(
        suffix['portuguese'], strict=True)


def test_finalizer_order_and_disjoint_references():
    patches = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert patches.count('batch_87') == 1
    assert all(patches.index(p) < patches.index('batch_87') for p in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'font', 'repoint_stale'))
    refs = {p for r in audit()['entries'] for p in r['references']}
    for file in (ROOT / 'languages/pt/data').glob('pt*_audit.json'):
        if file.name != 'pt87_audit.json':
            assert not refs.intersection(p for r in json.loads(file.read_text()).get('entries', [])
                                         for p in r.get('references', [])), file


def test_retained_english_is_limited_to_names_and_pokemon_cries():
    """Empêche de livrer une réplique anglaise comme valeur volontairement conservée."""
    rows = audit()['entries']
    expected = {
        'Eldon', '<0xFC><0x01><0x06>Slash!', '<0xFC><0x01><0x04>Uxie!',
        '<0xFC><0x01><0x06>Kyouuun!', '<0xFC><0x01><0x06>Kyuun!',
        '<0xFC><0x01><0x06>Kyauun!', '<0xFC><0x01><0x06>Gugyugubah!',
        'Bessy', 'Clarabelle', 'Dottie', 'Miltank', 'Swizer',
    }

    retained = [row['portuguese'] for row in rows if row['status'] == 'retained_english']

    assert len(retained) == len(expected)
    assert set(retained) == expected
