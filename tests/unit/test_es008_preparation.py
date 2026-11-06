"""Préparation ES-008 : contrat fermé et preuves binaires, sans livraison déclarée."""
import hashlib
import importlib
import json
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / 'docs/analysis/es/008_PREPARATION.json'


def test_es008_preparation_covers_the_contract_without_claiming_delivery():
    """Chaque clé reste comptée, y compris les faux débuts d'extraction."""
    report = json.loads(REPORT.read_text())
    lots = json.loads((ROOT / 'docs/analysis/es/lots.json').read_text())
    contract = next(lot for lot in lots if lot['id'] == 'ES-008')['offsets']
    entries = report['entries']

    assert len(entries) == len({entry['offset'] for entry in entries}) == 373
    assert {entry['offset'] for entry in entries} == set(contract)
    assert Counter(entry['qualification'] for entry in entries) == report['counts']
    assert report['phase'] == 'préparation technique, non livré'
    assert all(entry['traduction_finale'] is None for entry in entries)
    assert all(entry['injection_certifiee'] is False for entry in entries)
    assert all(entry['justification'] and entry['surface_provisoire'] for entry in entries)


@pytest.mark.rom
def test_es008_preimages_references_and_commands_match_source_roms():
    """Vérifie toutes les références aux clés et les arguments de commandes."""
    report = json.loads(REPORT.read_text())
    english = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    spanish = (ROOT / 'input/roms/spanishrom.gba').read_bytes()
    builder = importlib.import_module(
        'src.translators.19_build_translated_rom_generic').TranslatedROMBuilder

    assert hashlib.sha256(english).hexdigest() == report['source_sha256']
    assert hashlib.sha256(spanish).hexdigest() == report['es_sha256']
    for entry in report['entries']:
        offset = int(entry['offset'], 16)
        raw = bytes.fromhex(entry['preimage_en_hex'])
        assert english[offset:offset + len(raw)] == raw, entry['offset']
        assert raw[-1] == 0xFF
        assert len(raw) == entry['octets_avec_ff']
        commands = builder._extract_control_sequences_from_raw(raw, include_breaks=True)
        assert [bytes(sequence).hex() for sequence in commands] == entry['commandes_completes_hex']
        for target in [entry, *entry['voisins_references']]:
            address = int(target['offset'], 16)
            needle = (address + 0x08000000).to_bytes(4, 'little')
            actual = []
            site = english.find(needle)
            while site >= 0:
                actual.append(f'0x{site:08X}')
                site = english.find(needle, site + 1)
            assert actual == target['pointer_sites'], target['offset']
        mapping = entry['offset_map']
        if mapping and mapping.get('spanish_offset') is not None:
            es_offset = mapping['spanish_offset']
            es_raw = bytes.fromhex(entry['es_map_hex'])
            assert spanish[es_offset:es_offset + len(es_raw)] == es_raw


def test_es008_records_live_menu_starts_and_missing_english_inventory():
    """Les aides et le cri Pokédex ne deviennent pas des exclusions arbitraires."""
    entries = {int(e['offset'], 16): e for e in json.loads(REPORT.read_text())['entries']}
    starts = {
        0x415D45: 0x415D48, 0x415D4F: 0x415D50, 0x415D5E: 0x415D60,
        0x415D77: 0x415D78, 0x415D8A: 0x415D8C,
        0x4160F9: 0x4160FC, 0x416101: 0x416104,
    }

    for key, live in starts.items():
        record = entries[key]
        assert not record['pointer_sites']
        assert any(int(candidate['offset'], 16) == live and candidate['pointer_sites']
                   for candidate in record['voisins_references'])
    cry = entries[0x415FAD]
    assert cry['inventaire']['en'] == ''
    assert cry['preimage_en_hex'] == 'f804bde6edff'
    assert cry['pointer_sites'] == ['0x00105FE4', '0x001067B8']
    assert cry['commandes_completes_hex'] == ['f804']
