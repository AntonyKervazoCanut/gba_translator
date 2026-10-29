"""Certification binaire du lot fermé ES-003, après tous les patches."""
import json
from pathlib import Path

import pytest

from scripts.audit_translation_coverage import parse_combined

ROOT = Path(__file__).resolve().parents[3]
REPORT = json.loads((ROOT / 'docs/analysis/es/003_TRAITEMENT.json').read_text())
pytestmark = pytest.mark.rom


def test_every_contract_offset_has_one_final_decision():
    lots = json.loads((ROOT / 'docs/analysis/es/lots.json').read_text())
    contract = {int(o, 16) for lot in lots if lot['id'] == 'ES-003' for o in lot['offsets']}
    records = REPORT['entries']
    offsets = [int(e['offset'], 16) for e in records]
    assert len(offsets) == len(set(offsets)) == 374
    assert set(offsets) == contract
    assert sum(REPORT['counts'].values()) == 374
    combined = parse_combined(ROOT / 'languages/es-maint/combined_es-maint.txt')
    assert contract & combined.keys() == {
        int(e['offset'], 16) for e in records if e['decision'] == 'traduit'
    }


def test_translations_reach_all_frozen_consumers_after_patches():
    rom = (ROOT / 'output/roms/GenedRom-es-maint.gba').read_bytes()
    aliases = json.loads((ROOT / 'languages/es-maint/text_aliases.json').read_text())['aliases']
    by_key = {int(e['contract_offset'], 16): e for e in aliases}
    for entry in REPORT['entries']:
        if entry['decision'] != 'traduit':
            continue
        key = int(entry['offset'], 16)
        expected = bytes.fromhex(entry['expected_hex'])
        assert len(expected) <= 512
        assert entry['source_commands'] == entry['final_commands']
        assert max(entry['widths_px_with_ten_wide_glyph_buffers']) <= 192
        sites = [int(p, 16) for p in entry['pointer_sites']]
        targets = [int.from_bytes(rom[p:p + 4], 'little') - 0x08000000 for p in sites] if sites else [key]
        for target in targets:
            assert 0 <= target <= len(rom) - len(expected), entry['offset']
            assert rom[target:target + len(expected)] == expected, entry['offset']
        if key in by_key:
            alias = by_key[key]
            live = int(alias['live_offset'], 16)
            if key == 0x24F20D:
                # Le préfixe 000000 est le padding de ICE. HIELO utilise deux
                # de ces octets, sans atteindre le début vivant de DRAGÓN.
                assert rom[0x24F209:live] == bytes.fromhex('c2c3bfc6c9ff00')
            else:
                assert rom[key:live] == bytes.fromhex(alias['prefix_hex'])
        if 0x23E558 <= key < 0x23EAC7:
            assert (key - 0x23E558) % 13 == 0
            assert len(expected) <= 13
            assert set(rom[key + len(expected):key + 13]) <= {0x00, 0xFF}
        if 0x3D4F26 <= key <= 0x3D56C2:
            assert len(expected.split(b'\xfe')) <= 3
            assert b'\xfa' not in expected and b'\xfb' not in expected
    # Ce suffixe est consommé derrière une structure FC0300, sans pointeur direct.
    expected = bytes.fromhex(next(e['expected_hex'] for e in REPORT['entries'] if e['offset'] == '0x0026D4E5'))
    for site in (0x26D3C6, 0x26D3E4):
        target = int.from_bytes(rom[site:site + 4], 'little') - 0x08000000
        assert rom[target:target + 6] == bytes.fromhex('00fc03000000')
        assert rom[target + 6:target + 6 + len(expected)] == expected


def test_conserved_records_and_binary_exclusions_stay_unchanged():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    rom = (ROOT / 'output/roms/GenedRom-es-maint.gba').read_bytes()
    for entry in REPORT['entries']:
        if entry['decision'] in ('traduit', 'exclu_fragment'):
            continue
        offset = int(entry['offset'], 16)
        raw = bytes.fromhex(entry['preimage_en_hex'])
        assert source[offset:offset + len(raw)] == raw, entry['offset']
        assert rom[offset:offset + len(raw)] == raw, entry['offset']
    for site in (0xD80A0, 0x11B4B4):
        assert int.from_bytes(rom[site:site + 4], 'little') == 0x0823E558
