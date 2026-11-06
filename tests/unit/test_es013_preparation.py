"""Garde les preuves ES-013 distinctes d'une traduction réellement livrée."""
import hashlib
import importlib
import json
from collections import Counter
from pathlib import Path

import pytest

from scripts.audit_es013_preparation import pointer_sites

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / 'docs/analysis/es/013_PREPARATION.json'


def test_exact_contract_and_explicit_pending_delivery():
    """Les 374 décisions provisoires ne certifient aucune injection."""
    report = json.loads(REPORT.read_text())
    lots = json.loads((ROOT / 'docs/analysis/es/lots.json').read_text())
    expected = next(lot['offsets'] for lot in lots if lot['id'] == 'ES-013')
    entries = report['entries']

    assert [entry['offset'] for entry in entries] == expected
    assert len(entries) == len({entry['offset'] for entry in entries}) == 374
    assert Counter(entry['qualification'] for entry in entries) == report['counts']
    assert report['phase'] == 'préparation technique, non livré'
    assert all(entry['traduction_finale'] is None for entry in entries)
    assert all(entry['injection_certifiee'] is False for entry in entries)
    assert all(entry['surface_provisoire'] and entry['justification'] for entry in entries)


def test_padding_table_and_nature_false_friends_are_separate():
    """Un faux début, une table ou un argument ne doit pas devenir une phrase."""
    entries = json.loads(REPORT.read_text())['entries']
    by_key = {entry['offset']: entry for entry in entries}
    padding = [entry for entry in entries if entry['qualification'] == 'doublon de remplissage']
    aliases = [entry for entry in entries if entry['qualification'] == 'alias hors clé contractuelle']

    assert len(padding) == 82
    assert len(aliases) == 20
    for entry in padding + aliases:
        assert not entry['pointer_sites']
        assert entry['pointeurs_debut_candidat']
        offset = int(entry['offset'], 16)
        live = int(entry['debut_candidat'], 16)
        raw = bytes.fromhex(entry['preimage_en_hex'])
        assert raw[:live-offset] == bytes(live-offset)
        assert raw[live-offset:].hex() == entry['preimage_vivante_hex']
        assert (entry['debut_candidat'] in by_key) == bool(entry['autre_cle_vivante_du_lot'])
    assert by_key['0x00458314']['preimage_en_hex'].startswith('60824508c0824508')
    assert by_key['0x00458314']['qualification'] == 'table de pointeurs'
    assert by_key['0x00459378']['inventaire']['en'] == ''
    assert by_key['0x00459378']['commandes_parseur_hex'] == ['fc133c', 'fc136e', 'fc13c6']
    assert by_key['0x00459378']['en_vivant_commandes_brutes'] == (
        'Name<0xFC><0x13><0x3C>Wanted<0xFC><0x13><0x6E>Offer<0xFC><0x13><0xC6>Lv.')
    assert by_key['0x00458314']['en_vivant_commandes_brutes'] is None
    assert by_key['0x00458FC6']['commandes_parseur_hex'] == ['f80a', 'f800', 'f801']
    assert by_key['0x00457D44']['commandes_parseur_hex'] == ['fe', 'f700', 'f701', 'fb', 'fe', 'f702', 'f703', 'fb', 'fe']
    assert by_key['0x00463DFE']['traduction_candidate_d849'] == 'Miedosa'
    assert by_key['0x00463E2A']['traduction_candidate_d849'] == 'Mansa'
    assert by_key['0x00463E30']['traduction_candidate_d849'] == 'Tímida'
    assert len([entry for entry in entries if entry['traduction_candidate_d849']]) == 25


def test_routing_reproduction_accounts_for_each_missing_alias():
    """Le blocage documenté concerne exactement les vingt clés, sans lot voisin."""
    report = json.loads(REPORT.read_text())
    expected = {entry['offset'] for entry in report['entries']
                if entry['qualification'] == 'alias hors clé contractuelle'}
    probe = json.loads((ROOT / 'docs/analysis/es/013_ACHEMINEMENT_REPRO.json').read_text())

    assert {entry['offset'] for entry in probe['entries']} == expected
    assert len(probe['entries']) == 20
    assert all(entry['json_entry'] is None for entry in probe['entries'])
    assert all(entry['live_offset_resolved'] is False for entry in probe['entries'])
    assert all(entry['expected_pointer_sites'] for entry in probe['entries'])


@pytest.mark.rom
def test_all_preimages_references_and_offset_map_against_real_sources():
    """Vérifie chaque preuve binaire, y compris les références non alignées."""
    report = json.loads(REPORT.read_text())
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    spanish = (ROOT / 'input/roms/spanishrom.gba').read_bytes()
    builder = importlib.import_module(
        'src.translators.19_build_translated_rom_generic').TranslatedROMBuilder

    assert hashlib.sha256(source).hexdigest() == report['source_sha256']
    assert hashlib.sha256(spanish).hexdigest() == report['es_sha256']
    for entry in report['entries']:
        offset = int(entry['offset'], 16)
        live = int(entry['debut_candidat'], 16)
        raw = bytes.fromhex(entry['preimage_en_hex'])
        live_raw = bytes.fromhex(entry['preimage_vivante_hex'])
        assert source[offset:offset+len(raw)] == raw, entry['offset']
        assert source[live:live+len(live_raw)] == live_raw, entry['offset']
        assert raw[-1] == live_raw[-1] == 255
        assert len(raw) == entry['octets_avec_ff']
        assert pointer_sites(source, offset) == entry['pointer_sites']
        assert pointer_sites(source, live) == entry['pointeurs_debut_candidat']
        sequences = builder._extract_control_sequences_from_raw(live_raw, include_breaks=True)
        assert [bytes(seq).hex() for seq in sequences] == entry['commandes_parseur_hex']
        for match in entry['correspondances_es']:
            target = match['mapping'].get('spanish_offset')
            if target is not None:
                es_raw = bytes.fromhex(match['preimage_hex'])
                assert spanish[target:target+len(es_raw)] == es_raw
                assert pointer_sites(spanish, target) == match['pointer_sites']
    for table in report['preuves_tables']:
        offset = int(table['offset'], 16)
        raw = bytes.fromhex(table['hex'])
        assert source[offset:offset+len(raw)] == raw
        assert pointer_sites(source, offset) == table['pointer_sites']
    # Deux pointeurs par ID : les natures ne sont pas des cellules à écraser.
    natures = [entry for entry in report['entries'] if entry['qualification'] == 'nature']
    for index, entry in enumerate(natures):
        assert entry['pointer_sites'] == [f'0x{0x463E60+4*index:08X}', f'0x{0x1FE65F4+4*index:08X}']
