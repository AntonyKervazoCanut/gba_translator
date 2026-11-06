"""Vérifie le périmètre fermé et les préimages de préparation ES-004."""
import hashlib
import json
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / 'docs/analysis/es/004_PREPARATION.json'


def test_preparation_covers_the_exact_contract_without_claiming_delivery():
    """Les fragments restent comptés, sans devenir des traductions inventées."""
    report = json.loads(REPORT.read_text())
    lots = json.loads((ROOT / 'docs/analysis/es/lots.json').read_text())
    contract = next(lot for lot in lots if lot['id'] == 'ES-004')['offsets']
    records = report['entries']
    offsets = [int(entry['offset'], 16) for entry in records]

    assert len(offsets) == len(set(offsets)) == 374
    assert set(offsets) == {int(offset, 16) for offset in contract}
    assert Counter(entry['qualification'] for entry in records) == report['counts']
    assert report['phase'] == 'préparation technique, non livré'
    assert all(entry['traduction_finale'] is None for entry in records)
    assert all(entry['injection_certifiee'] is False for entry in records)
    assert all(entry['justification'] and entry['surface'] for entry in records)
    assert {int(entry['offset'], 16) for entry in records
            if entry['qualification'] == 'fragment'} == {
                0x3D5AB0, 0x3D5AFD, 0x3DDD0B, 0x3DEC2D}


@pytest.mark.rom
def test_preimages_and_all_direct_references_match_the_source_rom():
    """Contrôle les octets réels et toutes les occurrences, pas le vieux CSV."""
    report = json.loads(REPORT.read_text())
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    spanish = (ROOT / 'input/roms/spanishrom.gba').read_bytes()

    assert hashlib.sha256(source).hexdigest() == report['source_sha256']
    assert hashlib.sha256(spanish).hexdigest() == report['es_sha256']
    assert int.from_bytes(source[0x9A8D8:0x9A8DC], 'little') == 0x08876200
    assert int.from_bytes(source[0x9A98C:0x9A990], 'little') == 0x08876200
    assert source[0x9A96C:0x9A990].hex() == report['gitems']['accessor_hex']
    assert int.from_bytes(source[0x3ECEDC:0x3ECEE0], 'little') == 0x083E7FE0
    assert int.from_bytes(source[0x3ECEE4:0x3ECEE8], 'little') == 0x083E8504
    for entry in report['entries']:
        offset = int(entry['offset'], 16)
        raw = bytes.fromhex(entry['preimage_en_hex'])
        assert source[offset:offset + len(raw)] == raw, entry['offset']
        assert raw[-1] == 0xFF
        needle = (offset + 0x08000000).to_bytes(4, 'little')
        actual = []
        site = source.find(needle)
        while site >= 0:
            actual.append(site)
            site = source.find(needle, site + 1)
        assert actual == [int(site, 16) for site in entry['pointer_sites']]
        for item_id in entry['item_ids_cfru_base_876200']:
            assert 0x876214 + 44 * item_id in actual
        if entry['qualification'] == 'mot Easy Chat':
            assert len(actual) == 1
            group = 0x3E7FE0 if offset < 0x3E811D else 0x3E8504
            assert (actual[0] - group) % 12 == 0
            assert actual[0] >= group
        if entry['es_map_offset'] is not None:
            es_offset = int(entry['es_map_offset'], 16)
            es_raw = bytes.fromhex(entry['es_map_hex'])
            assert spanish[es_offset:es_offset + len(es_raw)] == es_raw

