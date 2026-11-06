"""ES-011 : pipeline réel limité aux 302 textes et comparaison intégrale des écritures."""
import json
from dataclasses import replace
from pathlib import Path

import pytest

from scripts import build_language as driver
from src.core.item_description_routes import SystemTextRoutes
from src.core.text_aliases import TextAliases
from src.i18n import load_registry

ROOT = Path(__file__).resolve().parents[3]
pytestmark = [pytest.mark.rom, pytest.mark.slow]


@pytest.fixture
def clean_pipeline_artifacts():
    """Nettoie les vues temporaires même si une assertion échoue."""
    yield
    for suffix in ('translation_ready.json', 'trilingual_translation.csv', 'alias_base.csv'):
        (driver.TRANSLATION_DIR / f'es011-translation-probe_{suffix}').unlink(missing_ok=True)


def test_es011_selected_pipeline_has_exact_readers_and_no_foreign_writes(tmp_path, clean_pipeline_artifacts):
    report = json.loads((ROOT / 'docs/analysis/es/011_TRAITEMENT.json').read_text())
    records = [row for row in report['entries'] if 'texte' in row]
    selected = tmp_path / 'combined.txt'
    selected.write_text(''.join(row['offset'] + ': ' + row['texte'].replace('\n', r'\n') + '\n' for row in records))
    config = replace(load_registry().get('es-maint'), code='es011-translation-probe',
                     combined=str(selected), output_rom='GenedRom-es011-translation-probe.gba')
    source = driver.ENGLISH_ROM.read_bytes()
    ready = driver.generate_translation_json(config)
    items = json.loads(ready.read_text())['translations']

    assert len(items) == 302
    assert {item.get('contract_offset', item['offset']) for item in items} == {int(row['offset'], 16) for row in records}
    assert all(not item['allow_fallback'] and not item['allow_truncate'] for item in items)
    output = driver.build_rom(config, ready)
    actual = output.read_bytes()
    expected = bytearray(source)
    spans = []
    for row in records:
        encoded = bytes.fromhex(row['encoded_hex'])
        for reference in row['references']:
            ref = int(reference, 16)
            target = int.from_bytes(actual[ref:ref + 4], 'little') - 0x08000000
            assert actual[target:target + len(encoded)] == encoded, row['offset']
            expected[ref:ref + 4] = actual[ref:ref + 4]
            expected[target:target + len(encoded)] = encoded
            spans.extend([(ref, ref + 4), (target, target + len(encoded))])
    assert actual == expected, 'Écriture hors du lot avant patches'
    driver.apply_patches(replace(config, code='es-maint'), output, ready, build_number=0)
    actual = output.read_bytes()
    empty = tmp_path / 'empty.txt'
    empty.write_text('')
    empty_json = tmp_path / 'empty.json'
    empty_json.write_text('{"translations": [], "total_translations": 0}')
    baseline = tmp_path / 'baseline.gba'
    baseline.write_bytes(source)
    driver.apply_patches(replace(config, code='es-maint', combined=str(empty)), baseline, empty_json, build_number=0)
    expected = bytearray(baseline.read_bytes())
    for start, end in spans:
        expected[start:end] = actual[start:end]
    assert actual == expected, 'Écriture hors du lot après patches'
    combined = {int(row['offset'], 16): row['texte'] for row in records}
    TextAliases.load(ROOT / config.text_aliases, source).verify(actual, ready, combined)
    SystemTextRoutes.load(ROOT / config.system_texts, source).verify(actual, ready, combined)
