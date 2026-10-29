"""B-686 : périmètre, budgets et commandes des 97 offsets pokedex-01."""
import importlib
import json
import re
from pathlib import Path

import pytest

from scripts.apply_inline_overrides_fr import _load_combined, _normalize_text
from src.core.dialogue_linewrap import line_width
from src.core.text_codec import GERMAN_UMLAUT_CHARS, TextDecoder, TextEncoder

ROOT = Path(__file__).resolve().parents[3]
OFFSETS = tuple(int(value, 16) for value in ["447800", "44A0C1", "44C1F5", "44C5FD", "44CAD6", "44D92A", "44DCC3", "452FCB", "453010", "454284", "4542BC", "4542F3", "454398", "454625", "45465A", "454789", "4547B7", "454BFD", "454C31", "454C68", "454CA2", "454CDB", "454D13", "454D4A", "454F02", "454F2D", "454F5A", "454F86", "454FB2", "454FE1", "455010", "45503E", "45506E", "45509A", "4550C8", "4550F3", "455121", "45514E", "45517B", "4551A7", "4551D4", "455200", "45522C", "455259", "455287", "4552B3", "4552DF", "45530B", "455336", "455362", "455392", "4553C1", "4553F2", "455424", "455453", "455483", "4554B0", "4554E3", "455515", "455548", "455573", "45559E", "4555C9", "4555F4", "45561F", "45564A", "455675", "4556A0", "4556CB", "4566C8", "4566E8", "456708", "456728", "45687C", "45689C", "4568BC", "4568DC", "4571B7", "45749D", "4574C1", "4574E9", "4577B9", "4577F5", "457950", "4579BC", "457A70", "457B2A", "457B4C", "457D44", "457E28", "457E41", "458FC6", "45934B", "459378", "4593D3", "459541", "459561"])


def test_decorations_fit_three_short_lines():
    texts, _ = _load_combined(ROOT / 'languages/de/combined_de.txt')
    decorations = [offset for offset in OFFSETS if 0x454284 <= offset <= 0x4556CB]
    assert len(decorations) == 60
    for offset in decorations:
        lines = texts[offset].split('\n')
        assert len(lines) <= 3
        assert max(map(line_width, lines)) <= 110, hex(offset)


def test_trade_preserves_level_then_species_and_clear_positions():
    texts, _ = _load_combined(ROOT / 'languages/de/combined_de.txt')
    assert re.findall(r'<0xF7><0x([0-9A-F]{2})>', texts[0x457D44]) == ['00', '01', '02', '03']
    assert texts[0x457D44].count('<0xFB>') == 2
    expanded = re.sub(r'<0xF7><0x0[02]>', '100', texts[0x457D44])
    expanded = re.sub(r'<0xF7><0x0[13]>', 'W' * 12, expanded)
    for page in expanded.split('<0xFB>'):
        assert line_width(page.replace('\n', ' ')) <= 192
    assert re.findall(r'<0xFC><0x13><0x([0-9A-F]{2})>', texts[0x459378]) == ['3C', '6E', 'C6']


def test_qualification_covers_exactly_the_ticket():
    report = json.loads((ROOT / 'docs/analysis/686_POKEDEX_01_DE.json').read_text())
    texts, _ = _load_combined(ROOT / 'languages/de/combined_de.txt')
    offsets = [int(entry['offset'], 16) for entry in report['entries']]
    assert len(offsets) == len(set(offsets)) == 97
    assert set(offsets) == set(OFFSETS)
    assert all(entry['decision'] and entry['motif'] for entry in report['entries'])
    assert sum(len(entry['references']) for entry in report['entries']) == 76
    for entry in report['entries']:
        assert entry['de_final_source'] == texts.get(int(entry['offset'], 16))
        assert all(target['controls_match_source'] for target in entry['final'])


@pytest.mark.rom
def test_corrected_texts_are_reached_in_final_rom():
    import yaml
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    final = (ROOT / 'output/roms/GenedRom-de.gba').read_bytes()
    manifest = yaml.safe_load((ROOT / 'languages/de/protected_entries.yaml').read_text())
    entries = [entry for entry in manifest['entries'] if entry['name'].startswith('B-686 ')]
    builder = importlib.import_module('src.translators.19_build_translated_rom_generic').TranslatedROMBuilder
    assert len(OFFSETS) == len(set(OFFSETS)) == 97
    assert len(entries) == 67
    # Coïncidences binaires : ne jamais réécrire ces instructions/données
    # comme s'il s'agissait de références à une chaîne.
    for false_reference in (0x146B64, 0xCBA129):
        assert final[false_reference:false_reference + 4] == source[false_reference:false_reference + 4]
    for entry in entries:
        offset = int(entry['offset'], 16)
        assert offset in OFFSETS
        needle = (offset + 0x08000000).to_bytes(4, 'little')
        refs = [match.start() for match in re.finditer(re.escape(needle), source)]
        if offset < 0x450000:
            refs = [ref for ref in refs if 0x1A35800 <= ref < 0x1A3ABB0
                    and (ref - 0x1A35800) % 36 == 0]
        elif offset <= 0x4556CB:
            refs = [ref for ref in refs if 0x455730 <= ref <= 0x456610
                    and (ref - 0x455730) % 32 == 0]
        assert refs, hex(offset)
        expected = TextEncoder.encode_pokemon(_normalize_text(entry['expected']), skip_aliases=GERMAN_UMLAUT_CHARS)
        original = source[offset:source.index(255, offset) + 1]
        for ref in refs:
            target = int.from_bytes(final[ref:ref + 4], 'little') - 0x08000000
            assert 0 <= target < len(final), (hex(offset), hex(ref))
            actual = final[target:final.index(255, target) + 1]
            if offset <= 0x4556CB:
                lines = TextDecoder.decode_pokemon(actual).split('\n')
                assert len(lines) <= 3
                budget = 232 if offset < 0x450000 else 110
                assert max(map(line_width, lines)) <= budget, hex(offset)
            # La passe Pokédex peut uniquement déplacer les sauts de ligne.
            assert actual.replace(b'\xfe', b'\x00') == expected.replace(b'\xfe', b'\x00'), (hex(offset), hex(ref), actual.hex())
            assert builder._extract_control_sequences_from_raw(actual) == builder._extract_control_sequences_from_raw(original), hex(offset)
