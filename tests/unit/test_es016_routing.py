"""Contrats ES-016 : seuls les consommateurs moteur prouvés sont inscriptibles."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KEYS = {0x772093, 0x781278, 0x781668, 0x788255, 0x78C2A8, 0x78C2FD}
DUPLICATES = {0x7808DD: 0x7808DE, 0x788537: 0x788538, 0x78D43D: 0x78D43E}


def test_es016_only_proven_live_consumers_are_enabled():
    contract = json.loads((ROOT / 'languages/es-maint/text_aliases.json').read_text())
    entries = {int(e['contract_offset'], 16): e for e in contract['aliases']}
    assert KEYS <= entries.keys()
    assert not (DUPLICATES.keys() | {0x780E33}) & entries.keys()
    preserved = {int(e['offset'], 16): e for e in contract['preserved_sources']}
    assert KEYS | DUPLICATES.keys() | set(DUPLICATES.values()) <= preserved.keys()
    assert all(preserved[key]['nontext'] for key in DUPLICATES)
    assert 0x780E33 in {int(e['contract_offset'], 16) for e in contract['excluded']}


def test_dormant_move_table_is_not_the_active_consumer():
    from tests.unit.test_text_aliases import rom_fixture
    source = rom_fixture()
    for root in (0xE5440, 0x137BC8, 0x9F3B64):
        assert int.from_bytes(source[root:root+4], 'little') == 0x0899F194
    assert int.from_bytes(source[0x9047D0:0x9047D4], 'little') == 0x08780E34
    assert int.from_bytes(source[0x99F964:0x99F968], 'little') == 0x08A3A6D6
    assert source[0x780E34:0x780E8C] != source[0xA3A6D6:0xA3A72E]


def test_duplicate_false_starts_and_dormant_description_fail_closed(tmp_path):
    import pytest

    from src.core.text_aliases import TextAliases
    from tests.unit.test_text_aliases import CONTRACT, rom_fixture
    aliases = TextAliases.load(CONTRACT, rom_fixture())
    path = tmp_path / 'ready.json'
    for key in (0x780E33, 0x780E34):
        with pytest.raises(ValueError, match='exclue'):
            aliases.check_keys({key})
    for prefix, live in DUPLICATES.items():
        for keys in ({prefix}, {prefix, live}):
            path.write_text(json.dumps({'translations': [{'offset': k, 'translation': 'TEST'} for k in keys]}))
            with pytest.raises(ValueError, match='hors écriture'):
                aliases.resolve_json(path, keys)
    for key in KEYS:
        with pytest.raises(ValueError, match='collision'):
            aliases.check_keys({key, key+1})


def test_every_alias_preserves_full_source_and_only_repoints_qualified_sites(tmp_path):
    from src.core.text_aliases import TextAliases
    from src.core.text_codec import TextEncoder
    from src.core.text_reinserter import SmartReinserter
    from tests.unit.test_text_aliases import CONTRACT, rom_fixture
    source = rom_fixture()
    aliases = TextAliases.load(CONTRACT, source)
    combined = {}
    for key in KEYS:
        raw = bytes.fromhex(aliases.entries[key]['english_raw_hex'])
        combined[key] = ''.join(f'<0x{b:02X}>' for b in raw[:-1])
    combined[0x781278] = 'TEST\nTEST\nTEST'
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': [{'offset': k, 'translation': v} for k, v in combined.items()]}))
    aliases.resolve_json(path, KEYS)
    items = json.loads(path.read_text())['translations']
    rom = bytearray(source)
    rom[-4096:] = b'\xff'*4096
    expected = bytearray(rom)
    inserter = SmartReinserter(rom, allow_relocate=True)
    for item in items:
        assert item['force_relocation'] and item['contract_offset'] in KEYS
        assert not item['allow_fallback'] and not item['allow_truncate']
        assert inserter.reinsert_text(item)
    inserter.flush_relocations()
    for item in items:
        encoded = TextEncoder.encode_pokemon(item['translation'])
        for site in item['pointer_offsets']:
            target = int.from_bytes(rom[site:site+4], 'little')-0x08000000
            assert target != item['offset']
            expected[site:site+4] = rom[site:site+4]
            expected[target:target+len(encoded)] = encoded
    assert rom == expected
    aliases.verify(rom, path, combined)


def test_object_and_dialogue_layouts_refuse_overflow_and_lost_arguments(tmp_path):
    import pytest

    from src.core.text_aliases import TextAliases
    from tests.unit.test_text_aliases import CONTRACT, rom_fixture
    aliases = TextAliases.load(CONTRACT, rom_fixture())
    path = tmp_path / 'ready.json'
    for key, text in [(0x781278, 'W'*40), (0x781278, 'A\nB\nC\nD'),
                      (0x781668, 'A\nB<0xFD><0x01>.'),
                      (0x781668, 'A\n'+'W'*30+'<0xFD><0x02>.'),
                      (0x788255, 'A\nB\nC'), (0x772093, 'A')]:
        path.write_text(json.dumps({'translations': [{'offset': key, 'translation': text}]}))
        with pytest.raises(ValueError):
            aliases.resolve_json(path, {key})
