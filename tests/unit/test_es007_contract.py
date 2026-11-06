"""Garde les traductions ES-007 et leurs compositions statistiques."""
import importlib
import json
import re
from pathlib import Path

import pytest

from scripts.audit_translation_coverage import parse_combined
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder

ROOT = Path(__file__).resolve().parents[2]
REPORT = json.loads((ROOT / 'docs/analysis/es/007_TRAITEMENT.json').read_text())
BUILDER = importlib.import_module('src.translators.19_build_translated_rom_generic').TranslatedROMBuilder


def test_contract_is_exhaustive_and_pending_work_is_explicit() -> None:
    """Le rapport couvre aussi les noms, buffers et fragments conservés."""
    lot = next(e for e in json.loads((ROOT / 'docs/analysis/es/lots.json').read_text())
               if e['id'] == 'ES-007')
    records = REPORT['entries']
    assert len(records) == len({e['offset'] for e in records}) == 374
    assert {e['offset'] for e in records} == set(lot['offsets'])
    assert sum(REPORT['counts'].values()) == 374
    assert REPORT['counts'] == {'traduit': 332, 'conserve_sans_reference': 19,
                                'conserve_nom': 9, 'conserve_buffer': 4, 'exclu_fragment': 10}
    assert all(e['justification'] and e['zone'] for e in records)
    combined = parse_combined(ROOT / 'languages/es-maint/combined_es-maint.txt')
    assert set(combined) & {int(o, 16) for o in lot['offsets']} == {
        int(e['offset'], 16) for e in records if e['decision'] == 'traduit'
    }


@pytest.mark.parametrize('entry', REPORT['entries'], ids=lambda e: e['offset'])
def test_complete_commands_and_byte_budgets(entry: dict) -> None:
    """Compare les arguments, les ruptures FA/FB et la valeur réellement protégée."""
    if entry['decision'] != 'traduit':
        assert 'final_text' not in entry
        return
    source = bytes.fromhex(entry['preimage_en_hex'])
    text = entry['final_text'].replace(r'\n', '\n')
    expected = TextEncoder.encode_pokemon(text, skip_aliases=SPANISH_GLYPH_CHARS)
    assert expected.hex() == entry['expected_hex']
    assert len(expected) <= 512
    assert BUILDER._extract_control_sequences_from_raw(expected) == BUILDER._extract_control_sequences_from_raw(source)
    # Borne de sonde, pas une certification des noms ennemis préfixés ni des
    # mouvements/objets/habilités dynamiques : ces limites restent documentées.
    expanded = re.sub(r'<0xFD><0x[0-9A-Fa-f]{2}>', 'W' * 10, text)
    assert max(line_widths(expanded)) <= 192


def test_community_damage_is_corrected_and_exp_boost_stays_composable() -> None:
    values = parse_combined(ROOT / 'languages/es-maint/combined_es-maint.txt')
    assert values[0x3EED08] == 'Pueblo Bellin'
    assert values[0x3EED22] == 'Pueblo Crater'
    assert values[0x3EEE7C] == 'Bosque Grim'
    assert 'maximiz' in values[0x3FC140]
    assert values[0x3FB283] == '<0x00>un extra de'
    assert 'Mov. Espejo' in values[0x3FCE38]
    assert 'Canto Mortal' in values[0x3FC0EE]
    assert 'debilidad' not in values[0x3FC0EE]
    for offset in (0x3FC483, 0x3FC4AB):
        assert 'Rabia' in values[offset]
        assert 'Rencor' not in values[offset]


@pytest.mark.parametrize('template,verb', [(0x3FCB5F, 'subió'), (0x3FCB6A, 'subió'),
                                          (0x3FCB8F, 'bajó'), (0x3FCB9A, 'bajó')])
@pytest.mark.parametrize('strong', [False, True])
def test_stat_templates_compose_grammatical_phrases(template: int, verb: str, strong: bool) -> None:
    """Le constructeur préfixe l'intensité ; aucun verbe ne doit la suivre."""
    values = parse_combined(ROOT / 'languages/es-maint/combined_es-maint.txt')
    modifier = values[0x3FCB41 if verb == 'subió' else 0x3FCB50] if strong else ''
    suffix = values[0x3FCB4A if verb == 'subió' else 0x3FCB59]
    text = values[template].replace('<0xFD><0x0F>', 'Pikachu').replace('<0xFD><0x10>', 'Pikachu')
    text = text.replace('<0xFD><0x00>', 'Ataque').replace('<0xFD><0x01>', modifier + suffix)
    text = text.replace('<0x00>', ' ').replace(r'\n', '\n')
    assert text == f'¡Pikachu: Ataque\n{verb}' + (' mucho' if strong else '') + '!'


@pytest.mark.parametrize('count', range(4))
def test_perish_count_fits_a_long_wild_name_without_plural_agreement(count: int) -> None:
    """Le compteur reste lisible avec un surnom large et le qualificatif sauvage."""
    values = parse_combined(ROOT / 'languages/es-maint/combined_es-maint.txt')
    text = values[0x3FC0EE].replace('<0xFD><0x0F>', 'W' * 10 + ' salvaje')
    text = text.replace('<0xFD><0x00>', str(count)).replace(r'\n', '\n')
    assert f'Canto Mortal bajó a {count}!' in text
    assert len(text.splitlines()) == 2
    assert max(line_widths(text)) <= 192


def test_live_routes_stay_in_entries_when_concurrent_guards_are_added() -> None:
    """Les jonctions cumulatives ne doivent pas déplacer nos routes dans guards."""
    routes = json.loads((ROOT / 'languages/es-maint/system_texts.json').read_text())
    selected = {int(e['offset'], 16): e for e in REPORT['entries'] if e['decision'] == 'traduit'}
    # FLATTEN conserve sa route normale ; son occurrence audio n'est pas texte.
    expected = set(selected) - {0x3ECAB7}
    actual = {int(e['offset'], 16): e for e in routes['entries'] if int(e['offset'], 16) in selected}
    assert set(actual) == expected
    assert len(actual) == 331
    for offset, route in actual.items():
        assert route['source_hex'] == selected[offset]['preimage_en_hex']
        assert route['pointer_offsets'] == [int(p, 16) for p in selected[offset]['pointer_sites']]
    assert not selected.keys() & {int(e['offset'], 16) for e in routes.get('guards', [])}
