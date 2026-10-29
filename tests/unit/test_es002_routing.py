"""Contrats ES-002 sur préimages réelles, sans écrire de traduction source."""
import json
from pathlib import Path

import pytest

from src.core.item_description_routes import SystemTextRoutes
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder
from src.core.text_reinserter import SmartReinserter

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = json.loads((ROOT / 'tests/unit/fixtures/es002_routing.json').read_text())
CONTRACT = ROOT / 'languages/es-maint/system_texts.json'


def source_rom():
    rom = bytearray(FIXTURE['rom_size'])
    for part in FIXTURE['slices']:
        raw = bytes.fromhex(part['hex'])
        rom[part['offset']:part['offset']+len(raw)] = raw
    rom[-4096:] = b'\xff' * 4096
    return rom


def test_system_pages_survive_real_json_and_insertion(tmp_path):
    source = source_rom()
    routes = SystemTextRoutes.load(CONTRACT, source)
    combined = {int(e['offset'], 16): e['traduction'].replace('\\n', '\n')
                for e in FIXTURE['entries'] if int(e['offset'], 16) in routes.entries}
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': []}))

    routes.enrich_json(path, combined)
    rom = bytearray(source)
    inserter = SmartReinserter(rom, allow_relocate=True, skip_encode_aliases=SPANISH_GLYPH_CHARS)
    for item in json.loads(path.read_text())['translations']:
        normalized = routes.normalize(item)
        assert normalized['translation'] == combined[item['offset']]
        assert inserter.reinsert_text(normalized)
    inserter.flush_relocations()
    routes.verify(rom, path)

    assert len(routes.entries) == 4
    for key, entry in routes.entries.items():
        expected = TextEncoder.encode_pokemon(combined[key], skip_aliases=SPANISH_GLYPH_CHARS)
        for site in entry['pointer_offsets']:
            live = int.from_bytes(rom[site:site+4], 'little') - 0x08000000
            assert rom[live:live+len(expected)] == expected
        end = key + len(bytes.fromhex(entry['source_hex']))
        assert rom[key-1] == source[key-1]
        assert rom[end:end+16] == source[end:end+16]
    assert len(bytes.fromhex(routes.entries[0x1BDBF8]['source_hex'])) == 743


@pytest.mark.parametrize('mutation', ['preimage', 'pointer', 'extra_pointer', 'duplicate', 'opcode'])
def test_system_routes_reject_ambiguity(tmp_path, mutation):
    source = source_rom()
    data = json.loads(CONTRACT.read_text())
    entry = data['entries'][0]
    if mutation == 'preimage':
        source[int(entry['offset'], 16)] ^= 1
    elif mutation == 'pointer':
        source[entry['pointer_offsets'][0]] ^= 1
    elif mutation == 'extra_pointer':
        source[16:20] = (int(entry['offset'],16)+0x08000000).to_bytes(4,'little')
    elif mutation == 'opcode':
        source[0x1BB9F2] ^= 1
    else:
        data['entries'].append(entry)
    path = tmp_path / 'contract.json'
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        SystemTextRoutes.load(path, source)


def test_system_route_rejects_lost_scroll(tmp_path):
    routes = SystemTextRoutes.load(CONTRACT, source_rom())
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': []}))
    with pytest.raises(ValueError, match='commandes'):
        routes.enrich_json(path, {0x1BC7E2: 'ONE\nTWO'})


def test_only_maintained_es_inline_consumes_the_delivery_json(tmp_path, monkeypatch):
    from dataclasses import replace

    from scripts import build_language as driver
    calls = []
    monkeypatch.setattr(driver, 'run', lambda command: calls.append([str(x) for x in command]))
    ready = tmp_path / 'ready.json'
    for language in ['es-maint', 'it', 'de']:
        calls.clear()
        config = replace(driver.load_registry().get(language), patches=['inline'])
        driver.apply_patches(config, tmp_path / 'copy.gba', ready, 0)
        command = calls[0]
        assert ('--translations' in command) == (language == 'es-maint')
        assert ('--no-template-fallback' in command) == (language == 'es-maint')
        if language == 'es-maint':
            assert command[command.index('--translations')+1] == str(ready)


def test_system_routes_are_opt_in_and_trainer_pass_is_reused():
    from src.i18n import load_registry
    registry = load_registry()
    assert registry.get('es-maint').system_texts == 'languages/es-maint/system_texts.json'
    assert registry.get('es-maint').patches.count('trainer_class_names_it') == 1
    assert all(not c.system_texts for c in registry if c.code != 'es-maint')


def test_five_prepared_classes_fit_and_preserve_all_other_bytes():
    from scripts.patch_trainer_class_names_it import patch
    rom = source_rom()
    before = bytes(rom)
    combined = {int(e['offset'],16): e['traduction'] for e in FIXTURE['entries'] if 'cellule' in e}

    stats = patch(rom, combined)

    assert stats['written'] == 5 and stats['overflow'] == 0
    expected = bytearray(before)
    for offset, text in combined.items():
        encoded = TextEncoder.encode_pokemon(text)
        assert len(encoded) <= 13
        expected[offset:offset+13] = encoded + bytes(13-len(encoded))
    assert rom == expected


def test_system_final_verification_rejects_silent_fallback(tmp_path):
    source = source_rom()
    routes = SystemTextRoutes.load(CONTRACT, source)
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': []}))
    routes.enrich_json(path, {0x1BC7E2: 'TEST\nSECOND<0xFA>THIRD'})
    with pytest.raises(ValueError, match='non injectée'):
        routes.verify(source, path)


def test_inline_without_delivery_json_fails_explicitly(tmp_path):
    from dataclasses import replace

    from scripts import build_language as driver
    config = replace(driver.load_registry().get('es-maint'), patches=['inline'])
    with pytest.raises(ValueError, match='JSON de livraison requis'):
        driver.apply_patches(config, tmp_path / 'copy.gba')


def test_inline_cli_preserves_six_delivered_source_spans_and_excluded_neighbour(tmp_path, monkeypatch):
    import sys

    from scripts import apply_inline_overrides_fr as inline
    from src.core.text_codec import TextDecoder

    source = source_rom()
    source_path = tmp_path / 'source.gba'
    target = tmp_path / 'built.gba'
    source_path.write_bytes(source)
    target.write_bytes(source)
    extracts, delivered, lines = [], [], []
    for entry in FIXTURE['neighbours']:
        offset = entry['offset']
        end = source.index(255, offset) + 1
        raw = bytes(source[offset:end])
        text = TextDecoder.decode_pokemon(raw, preserve_unknown=True)
        extracts.append({'offset': offset, 'raw_bytes': raw.hex(), 'byte_length': len(raw),
                         'decoded_text': text, 'encoding': 'pokemon'})
        delivered.append({'offset': offset, 'translation': 'TEST', 'original_text': text})
        lines.append(f'0x{offset:08X}: TEST\n')
    combined = tmp_path / 'combined.txt'
    combined.write_text(''.join(lines))
    extraction = tmp_path / 'extracted.json'
    extraction.write_text(json.dumps({'texts': extracts}))
    ready = tmp_path / 'ready.json'
    ready.write_text(json.dumps({'translations': delivered}))
    monkeypatch.setattr(sys, 'argv', ['inline', '--source', str(source_path), '--rom', str(target),
        '--combined', str(combined), '--reference-texts', str(extraction),
        '--english-texts', str(extraction), '--translations', str(ready),
        '--collision-guard', '--no-template-fallback'])

    assert inline.main() == 0

    assert target.read_bytes() == source
    assert target.read_bytes()[0x237503] == source[0x237503] != 0xFF
