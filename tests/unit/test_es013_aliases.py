"""Les vingt identifiants ES-013 conservent leurs préfixes et leurs lecteurs."""
import json
from pathlib import Path

from src.core.text_aliases import TextAliases
from tests.unit.test_text_aliases import rom_fixture

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = json.loads((Path(__file__).parent / 'fixtures/text_aliases/es013.json').read_text())


def test_twenty_contractual_aliases_are_routed():
    aliases = TextAliases.load(ROOT / 'languages/es-maint/text_aliases.json', rom_fixture())
    for entry in FIXTURE['aliases']:
        key = int(entry['contract_offset'], 16)
        assert key in aliases.entries
        actual = aliases.entries[key]
        assert actual['live_offset'] == int(entry['live_offset'], 16)
        assert actual['prefix_hex'] == entry['prefix_hex']
        assert actual['english_raw_hex'] == entry['english_raw_hex']
        assert actual['pointer_offsets'] == [int(p, 16) for p in entry['pointer_offsets']]


def test_contractual_starts_cannot_gain_direct_readers():
    import pytest
    for entry in FIXTURE['aliases']:
        rom = bytearray(rom_fixture())
        key = int(entry['contract_offset'], 16)
        rom[0x20:0x24] = (0x08000000 + key).to_bytes(4, 'little')
        with pytest.raises(ValueError, match='direct pointer'):
            TextAliases.load(ROOT / 'languages/es-maint/text_aliases.json', bytes(rom))


def test_each_zero_prefix_and_each_live_pointer_is_required():
    import pytest
    for entry in FIXTURE['aliases']:
        key = int(entry['contract_offset'], 16)
        for site in [key, *(int(p, 16) for p in entry['pointer_offsets'])]:
            rom = bytearray(rom_fixture())
            rom[site] ^= 1
            with pytest.raises(ValueError):
                TextAliases.load(ROOT / 'languages/es-maint/text_aliases.json', bytes(rom))
