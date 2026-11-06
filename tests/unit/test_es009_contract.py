"""Contrat technique ES-009 : portée exacte, limites moteur et refus explicites."""
import json
from pathlib import Path

import pytest

from src.core.item_description_routes import SystemTextRoutes

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / 'tests/unit/fixtures/es009_contract.json'


@pytest.fixture(scope='module')
def source():
    fixture = json.loads((ROOT / 'tests/unit/fixtures/es009_rom.json').read_text())
    data = bytearray(fixture['size'])
    for row in fixture['slices']:
        raw = bytes.fromhex(row['hex'])
        data[row['offset']:row['offset'] + len(raw)] = raw
    return data


@pytest.fixture(scope='module')
def routes(source):
    return SystemTextRoutes.load(CONTRACT, source)


def encode_tokens(raw):
    return ''.join(f'<0x{b:02X}>' for b in raw[:-1])


def test_exact_scope_without_aliases_or_production_translation(routes):
    preparation = json.loads((ROOT / 'docs/analysis/es/009_PREPARATION.json').read_text())
    selected = {int(e['offset'], 16) for e in preparation['entries']
                if any(c.startswith(('fc13', 'f7')) for c in e['commandes_parseur_hex'])}
    parent_only = {0x417CD1, 0x417CE6, 0x417CFF, 0x417D18, 0x417D32}
    assert len(routes.entries) == 26
    assert len(routes.excluded) == 10
    assert routes.entries.keys() | routes.excluded == selected - parent_only
    assert not (routes.entries.keys() & routes.excluded)
    manifest = json.loads((ROOT / 'languages/es-maint/system_texts.json').read_text())
    assert [e for e in manifest['entries'] if int(e['offset'], 16) in selected] == json.loads(CONTRACT.read_text())['entries']


def test_source_prices_and_nicknames_fit_qualified_windows(routes, tmp_path):
    combined = {k: encode_tokens(bytes.fromhex(e['source_hex']))
                for k, e in routes.entries.items() if k not in (0x41825C, 0x418433, 0x418443)}
    path = tmp_path / 'ready.json'
    path.write_text('{"translations": []}')
    routes.enrich_json(path, combined)
    assert len(json.loads(path.read_text())['translations']) == 23


@pytest.mark.parametrize('key', [0x41825C, 0x418433, 0x418443])
def test_source_item_messages_are_not_certified_for_long_buffers(routes, tmp_path, key):
    path = tmp_path / 'ready.json'
    path.write_text('{"translations": []}')
    raw = bytes.fromhex(routes.entries[key]['source_hex'])
    with pytest.raises(ValueError, match='fenêtre'):
        routes.enrich_json(path, {key: encode_tokens(raw)})
    routes.enrich_json(path, {key: '<0xF7><0x00>!'})


@pytest.mark.parametrize('key', [0x4180A7, 0x4180BC, 0x4180D0, 0x4180FA, 0x41810D,
                               0x41811D, 0x41812F, 0x418142, 0x418152, 0x418163])
def test_bypassed_table_cannot_be_injected(routes, tmp_path, key):
    path = tmp_path / 'ready.json'
    path.write_text('{"translations": []}')
    with pytest.raises(ValueError, match='sans injection'):
        routes.enrich_json(path, {key: 'A'})


def test_name_column_is_checked_even_below_total_window_limit(routes, tmp_path):
    key = 0x417984
    raw = bytes.fromhex(routes.entries[key]['source_hex'])
    column = raw.index(b'\xfc\x13')
    path = tmp_path / 'ready.json'
    path.write_text('{"translations": []}')
    with pytest.raises(ValueError, match='colonne'):
        routes.enrich_json(path, {key: 'W' * 15 + encode_tokens(raw[column:])})


def test_engine_guards_are_verified_after_patches_even_without_translation(routes, source, tmp_path):
    path = tmp_path / 'ready.json'
    path.write_text('{"translations": []}')
    changed = bytearray(source)
    changed[0xCB94C] ^= 1
    with pytest.raises(ValueError, match='métadonnées'):
        routes.verify(changed, path, {})


def test_engine_font_preimage_is_required(source, tmp_path):
    changed = bytearray(source)
    changed[0x1FB100] ^= 1
    with pytest.raises(ValueError, match='métadonnées'):
        SystemTextRoutes.load(CONTRACT, changed)


@pytest.mark.rom
def test_fixture_and_engine_evidence_match_pinned_source():
    import hashlib

    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    evidence = json.loads((ROOT / 'docs/analysis/es/009_FORMATTED.json').read_text())
    assert hashlib.sha256(source).hexdigest() == evidence['pc']['source_sha256'] == evidence['price']['sha256']
    fixture = json.loads((ROOT / 'tests/unit/fixtures/es009_rom.json').read_text())
    for row in fixture['slices']:
        raw = bytes.fromhex(row['hex'])
        assert source[row['offset']:row['offset'] + len(raw)] == raw
    scan = evidence['pc']['item_name_scan']
    font = source[0x1FB100:0x1FB300]
    assert len(scan) == 729
    for row in scan:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['hex'])
        assert source[offset:offset + len(raw) + 1] == raw + b'\xff'
        assert row['bytes'] == len(raw)
        assert row['width'] == sum(font[b] for b in raw)
    assert max(r['bytes'] for r in scan) == 17
    assert max(r['width'] for r in scan) == 95
    SystemTextRoutes.load(ROOT / 'languages/es-maint/system_texts.json', source)


@pytest.mark.parametrize('cache_text,remove_layout', [('A', False), ('W' * 100, True)])
def test_final_verification_uses_combined_and_canonical_layout(routes, source, tmp_path, cache_text, remove_layout):
    from src.core.text_codec import TextEncoder

    key = 0x418433
    combined = {key: '<0xF7><0x00>!'}
    path = tmp_path / 'ready.json'
    path.write_text('{"translations": []}')
    routes.enrich_json(path, combined)
    payload = json.loads(path.read_text())
    item = payload['translations'][0]
    item['translation'] = '<0xF7><0x00>' + cache_text
    if remove_layout:
        item.pop('layout')
        item.pop('strict_encoded_layout')
    path.write_text(json.dumps(payload))
    changed = bytearray(source)
    target = 0x1F90000
    raw = TextEncoder.encode_pokemon(item['translation'])
    changed[target:target+len(raw)] = raw
    for pointer in routes.entries[key]['pointer_offsets']:
        changed[pointer:pointer+4] = (0x08000000 + target).to_bytes(4, 'little')
    with pytest.raises(ValueError):
        routes.verify(changed, path, combined)
