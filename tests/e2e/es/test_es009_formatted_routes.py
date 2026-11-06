"""ES-009 : chaîne CSV → JSON → builder → patches, sources temporaires seules."""
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

from scripts import build_language as driver
from src.core.item_description_routes import SystemTextRoutes
from src.core.text_codec import TextEncoder
from src.i18n import load_registry

ROOT = Path(__file__).resolve().parents[3]
pytestmark = [pytest.mark.rom, pytest.mark.slow]


def prepare_probe(tmp_path: Path) -> dict:
    """Force la relocation sans changer noms, prix, nombres ou commandes source."""
    source = driver.ENGLISH_ROM.read_bytes()
    config = load_registry().get('es-maint')
    routes = SystemTextRoutes.load(ROOT / config.system_texts, source)
    entries = {key: entry for key, entry in routes.entries.items()
               if entry.get('layout', {}).get('engine_layout')}
    assert len(entries) == 26
    combined_map = {key: ''.join(f'<0x{b:02X}>' for b in bytes.fromhex(e['source_hex'])[:-1])
                    for key, e in entries.items()}
    for key in (0x41825C, 0x418433, 0x418443):
        combined_map[key] = '<0xF7><0x00>!'
    protected = list((ROOT / 'languages').glob('*/combined_*.txt'))
    protected += list((ROOT / 'languages').glob('*/protected_entries.yaml'))
    protected += [ROOT / 'docs/analysis/es/lots.json', ROOT / 'languages/es-maint/glossary.md']
    hashes = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    combined = tmp_path / 'combined.txt'
    combined.write_text(''.join(f'0x{k:08X}: {v}\n' for k, v in combined_map.items()))
    config = replace(config, code='es009-formatted-probe', combined=str(combined),
                     output_rom='GenedRom-es009-formatted-probe.gba')
    ready = driver.generate_translation_json(config)
    payload = json.loads(ready.read_text())
    assert {item['offset'] for item in payload['translations']} == entries.keys()
    for item in payload['translations']:
        assert item['allow_fallback'] is False and item['allow_truncate'] is False
        assert item['strict_encoded_layout'] is True
        # Réduit seulement la capacité des cellules de la sonde. Le contenu et
        # les consommateurs viennent du vrai CSV enrichi par SystemTextRoutes.
        item.update(original_length=1, max_length=1, padding_available=0)
    ready.write_text(json.dumps(payload))
    output = driver.build_rom(config, ready)
    actual = output.read_bytes()
    expected = bytearray(source)
    allowed = []
    records = []
    for key, entry in sorted(entries.items()):
        raw = TextEncoder.encode_pokemon(combined_map[key])
        targets = set()
        for ref in entry['pointer_offsets']:
            target = int.from_bytes(actual[ref:ref + 4], 'little') - 0x08000000
            assert target != key
            assert actual[target:target + len(raw)] == raw
            expected[ref:ref + 4] = actual[ref:ref + 4]
            expected[target:target + len(raw)] = raw
            allowed.extend([(ref, ref + 4), (target, target + len(raw))])
            targets.add(target)
        assert len(targets) == 1
        records.append({'key': key, 'pointers': entry['pointer_offsets'],
                        'target': targets.pop(), 'expected_hex': raw.hex(), 'source_hex': entry['source_hex'], 'layout': entry['layout']})
    assert actual == expected, 'Écriture hors sélection avant patches'
    routes.verify(actual, ready, combined_map)
    driver.apply_patches(replace(config, code='es-maint'), output, ready, build_number=0)
    actual = output.read_bytes()
    routes.verify(actual, ready, combined_map)
    empty = tmp_path / 'empty.txt'
    empty.write_text('')
    empty_json = tmp_path / 'empty.json'
    empty_json.write_text('{"translations": [], "total_translations": 0}')
    baseline = tmp_path / 'baseline.gba'
    baseline.write_bytes(source)
    driver.apply_patches(replace(config, code='es-maint', combined=str(empty)), baseline, empty_json, build_number=0)
    expected = bytearray(baseline.read_bytes())
    for start, end in allowed:
        expected[start:end] = actual[start:end]
    assert actual == expected, 'Écriture hors sélection après patches'
    for key, entry in entries.items():
        assert actual[key-3:key+len(bytes.fromhex(entry['source_hex']))+3] == source[key-3:key+len(bytes.fromhex(entry['source_hex']))+3]
    for site in (0x3BFC8A, 0x40F1AA, 0x1AAA166, 0x1BB7B57, 0x1DA2F35):
        assert actual[site-3:site+7] == source[site-3:site+7]
    assert {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in protected} == hashes
    report = {'groups': json.loads((ROOT / 'docs/analysis/es/009_FORMATTED.json').read_text())['price']['groups'], 'rom': str(output), 'records': records,
              'consumers': sum(len(e['pointer_offsets']) for e in entries.values()),
              'sha256': hashlib.sha256(actual).hexdigest()}
    path = ROOT / 'output/reports/es009-formatted-probe.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + '\n')
    return report


def test_every_formatted_consumer_and_all_postpatch_bytes(tmp_path):
    try:
        report = prepare_probe(tmp_path)
        assert len(report['records']) == 26
    finally:
        for suffix in ('translation_ready.json', 'trilingual_translation.csv', 'alias_base.csv'):
            (driver.TRANSLATION_DIR / f'es009-formatted-probe_{suffix}').unlink(missing_ok=True)
