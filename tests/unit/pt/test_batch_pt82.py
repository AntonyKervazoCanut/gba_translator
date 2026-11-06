"""PT-82 : échanges, base de Vivill, cellules Zygarde et défis du Frontier."""
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
AUDIT = json.loads((ROOT / 'languages/pt/data/pt82_audit.json').read_text())
LIVE = [row for row in AUDIT['entries'] if row['status'] != 'exception']
TEXTS, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')


def test_exact_manifest_and_protections():
    manifest = next(batch['offsets'] for batch in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if batch['id'] == 'PT-82')
    guards = {int(entry['offset'], 16): entry['expected'] for entry in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [row['offset'] for row in AUDIT['entries']] == manifest
    assert len(manifest) == 300 and len(LIVE) == 297
    assert [row['index'] for row in AUDIT['entries'] if row['status'] == 'exception'] == [26, 98, 150]
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['reason']
        if row['status'] == 'exception':
            assert not row['references']
            assert offset not in TEXTS and offset not in guards
        else:
            assert TEXTS[offset] == _normalize_text(guards[offset])
            assert guards[offset] == row['portuguese']
            assert row['references']


@pytest.mark.parametrize('row', LIVE, ids=lambda row: row['offset'])
def test_exact_controls_and_layout(row):
    text = TEXTS[int(row['offset'], 16)]
    raw = TextEncoder.encode_pokemon(text, strict=True)
    source_commands = _extract_control_sequences_from_raw(bytes.fromhex(row['source_hex']))
    commands = _extract_control_sequences_from_raw(raw)
    assert [command for command in commands if command[0] != 0xFE] == [
        command for command in source_commands if command[0] != 0xFE]
    assert len(raw) == row['encoded_bytes'] and raw[-1] == 255 and 255 not in raw[:-1]
    assert line_widths(text) == row['line_widths']
    assert max(row['line_widths']) <= row['max_width']
    assert row['max_width'] == (172 if row['index'] in (0, 112) else 192)
    parts = re.split(r'(<0xF[AB]>)', text)
    max_lines = 4 if row['kind'] == 'location_description' else 3 if row['kind'] in ('cell_description', 'description') else 2
    assert all(part.count('\n') < max_lines for part in parts[::2])
    assert all('\n' not in parts[index] for index in range(2, len(parts), 2)
               if parts[index - 1] == '<0xFA>')
    if row['status'] == 'retained_english':
        assert raw == bytes.fromhex(row['source_hex'])


def _prose(index: int) -> str:
    """Retire les commandes pour vérifier le sens indépendamment de l'habillage."""
    text = TEXTS[int(AUDIT['entries'][index]['offset'], 16)]
    return re.sub(r'\s+', ' ', re.sub(r'<0x[0-9A-Fa-f]{2}>', ' ', text)).strip()


def test_trade_records_keep_species_and_received_nicknames():
    for index, species, nickname in ((8, 'Ducklett', 'Quacker'), (10, 'Electrode', 'Roly-Poly'),
                                     (12, 'Hitmontop', 'Top'), (14, 'Pachirisu', 'Squirry'),
                                     (17, 'Shiinotic', 'Shin'), (18, 'Amoonguss', 'Among Them'),
                                     (20, 'Lampent', 'Torch')):
        assert species in _prose(index) and nickname in _prose(index)
    assert 'Alola' in _prose(8)
    assert 'troque' in _prose(2).lower() and 'Borrius' in _prose(2)


def test_password_hints_preserve_letters_and_initial_letter_distinction():
    for index, letter in ((55, 'A'), (56, 'A'), (60, 'K'), (64, 'L'),
                          (67, 'O'), (72, 'O'), (86, 'V')):
        assert f'<0x06>{letter}<0xFC>' in TEXTS[int(AUDIT['entries'][index]['offset'], 16)]
        assert 'senha' in _prose(index)
    assert 'começa' in _prose(56)
    assert 'uma letra' in _prose(55)
    assert 'oito' in _prose(73)
    assert 'Research Lab' in _prose(73) and 'Command Centre' in _prose(73)


def test_zygarde_thresholds_forms_and_ability_changes():
    for index, threshold in ((118, '10'), (121, '10'), (122, '10'), (123, '50'), (143, '10')):
        assert threshold in _prose(index) and 'cento' in _prose(index)
    assert 'todas as células' in _prose(124)
    assert 'permanente' in _prose(124) and 'permanente' in _prose(145)
    assert 'temporári' in _prose(144)
    assert 'Habilidade' in _prose(125) and 'movimentos' in _prose(125)
    assert 'Habilidade' in _prose(132) and 'Habilidade' in _prose(135)
    assert 'desmont' in _prose(149).lower()
    assert 'único' in _prose(151)
    assert 'Cube' in _prose(153)


def test_circus_and_mine_rules_are_complete_beyond_extraction_cap():
    for index in (271, 272, 293):
        text = _prose(index)
        assert 'salv' in text and 'desclassificado' in text
        assert 'continuar' in text and 'Tenha isso em mente!' in text
        assert 'BP' in text
    assert 'três' in _prose(271) and 'quatro' in _prose(271) and 'seis' in _prose(271)
    assert 'dois ou três Pokémon' in _prose(272) and 'Link Cable' in _prose(272)
    assert 'não poderá interromper' in _prose(272)
    assert 'Habilidades' in _prose(282) and 'dano direto' in _prose(282)
    assert 'item terá efeito' in _prose(282)
    assert 'Dynamax' in _prose(293) and 'Batalhas Inversas' in _prose(293)
    assert 'itens minerados' in _prose(293)
    assert 'seis' in _prose(295) and 'todas' in _prose(295)
    assert 'Escavador' in _prose(297) and 'não pode' in _prose(297)
    assert '6' in _prose(299) and 'todas' in _prose(299)


def test_finalizer_after_repairs_and_other_batches_disjoint():
    patches = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert patches.count('batch_82') == 1
    assert all(patches.index(patch) < patches.index('batch_82') for patch in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))
    refs = {ref for row in LIVE for ref in row['references']}
    for file in (ROOT / 'languages/pt/data').glob('pt*_audit.json'):
        if file.name != 'pt82_audit.json':
            assert not refs.intersection(ref for row in json.loads(file.read_text()).get('entries', [])
                                         for ref in row.get('references', [])), file


def test_mission_descriptions_have_explicit_narrow_three_line_layout():
    for index in (0, 112):
        row = AUDIT['entries'][index]
        text = TEXTS[int(row['offset'], 16)]
        assert 1 <= text.count('\n') <= 2
        assert '<0xFA>' not in text and '<0xFB>' not in text
        assert max(line_widths(text)) <= 172
