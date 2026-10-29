"""Contrat hors réseau du glossaire brésilien, sans traduction de masse."""
import re
import struct
from datetime import date
from pathlib import Path

import pytest
import yaml

from languages.fr.patches import status_abbrevs
from src.core.text_codec import POKEMON_TABLE

ROOT = Path(__file__).resolve().parents[3]
CATEGORIES = {'species', 'moves', 'abilities', 'items', 'types', 'natures',
              'stats', 'statuses', 'system', 'borrius_names'}


@pytest.fixture(scope='module')
def glossary():
    return yaml.safe_load((ROOT / 'languages/pt/data/official_terminology.yaml').read_text())


def test_schema_and_decision_evidence(glossary):
    assert glossary['schema_version'] == 1
    assert glossary['language'] == 'pt-BR'
    assert date.fromisoformat(glossary['frozen_on'])
    assert set(glossary['categories']) == CATEGORIES
    for source in glossary['sources'].values():
        assert date.fromisoformat(source['accessed_on'])
        assert source['url'].startswith('https://') or source['kind'] == 'project'
        assert source['locale'] in {'pt-BR', 'en-US', 'project'}
        if source['kind'] == 'project':
            assert (ROOT / source['url']).is_file()
    for category in glossary['categories'].values():
        assert category['fallback'] == 'preserve_english'
        assert category['decision']
        for entry in category['entries'].values():
            assert entry['value'] and entry['evidence']
            assert entry['classification'] in {'official_pt_br', 'retained_english', 'project_choice'}
            assert isinstance(entry['variants'], list)
            for variant in entry['variants']:
                assert variant['value'] and variant['kind'] and variant['reason']
                assert variant['decision'] == 'rejected'
            assert entry['sources'] and set(entry['sources']) <= glossary['sources'].keys()
            if entry['classification'] == 'official_pt_br':
                assert any(glossary['sources'][s]['kind'] == 'official'
                           and glossary['sources'][s]['locale'] == 'pt-BR'
                           for s in entry['sources'])


def test_complete_closed_vocabularies(glossary):
    categories = glossary['categories']
    assert {name: e['value'] for name, e in categories['types']['entries'].items()} == {
        'Normal': 'Normal', 'Fighting': 'Lutador', 'Flying': 'Voador',
        'Poison': 'Venenoso', 'Ground': 'Terrestre', 'Rock': 'Pedra',
        'Bug': 'Inseto', 'Ghost': 'Fantasma', 'Steel': 'Aço', 'Fire': 'Fogo',
        'Water': 'Água', 'Grass': 'Planta', 'Electric': 'Elétrico',
        'Psychic': 'Psíquico', 'Ice': 'Gelo', 'Dragon': 'Dragão',
        'Dark': 'Sombrio', 'Fairy': 'Fada',
    }
    assert set(categories['natures']['entries']) == {
        'Hardy', 'Lonely', 'Brave', 'Adamant', 'Naughty', 'Bold', 'Docile',
        'Relaxed', 'Impish', 'Lax', 'Timid', 'Hasty', 'Serious', 'Jolly',
        'Naive', 'Modest', 'Mild', 'Quiet', 'Bashful', 'Rash', 'Calm',
        'Gentle', 'Sassy', 'Careful', 'Quirky',
    }
    assert set(categories['stats']['entries']) == {'HP', 'Attack', 'Defense',
        'Special Attack', 'Special Defense', 'Speed', 'Accuracy', 'Evasion'}
    assert set(categories['statuses']['entries']) == {'poison', 'burn', 'freeze',
        'paralysis', 'sleep', 'faint', 'confusion'}
    assert categories['abilities']['entries']['Overgrow']['value'] == 'Supercrescimento'
    assert categories['abilities']['entries']['Torrent']['value'] == 'Dilúvio'
    assert categories['types']['entries']['Grass']['value'] == 'Planta'
    assert categories['borrius_names']['entries']['Frozen Heights']['value'] == 'Frozen Heights'
    assert all(e['value'] == name for name, e in categories['natures']['entries'].items())


def test_status_registry_encoding_and_patch_scope(glossary):
    config = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())
    expected = {'poison': 'PSN', 'burn': 'QMD', 'freeze': 'CNG', 'paralysis': 'PAR', 'sleep': 'DRM', 'faint': 'DES'}
    assert config['status_abbrev'] == expected == glossary['status_display']['abbreviations']
    for value in expected.values():
        assert re.fullmatch('[A-Z]{3}', value)
        assert len(bytes(POKEMON_TABLE[c] for c in value)) == 3
    assert glossary['status_display']['faint_applied'] is False
    assert glossary['status_display']['battle_badges_localized'] is False
    patches = status_abbrevs._patches_from_registry(expected)
    assert [(p['index'], p['fr']) for p in patches] == [(0, 'DRM'), (3, 'QMD'), (4, 'CNG')]
    assert 'status_badges' not in config['patches']


def test_patch_follows_live_pointers_without_touching_ko(glossary):
    # Les adresses sont volontairement relogées : le patch doit suivre les pointeurs.
    rom = bytearray(0x420100)
    order = ['sleep', 'poison', 'paralysis', 'burn', 'freeze']
    for index, key in enumerate(order):
        offset = 0x420000 + index * 8
        en = status_abbrevs._EN_STATUS[key][1]
        rom[offset:offset + 4] = status_abbrevs._encode(en) + b'\xff'
        struct.pack_into('<I', rom, status_abbrevs.PTR_TABLE_OFFSET + index * 8,
                         status_abbrevs.GBA_BASE + offset)
    ko_offset = 0x420080
    rom[ko_offset:ko_offset + 3] = status_abbrevs._encode('KO') + b'\xff'
    before = bytes(rom)
    patches = status_abbrevs._patches_from_registry(glossary['status_display']['abbreviations'])
    assert status_abbrevs.apply_to_rom(rom, patches=patches) == 3
    for index, key in enumerate(order):
        offset = 0x420000 + index * 8
        assert rom[offset:offset + 4] == status_abbrevs._encode(
            glossary['status_display']['abbreviations'][key]) + b'\xff'
    changed = {i for i, (a, b) in enumerate(zip(before, rom)) if a != b}
    assert changed <= {0x420000 + index * 8 + j for index in (0, 3, 4) for j in range(3)}
    assert rom[ko_offset:ko_offset + 3] == status_abbrevs._encode('KO') + b'\xff'
    assert status_abbrevs.apply_to_rom(rom, patches=patches) == 0


@pytest.mark.parametrize('font_index,stride,max_width', [(0, 32, 15), (1, 64, 18),
    (2, 64, 18), (3, 64, 18), (4, 64, 18)])
def test_status_glyphs_and_pixel_budget_in_real_fonts(glossary, font_index, stride, max_width):
    font = (ROOT / 'tests/unit/fixtures/pt_fonts' / f'latin_{font_index}.bin').read_bytes()
    for abbreviation in glossary['status_display']['abbreviations'].values():
        codes = [POKEMON_TABLE[c] for c in abbreviation]
        assert sum(font[stride * 256 + code] for code in codes) <= max_width
        for code in codes:
            glyph = font[code * stride:(code + 1) * stride]
            assert any((byte >> shift) & 3 in (1, 2)
                       for byte in glyph for shift in (0, 2, 4, 6))
