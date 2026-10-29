"""Contrat hors réseau du glossaire IT : preuves, jointures et cellules."""

from __future__ import annotations

import csv
import gzip
import hashlib
import io
import json
from pathlib import Path

import pytest
import yaml

from languages.it.patches import cfru_type_names, status_badges, type_icons
from src.text.charmap_data import CHAR_TO_BYTE

ROOT = Path(__file__).resolve().parents[3]
PATH = ROOT / 'languages/it/data/official_terminology.yaml'
REVISION = 'c0a9bc75af3a455cdfa27dde21e4ec95aedd3f25'


@pytest.fixture(scope='module')
def glossary() -> dict:
    """Charge uniquement le fichier versionné, sans accès réseau."""
    return yaml.safe_load(PATH.read_text(encoding='utf-8'))


def test_schema_and_every_category_has_a_sourced_decision(glossary: dict) -> None:
    assert glossary['schema_version'] == 1
    assert glossary['language'] == 'it'
    categories = {'types', 'moves', 'abilities', 'items', 'natures', 'stats',
                  'statuses', 'generic_locations', 'unbound_names'}
    assert set(glossary['category_decisions']) == categories
    for decision in glossary['category_decisions'].values():
        assert isinstance(decision['decision'], str) and decision['decision']
        assert decision['sources']
        assert set(decision['sources']) <= glossary['sources'].keys()
    assert glossary['sources']['pokemon_training']['kind'] == 'official'
    assert glossary['sources']['pokemon_training']['url'].startswith('https://www.pokemon.com/it/')
    for path in glossary['sources']['project']['paths']:
        assert (ROOT / path).is_file()


@pytest.mark.parametrize('stem', ['move_names', 'ability_names', 'item_names',
                                  'type_names', 'nature_names', 'stat_names'])
def test_exact_archived_sources_and_complete_bilingual_derivation(glossary: dict, stem: str) -> None:
    source = glossary['sources']['pokeapi']
    frozen = source['files'][stem + '.csv']
    expected_hashes = json.loads((ROOT / 'docs/analysis/audit_traduction_it_mesures.json').read_text())['pokeapi_hashes']

    raw = gzip.decompress(frozen['raw_gzip'])
    rows = list(csv.DictReader(io.StringIO(raw.decode('utf-8'))))
    grouped = {}
    for row in rows:
        grouped.setdefault(row[next(iter(row))], {})[row['local_language_id']] = row['name']
    variants = {}
    for row in grouped.values():
        if '8' in row and '9' in row:
            variants.setdefault(row['9'], set()).add(row['8'])
    unambiguous = {en: next(iter(names)) for en, names in variants.items() if len(names) == 1}

    assert source['commit'] == REVISION
    assert source['language_ids'] == {'it': 8, 'en': 9}
    assert frozen['url'] == f'https://raw.githubusercontent.com/PokeAPI/pokeapi/{REVISION}/data/v2/csv/{stem}.csv'
    assert hashlib.sha256(raw).hexdigest() == frozen['sha256'] == expected_hashes[stem + '.csv']
    assert frozen['paired_entries'] == len(unambiguous)
    if stem in glossary['bulk_tables']:
        table = glossary['bulk_tables'][stem]
        assert table['source'] == 'pokeapi'
        assert table['source_file'] == stem + '.csv'
        assert table['key'] == 'english_name_not_cfru_index'
        assert table['entries'] == len(unambiguous)
        assert table['official_names'] == unambiguous
    else:
        section = {'type_names': 'types', 'nature_names': 'natures', 'stat_names': 'stats'}[stem]
        actual = dict(glossary[section])
        if stem == 'type_names':
            actual.update(glossary['excluded_types'])
        assert actual == unambiguous
    ambiguous = glossary['ambiguous_names'].get(stem, {})
    assert set(ambiguous) == {en for en, names in variants.items() if len(names) > 1}
    for en, entries in ambiguous.items():
        assert {entry['italian'] for entry in entries} == variants[en]
        for entry in entries:
            assert grouped[str(entry['pokeapi_id'])]['8'] == entry['italian']
            assert grouped[str(entry['pokeapi_id'])]['9'] == en


def test_indices_and_ambiguous_names_cannot_be_used_as_cfru_indices(glossary: dict) -> None:
    matching = glossary['matching']
    assert matching['key'] == 'exact_english_name'
    assert matching['pokeapi_ids_are_cfru_indices'] is False
    assert matching['automatic_replacement'] is False
    assert matching['divergences'] == 503
    assert 'Storage Key' not in glossary['bulk_tables']['item_names']['official_names']
    assert {v['italian'] for v in glossary['ambiguous_names']['item_names']['Storage Key']} == {'Depochiave', 'Chiave magazzino'}
    # Fire Lash a l'index CFRU 587, mais PokeAPI 680 (587 = Fairy Lock).
    moves = glossary['bulk_tables']['move_names']['official_names']
    assert moves['Fire Lash'] == 'Frusta di Fuoco'
    assert moves['Fairy Lock'] == 'Blocco Fatato'


def test_confirmed_ability_decisions_fit_without_changing_live_translation(glossary: dict) -> None:
    expected = {'Cloud Nine': 'Antimeteo', 'Color Change': 'Cambiacolore',
                'Limber': 'Scioltezza', 'Battle Armor': 'Lottascudo'}
    assert glossary['ability_corrections'] == expected
    assert len(glossary['confirmed_discrepancies']) == 4
    for entry in glossary['confirmed_discrepancies']:
        name = entry['official']
        assert name == expected[entry['english']]
        assert name == glossary['bulk_tables']['ability_names']['official_names'][entry['english']]
        encoded = bytes(CHAR_TO_BYTE[c] for c in name) + b'\xff'
        assert len(encoded) <= glossary['constrained_cells']['ability_names']['cell_bytes']


def test_fixed_cell_budgets_and_existing_cfru_display_forms(glossary: dict) -> None:
    policy = glossary['constrained_cells']
    assert policy['fallback_languages'] == []
    for section, budget in [('move_names', 13), ('ability_names', 17), ('item_names', 14),
                            ('species_names', 11), ('trainer_classes', 13)]:
        assert policy[section]['cell_bytes'] == budget
        assert policy[section]['max_glyphs'] == budget - 1
    cells = policy['cfru_type_names']['cells']
    assert len(cells) == len(cfru_type_names.TYPE_PATCHES) + 1
    actual = {(int(c['offset'], 16), c['english'], c['display']) for c in cells}
    assert actual == set(cfru_type_names.TYPE_PATCHES) | {(0x3FE894, 'NORMAL', 'NORMAL')}
    for cell in cells:
        encoded = bytes(CHAR_TO_BYTE[c] for c in cell['display'])
        assert len(encoded) <= cell['max_bytes'] == len(cell['english'])
        assert cell['official'] == next(v for k, v in glossary['types'].items() if k.upper() == cell['english'])
    assert glossary['type_icon_review']['current'] == type_icons.IT_NAME
    assert glossary['types']['Bug'] == 'Coleottero'
    assert glossary['type_icon_review']['current']['Bug'] == 'INSETTO'


def test_badges_distinguish_names_text_and_graphical_slots(glossary: dict) -> None:
    lang = yaml.safe_load((ROOT / 'languages/it/lang.yaml').read_text())
    expected = {'poison': 'PSN', 'burn': 'SCT', 'freeze': 'CON',
                'paralysis': 'PAR', 'sleep': 'SON', 'faint': 'KO'}
    statuses = glossary['statuses']
    assert {k: v['badge'] for k, v in statuses.items()} == lang['status_abbrev'] == expected
    for status in statuses.values():
        assert status['name'] and status['state'] and status['decision']
        assert status['badge_status'] == 'project_convention_not_officially_certified'
        assert set(status['sources']) <= glossary['sources'].keys()
        assert len(bytes(CHAR_TO_BYTE[c] for c in status['badge'])) <= 3
    by_slot = {v['graphics_slot']: v['badge'] for v in statuses.values()}
    for slot, *letters in status_badges._STATUS_PATCHES:
        assert by_slot[slot] == ''.join(letters)
    assert by_slot[status_badges._FNT_SLOT] == 'KO'
    assert by_slot[0] == 'PSN' and by_slot[1] == 'PAR'


def test_core_names_and_editorial_conventions_are_separate(glossary: dict) -> None:
    assert len(glossary['types']) == 18
    assert len(glossary['natures']) == 25
    assert len(glossary['stats']) == 8
    assert glossary['natures']['Quirky'] == 'Furba'
    assert glossary['stats']['Special Attack'] == 'Attacco Speciale'
    assert glossary['stat_display']['Special Attack'] == 'Att. Sp.'
    assert glossary['generic_locations']['Pokémon Center'] == 'Centro Pokémon'
    assert glossary['unbound_names']['source'] == 'project'
    assert glossary['unbound_names']['exceptions'] == {}
