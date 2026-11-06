"""Préimages contractuelles ES-009, sans revendiquer une livraison de texte."""
import hashlib
import importlib
import json
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / 'docs/analysis/es/009_PREPARATION.json'


def test_es009_preparation_covers_exactly_the_frozen_lot():
    """Aucun oubli, ajout extérieur ou traduction finale fictive."""
    report = json.loads(REPORT.read_text())
    lots = json.loads((ROOT / 'docs/analysis/es/lots.json').read_text())
    contract = next(lot for lot in lots if lot['id'] == 'ES-009')['offsets']
    entries = report['entries']

    assert len(entries) == len({e['offset'] for e in entries}) == 374
    assert {e['offset'] for e in entries} == set(contract)
    assert Counter(e['qualification'] for e in entries) == report['counts']
    assert report['phase'] == 'préparation technique, non livré'
    assert all(e['traduction_finale'] is None for e in entries)
    assert all(e['injection_certifiee'] is False for e in entries)
    assert all(e['justification'] and e['surface_provisoire'] for e in entries)


def test_es009_records_padding_and_formatted_surfaces_separately():
    """Les faux débuts et les arguments de commandes ne deviennent pas du texte."""
    entries = json.loads(REPORT.read_text())['entries']
    by_key = {int(e['offset'], 16): e for e in entries}
    padding = {
        0x4170B9: 0x4170BC, 0x4170DE: 0x4170E0, 0x41712D: 0x417130,
        0x417161: 0x417164, 0x41718B: 0x41718C, 0x4171C9: 0x4171CC,
    }

    for key, live in padding.items():
        entry = by_key[key]
        assert not entry['pointer_sites']
        assert int(entry['autre_cle_vivante_du_lot'], 16) == live
        assert by_key[live]['pointer_sites']
        raw = bytes.fromhex(entry['preimage_en_hex'])
        assert raw[:live - key] == bytes(live - key)
        assert raw[live - key:].hex() == by_key[live]['preimage_en_hex']
    assert sum(any(s.startswith('fc13') for s in e['commandes_parseur_hex'])
               for e in entries) == 34
    assert sum(any(s.startswith('f7') for s in e['commandes_parseur_hex'])
               for e in entries) == 7
    assert by_key[0x416EC6]['commandes_parseur_hex'] == [
        'fc080f', 'fc080f', 'fc080f', 'fc080f', 'fc080f',
        'fc103100', 'fb', 'fd02', 'fe', 'fd03', 'fb', 'fc09',
    ]
    assert max(e['octets_avec_ff'] for e in entries) == 159


@pytest.mark.rom
def test_es009_source_preimages_and_all_pointer_occurrences():
    """Relit les deux ROMs et vérifie toutes les occurrences binaires annoncées."""
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
        assert len(raw) == entry['octets_avec_ff']
        assert raw[-1] == 0xFF
        sequences = builder._extract_control_sequences_from_raw(raw, include_breaks=True)
        assert [bytes(s).hex() for s in sequences] == entry['commandes_parseur_hex']
        for target in [entry, *entry['voisins_references']]:
            address = int(target['offset'], 16)
            needle = (address + 0x08000000).to_bytes(4, 'little')
            actual = []
            site = english.find(needle)
            while site >= 0:
                actual.append(f'0x{site:08X}')
                site = english.find(needle, site + 1)
            assert actual == target['pointer_sites'], target['offset']
        match = entry['offset_map']
        if match and match.get('spanish_offset') is not None:
            es_offset = match['spanish_offset']
            es_raw = bytes.fromhex(entry['es_map_hex'])
            assert spanish[es_offset:es_offset + len(es_raw)] == es_raw
    for table in report['tables_candidates']:
        start = int(table['base'], 16)
        raw = bytes.fromhex(table['hex'])
        assert english[start:start + len(raw)] == raw
