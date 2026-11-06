"""ES-004 : préimages, consommateurs vivants et isolation du vrai pipeline."""
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

from scripts import build_language as driver
from src.core.font_glyphs import LATIN_FONTS
from src.core.item_description_routes import ItemDescriptionRoutes, SystemTextRoutes

ROOT = Path(__file__).resolve().parents[3]
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def delivery():
    report = json.loads((ROOT / 'docs/analysis/es/004_TRAITEMENT.json').read_text())
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-es-maint.gba').read_bytes()
    assert hashlib.sha256(source).hexdigest() == report['source_sha256']
    spanish = (ROOT / 'input/roms/spanishrom.gba').read_bytes()
    assert hashlib.sha256(spanish).hexdigest() == report['es_sha256']
    return report['entries'], source, built, spanish


def test_every_live_consumer_receives_the_complete_spanish_value(delivery):
    rows, source, built, spanish = delivery
    for row in rows:
        key = int(row['offset'], 16)
        original = bytes.fromhex(row['preimage_en_hex'])
        assert source[key:key + len(original)] == original
        if row['es_map_offset'] is not None:
            es_key = int(row['es_map_offset'], 16)
            expected_es = bytes.fromhex(row['es_map_hex'])
            assert spanish[es_key:es_key + len(expected_es)] == expected_es
        if row['value'] is None:
            assert built[key:key + len(original)] == original
            for ref in row['pointer_sites']:
                site = int(ref, 16)
                assert built[site:site + 4] == source[site:site + 4]
            continue
        expected = bytes.fromhex(row['encoded_hex'])
        sites = [key] if row['fixed_capacity'] else row['pointer_offsets']
        for site in sites:
            target = key if row['fixed_capacity'] else int.from_bytes(built[site:site + 4], 'little') - 0x08000000
            assert built[target:target + len(expected)] == expected, (row['offset'], hex(site))


def test_roots_metadata_and_fixed_berry_neighbors_are_preserved(delivery):
    _, source, built, _ = delivery
    for filename, cls in [('item_descriptions', ItemDescriptionRoutes), ('system_texts', SystemTextRoutes)]:
        routes = cls.load(ROOT / f'languages/es-maint/{filename}.json', source)
        routes.verify_guards(built, routes.guards)
    assert built[0x3DF7EF:0x3DF804] == source[0x3DF7EF:0x3DF804]
    for site in (0x9C77C, 0x14E294):
        assert built[site:site + 4] == source[site:site + 4]


def test_actual_font_metrics_fit_every_final_line(delivery):
    rows, _, built, _ = delivery
    for row in rows:
        if row['value'] is None:
            continue
        raw = bytes.fromhex(row['encoded_hex'])
        assert not set(raw[:-1]) & {0xF7, 0xF8, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD, 0xFF}
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            for line in raw[:-1].split(b'\xfe'):
                assert sum(built[widths + code] for code in line) <= row['layout']['max_width'], row['offset']


@pytest.mark.slow
def test_final_values_use_the_real_pipeline_without_any_unselected_write(delivery, tmp_path):
    rows, source, _, _ = delivery
    active = [row for row in rows if row['value'] is not None]
    combined = tmp_path / 'combined.txt'
    combined.write_text(''.join(f"{row['offset']}: " + row['value'].replace('\n', r'\n') + '\n'
                                for row in active))
    config = replace(driver.load_registry().get('es-maint'), code='es-maint-f854-probe',
                     combined=str(combined), output_rom='GenedRom-f854-probe.gba')
    try:
        ready = driver.generate_translation_json(config)
        output = driver.build_rom(config, ready)
        result = output.read_bytes()
        expected = bytearray(source)
        allowed = []
        for row in active:
            key = int(row['offset'], 16)
            raw = bytes.fromhex(row['encoded_hex'])
            if row['fixed_capacity']:
                expected[key:key + len(raw)] = raw
                allowed.append((key, key + len(raw)))
            else:
                for site in row['pointer_offsets']:
                    target = int.from_bytes(result[site:site + 4], 'little') - 0x08000000
                    expected[site:site + 4] = result[site:site + 4]
                    expected[target:target + len(raw)] = raw
                    allowed.extend([(site, site + 4), (target, target + len(raw))])
        assert result == expected, 'Écriture hors du lot avant les patches'
        driver.apply_patches(replace(config, code='es-maint'), output, ready, build_number=0)
        result = output.read_bytes()
        empty = tmp_path / 'empty.txt'
        empty.write_text('')
        empty_json = tmp_path / 'empty.json'
        empty_json.write_text('{"translations": [], "total_translations": 0}')
        baseline = tmp_path / 'baseline.gba'
        baseline.write_bytes(source)
        driver.apply_patches(replace(config, code='es-maint', combined=str(empty)),
                             baseline, empty_json, build_number=0)
        expected = bytearray(baseline.read_bytes())
        for start, end in allowed:
            expected[start:end] = result[start:end]
        assert result == expected, 'Écriture hors du lot après les patches'
        combined_map = {int(row['offset'], 16): row['value'] for row in active}
        for filename, cls in [('item_descriptions', ItemDescriptionRoutes), ('system_texts', SystemTextRoutes)]:
            cls.load(ROOT / f'languages/es-maint/{filename}.json', source).verify(result, ready, combined_map)
    finally:
        for suffix in ('translation_ready.json', 'trilingual_translation.csv', 'alias_base.csv'):
            (driver.TRANSLATION_DIR / f'{config.code}_{suffix}').unlink(missing_ok=True)
