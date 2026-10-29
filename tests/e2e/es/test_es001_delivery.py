"""Lot ES-001 dans le vrai JSON, le builder et tous les patches de production."""
import json
from pathlib import Path

import pytest

from scripts import build_language as driver
from src.core.item_description_routes import SystemTextRoutes
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder

ROOT = Path(__file__).resolve().parents[3]
pytestmark = [pytest.mark.rom, pytest.mark.slow]


def test_es001_real_pipeline_and_exact_write_ranges(tmp_path, monkeypatch):
    from dataclasses import replace

    report = json.loads((ROOT / 'docs/analysis/es/0851_ES001_TRAITEMENT.json').read_text())
    source = driver.ENGLISH_ROM.read_bytes()
    selected = [e for e in report['entries'] if e['decision'] == 'traduit_depuis_en']
    combined = tmp_path / 'combined.txt'
    combined.write_text(''.join(e['offset'] + ': ' + e['translation'].replace('\n', r'\n') + '\n'
                                for e in selected))
    original_config = driver.load_registry().get('es-maint')
    config = replace(original_config, output_rom=str(tmp_path / 'es001.gba'),
                     combined=str(combined),
                     text_aliases=str(ROOT / original_config.text_aliases),
                     system_texts=str(ROOT / original_config.system_texts),
                     item_descriptions=str(ROOT / original_config.item_descriptions))
    with monkeypatch.context() as patch:
        patch.setattr(driver, 'REPO_ROOT', tmp_path)
        patch.setattr(driver, 'TRANSLATION_DIR', tmp_path / 'output/translation')
        ready = driver.generate_translation_json(config)
    items = json.loads(ready.read_text())['translations']
    by_key = {e.get('contract_offset', e['offset']): e for e in items}
    assert len(selected) == 350
    assert len(items) == 350
    assert all(int(e['offset'], 16) in by_key for e in selected)
    output = driver.build_rom(config, ready)
    built = output.read_bytes()
    allowed = bytearray(len(source))
    for item in items:
        offset = item['offset']
        original_length = item['original_length'] + 1
        allowed[offset:offset+original_length] = b'\x01' * original_length
        normalized = SystemTextRoutes.normalize(item)
        encoded = TextEncoder.encode_pokemon(normalized['translation'], skip_aliases=SPANISH_GLYPH_CHARS)
        for site in item.get('pointer_offsets', []):
            allowed[site:site+4] = b'\x01' * 4
            target = int.from_bytes(built[site:site+4], 'little') - 0x08000000
            if 0 <= target < len(built):
                allowed[target:target+len(encoded)] = b'\x01' * len(encoded)
    assert not [i for i, (a, b) in enumerate(zip(source, built)) if a != b and not allowed[i]][:20]
    # Inline is a no-op for every delivered text, including relocated short ones.
    driver.apply_patches(replace(config, patches=['inline']), output, ready, build_number=0)
    assert output.read_bytes() == built
    driver.apply_patches(config, output, ready, build_number=0)
    final = output.read_bytes()
    production = original_config.output_rom_path(ROOT).read_bytes()
    for entry in selected:
        expected = bytes.fromhex(entry['encoded_hex'])
        for site_hex in entry['pointers']:
            site = int(site_hex, 16)
            target = int.from_bytes(final[site:site+4], 'little') - 0x08000000
            assert final[target:target+len(expected)] == expected, (entry['offset'], site_hex)
            production_target = int.from_bytes(production[site:site+4], 'little') - 0x08000000
            assert production[production_target:production_target+len(expected)] == expected
        key = int(entry['offset'], 16)
        if key != int(entry['live_offset'], 16):
            assert final[key] == source[key] == 0xAA
    # These are accidental address-like bytes, not executable text consumers.
    # The reviewed translations fit in place; relocation must never mutate them.
    for site in [0x1D9CAFA, 0x16C79CA, 0x176E4D3, 0x21A31, 0x4F9E5, 0x100713C, 0x5CABB2]:
        assert final[site:site+4] == source[site:site+4]
    assert final[0x18D43D] == source[0x18D43D] == 0xAA
