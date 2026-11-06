"""ES-009 : livraison réelle, relocation forcée et isolation de la ROM entière."""
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

from scripts import build_language as driver
from scripts.apply_combined_fr import _load_combined
from src.core.item_description_routes import SystemTextRoutes
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder
from src.i18n import load_registry

ROOT = Path(__file__).resolve().parents[3]
pytestmark = [pytest.mark.rom, pytest.mark.slow]
GRAPHIC_SITES = {0x3BFC8A, 0x40F1AA, 0x1AAA166, 0x1BB7B57, 0x1DA2F35}


def test_delivery_reaches_every_final_consumer_without_external_writes(tmp_path: Path):
    """Le vrai CSV et les patches doivent conserver les 337 valeurs complètes."""
    report = json.loads((ROOT / 'docs/analysis/es/009_DELIVERY.json').read_text())
    selected = {int(e['offset'], 16): e for e in report['entries'] if e['translation'] is not None}
    source = driver.ENGLISH_ROM.read_bytes()
    for entry in report['entries']:
        if 'replacement' in entry:
            replacement = entry['replacement']
            site = replacement['site']
            assert int.from_bytes(source[site:site+4], 'little') == 0x08000000 + replacement['target']
        if 'std_id' in entry:
            site = 0x3E06B8 + entry['std_id'] * 4
            assert int.from_bytes(source[site:site+4], 'little') == 0x08000000 + int(entry['offset'], 16)
        for menu in entry.get('menus', []):
            base = int.from_bytes(source[menu['root']:menu['root']+4], 'little') - 0x08000000
            count = source[menu['root']+4]
            assert base <= menu['site'] < base + count*8
            assert (menu['site']-base) % 8 == 0
    config = load_registry().get('es-maint')
    routes = SystemTextRoutes.load(ROOT / config.system_texts, source)
    combined = tmp_path / 'combined.txt'
    combined.write_text(''.join(f"{e['offset']}: {e['translation']}\n" for e in selected.values()))
    mapping, _ = _load_combined(combined)
    config = replace(config, code='es009-delivery-probe', combined=str(combined),
                     output_rom='GenedRom-es009-delivery-probe.gba')
    ready = driver.generate_translation_json(config)
    payload = json.loads(ready.read_text())
    assert {e['offset'] for e in payload['translations']} == selected.keys()
    for item in payload['translations']:
        assert not item['allow_fallback'] and not item['allow_truncate']
        if not routes.entries[item['offset']].get('fixed_capacity'):
            item.update(original_length=1, max_length=1, padding_available=0)
    ready.write_text(json.dumps(payload))
    output = driver.build_rom(config, ready)
    actual = output.read_bytes()
    expected = bytearray(source)
    allowed = set()
    records = []
    glyph_records = []
    for key in sorted(selected):
        entry = routes.entries[key]
        normalized = routes.normalize({'offset': key, 'translation': mapping[key],
                                       'english_raw_bytes': entry['source_hex'],
                                       **routes.layout_metadata(entry)})
        raw = TextEncoder.encode_pokemon(normalized['translation'], skip_aliases=SPANISH_GLYPH_CHARS)
        targets = set()
        refs = [key] if entry.get('fixed_capacity') else entry['pointer_offsets']
        for ref in refs:
            target = key if entry.get('fixed_capacity') else int.from_bytes(actual[ref:ref+4], 'little') - 0x08000000
            assert actual[target:target+len(raw)] == raw, hex(key)
            if not entry.get('fixed_capacity'):
                expected[ref:ref+4] = actual[ref:ref+4]
                allowed.add((ref, ref+4))
                if raw.hex() != entry['source_hex']:
                    assert target != key, hex(key)
            expected[target:target+len(raw)] = raw
            allowed.add((target, target+len(raw)))
            targets.add(target)
        assert len(targets) == 1
        if entry.get('layout', {}).get('engine_layout'):
            record = {'key': key, 'pointers': refs, 'expected_hex': raw.hex(),
                      'target': targets.pop(), 'layout': entry['layout']}
            if key in (0x41825C, 0x418433, 0x418443):
                record['source_hex'] = entry['source_hex']
            records.append(record)
        else:
            glyph_records.append({'key': key, 'target': targets.pop(),
                                  'expected_hex': raw.hex(),
                                  'font': entry.get('layout', {}).get('initial_font'),
                                  'max_width': entry.get('layout', {}).get('max_width', 192),
                                  'max_lines': entry.get('layout', {}).get('max_lines', 2),
                                  'std_id': selected[key].get('std_id')})
    assert actual == expected, 'Écriture hors sélection avant patches'
    routes.verify(actual, ready, mapping)
    driver.apply_patches(replace(config, code='es-maint'), output, ready, build_number=0)
    actual = output.read_bytes()
    routes.verify(actual, ready, mapping)
    empty = tmp_path / 'empty.txt'
    empty.write_text('')
    empty_json = tmp_path / 'empty.json'
    empty_json.write_text('{"translations": []}')
    baseline = tmp_path / 'baseline.gba'
    baseline.write_bytes(source)
    driver.apply_patches(replace(config, code='es-maint', combined=str(empty)), baseline, empty_json, build_number=0)
    expected = bytearray(baseline.read_bytes())
    for start, end in allowed:
        expected[start:end] = actual[start:end]
    assert actual == expected, 'Écriture hors sélection après patches'
    for site in GRAPHIC_SITES:
        assert actual[site-3:site+7] == source[site-3:site+7]
    assert len(records) == 26
    proof = {'rom': str(output), 'records': records, 'glyph_records': glyph_records, 'selected': len(selected),
             'pointer_occurrences': sum(len(e['pointer_offsets']) for e in selected.values()),
             'consumers': sum(site not in GRAPHIC_SITES for e in selected.values()
                              for site in e['pointer_offsets']),
             'sha256': hashlib.sha256(actual).hexdigest()}
    assert proof['pointer_occurrences'] == 614
    assert proof['consumers'] == 609
    path = ROOT / 'output/reports/es009-delivery-probe.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(proof, ensure_ascii=False, indent=2)+'\n')
    for suffix in ('translation_ready.json', 'trilingual_translation.csv', 'alias_base.csv'):
        (driver.TRANSLATION_DIR / f'es009-delivery-probe_{suffix}').unlink(missing_ok=True)


def test_production_rom_at_all_337_contracted_entries():
    """La sonde isolée ne remplace pas la vérification du vrai build es-maint."""
    source = driver.ENGLISH_ROM.read_bytes()
    config = load_registry().get('es-maint')
    routes = SystemTextRoutes.load(ROOT / config.system_texts, source)
    mapping, _ = _load_combined(config.combined_path(ROOT))
    routes.verify(config.output_rom_path(ROOT).read_bytes(), config.translation_json_path(ROOT), mapping)
    report = json.loads((ROOT / 'docs/analysis/es/009_DELIVERY.json').read_text())
    assert sum(bool(mapping.get(int(e['offset'], 16))) for e in report['entries']) == 337
