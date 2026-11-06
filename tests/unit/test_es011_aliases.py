"""Gardes des alias ES-011 et de leurs lignes vides structurelles."""
import json
from pathlib import Path

import pytest

from src.core.item_description_routes import ItemDescriptionRoutes
from src.core.text_aliases import TextAliases
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[2]
CANDIDATES = json.loads((ROOT / 'docs/analysis/es/011_ROUTES.json').read_text())['aliases_candidates']
DUPLICATES = [0x41CE3B, 0x41CEA7, 0x41CF13, 0x41CF4F, 0x41DC45]


def test_all_57_candidates_have_explicit_contracts():
    manifest = json.loads((ROOT / 'languages/es-maint/text_aliases.json').read_text())
    entries = {e['contract_offset']: e for e in manifest['aliases'] + manifest.get('excluded', [])}
    for candidate in CANDIDATES:
        entry = entries[candidate['contract_offset']]
        for field in ('live_offset', 'prefix_hex', 'english_raw_hex', 'pointer_offsets'):
            assert entry[field] == candidate[field]


@pytest.mark.parametrize('key', DUPLICATES)
def test_double_keys_are_always_rejected_even_for_equal_translations(key):
    candidate = next(e for e in CANDIDATES if int(e['contract_offset'], 16) == key)
    live = int(candidate['live_offset'], 16)
    aliases = TextAliases({key: {**candidate, 'live_offset': live}})
    with pytest.raises(ValueError, match='collision'):
        aliases.check_keys({key, live})


@pytest.mark.parametrize('key', [0x41D1FD, 0x41D200, 0x41DC45, 0x41DC48])
def test_dormant_credit_keys_cannot_be_translated(key):
    from tests.unit.test_text_aliases import CONTRACT, rom_fixture
    aliases = TextAliases.load(CONTRACT, rom_fixture())
    with pytest.raises(ValueError, match='dormante'):
        aliases.check_keys({key})


def test_pagination_width_is_opt_in_and_still_bounds_each_line():
    source = TextEncoder.encode_pokemon('A<0xFB>B')
    item = {'offset': 0, 'translation': 'A<0xFB>B', 'english_raw_bytes': source.hex(),
            'strict_encoded_layout': True,
            'layout': {'max_lines': 2, 'max_width': 20, 'allow_pagination': True}}
    assert ItemDescriptionRoutes.normalize(item)['translation'] == 'A<0xFB>B'
    item['layout'].pop('allow_pagination')
    with pytest.raises(ValueError, match='Pagination'):
        ItemDescriptionRoutes.normalize(item)


@pytest.mark.parametrize('key', [int(e['contract_offset'], 16) for e in CANDIDATES])
def test_all_preimages_and_exclusions_reject_drift(key):
    from tests.unit.test_text_aliases import CONTRACT, rom_fixture
    source = bytearray(rom_fixture())
    source[key] ^= 1
    with pytest.raises(ValueError, match='preimage'):
        TextAliases.load(CONTRACT, source)


@pytest.mark.parametrize('position', [0x14BCEC, 0x14E0DC, 0xF3F18, 0xF3F78, 0x41F42C, 0x67E0])
def test_source_and_final_verification_guard_engine_roots(tmp_path, position):
    from tests.unit.test_text_aliases import CONTRACT, rom_fixture
    source = rom_fixture()
    aliases = TextAliases.load(CONTRACT, source)
    altered = bytearray(source)
    altered[position] ^= 1
    with pytest.raises(ValueError, match='racine'):
        TextAliases.load(CONTRACT, altered)
    ready = tmp_path / 'ready.json'
    ready.write_text('{"translations": []}')
    with pytest.raises(ValueError, match='racine'):
        aliases.verify(altered, ready, {})


@pytest.mark.parametrize('translation', ['A<0xFC><0x0B><0x01><0x02><0xFB>',
                                        'A<0xFD><0x03><0xFD><0x02><0xFB>',
                                        'A<0xFD><0x02><0xFD><0x03><0xFA>'])
def test_commands_arguments_buffer_order_and_pagination_are_preserved(translation):
    item = {'offset': 0, 'translation': translation,
            'english_raw_bytes': 'bbfd02fd03fbff', 'preserve_control_flow': True}
    with pytest.raises(ValueError, match='commandes'):
        ItemDescriptionRoutes.normalize(item)


def test_message_page_height_is_checked_independently_of_total_line_count():
    item = {'offset': 0, 'translation': 'A<0xFE>B<0xFE>C<0xFB>D',
            'english_raw_bytes': 'bbfebcfebdfbbeff', 'strict_encoded_layout': True,
            'layout': {'max_width': 208, 'max_lines': 5, 'max_page_lines': 2, 'allow_pagination': True}}
    with pytest.raises(ValueError, match='lignes par page'):
        ItemDescriptionRoutes.normalize(item)


def test_recording_message_native_three_lines_are_not_certified(tmp_path):
    from tests.unit.test_text_aliases import CONTRACT, rom_fixture
    aliases = TextAliases.load(CONTRACT, rom_fixture())
    entry = aliases.entries[0x41CF13]
    raw_text = ''.join(f'<0x{b:02X}>' for b in bytes.fromhex(entry['english_raw_hex'])[:-1])
    ready = tmp_path / 'bad.json'
    ready.write_text(json.dumps({'translations': [{'offset': 0x41CF13, 'translation': raw_text}]}))
    with pytest.raises(ValueError, match='budget'):
        aliases.resolve_json(ready, {0x41CF13})


@pytest.mark.parametrize('key', DUPLICATES)
def test_csv_refuses_each_double_claim_before_reading_sources(tmp_path, key):
    from tests.unit.test_text_aliases import CONTRACT, rom_fixture
    aliases = TextAliases.load(CONTRACT, rom_fixture())
    candidate = next(e for e in CANDIDATES if int(e['contract_offset'], 16) == key)
    with pytest.raises(ValueError, match='collision|dormante'):
        aliases.prepare_csv(tmp_path / 'missing.csv', tmp_path / 'out.csv',
                            {key, int(candidate['live_offset'], 16)},
                            tmp_path / 'missing.json', b'', tmp_path / 'es.json', tmp_path / 'en.json')


@pytest.mark.parametrize('position', [0x41D1FD, 0x41D200, 0x4145C8, 0x41DC48, 0x41DCC8])
def test_final_patches_cannot_change_excluded_credits(tmp_path, position):
    from tests.unit.test_text_aliases import CONTRACT, rom_fixture
    aliases = TextAliases.load(CONTRACT, rom_fixture())
    result = bytearray(rom_fixture())
    result[position] ^= 1
    ready = tmp_path / 'ready.json'
    ready.write_text('{"translations": []}')
    with pytest.raises(ValueError, match='racine'):
        aliases.verify(result, ready, {})
