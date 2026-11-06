"""Sept menus : vrai CSV/JSON/builder/patches, sans traduction de production."""
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

from scripts import build_language as driver
from src.core.text_aliases import TextAliases
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder
from src.i18n import load_registry

ROOT = Path(__file__).resolve().parents[3]
KEYS = {0x415D45, 0x415D4F, 0x415D5E, 0x415D77, 0x415D8A, 0x4160F9, 0x416101}
pytestmark = [pytest.mark.rom, pytest.mark.slow]


def prepare_probe(tmp_path: Path) -> dict:
    """Construit une sonde temporaire, compare toutes les écritures autorisées."""
    source = driver.ENGLISH_ROM.read_bytes()
    aliases = TextAliases.load(ROOT / 'languages/es-maint/text_aliases.json', source)
    records = {key: aliases.entries[key] for key in KEYS}
    # Un caractère supplémentaire impose la relocation, sans confondre
    # arguments F8 et lettres ni prétendre livrer la traduction finale.
    combined_map = {key: 'Z' + ''.join(f'<0x{b:02X}>' for b in bytes.fromhex(entry['english_raw_hex'])[:-1])
                    for key, entry in records.items()}
    protected = list((ROOT / 'languages').glob('*/combined_*.txt'))
    protected += list((ROOT / 'languages').glob('*/protected_entries.yaml'))
    protected += [ROOT / 'docs/analysis/es/lots.json', ROOT / 'languages/es-maint/glossary.md']
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    combined = tmp_path / 'combined.txt'
    combined.write_text(''.join(f'0x{k:08X}: {v}\n' for k, v in combined_map.items()))
    config = replace(load_registry().get('es-maint'), code='es008-alias-probe',
                     combined=str(combined), output_rom='GenedRom-es008-alias-probe.gba')
    ready = driver.generate_translation_json(config)
    items = json.loads(ready.read_text())['translations']
    assert {item['contract_offset'] for item in items} == KEYS
    for item in items:
        assert not item['allow_fallback'] and not item['allow_truncate']
        assert item['preserve_control_flow']
    output = driver.build_rom(config, ready)
    actual = output.read_bytes()
    expected = bytearray(source)
    allowed = []
    observations = []
    for key, entry in sorted(records.items()):
        encoded = TextEncoder.encode_pokemon(combined_map[key], skip_aliases=SPANISH_GLYPH_CHARS)
        targets = set()
        for ref in entry['pointer_offsets']:
            target = int.from_bytes(actual[ref:ref + 4], 'little') - 0x08000000
            assert target not in (key, entry['live_offset'])
            assert actual[target:target + len(encoded)] == encoded
            expected[ref:ref + 4] = actual[ref:ref + 4]
            expected[target:target + len(encoded)] = encoded
            allowed.extend([(ref, ref + 4), (target, target + len(encoded))])
            targets.add(target)
        assert len(targets) == 1
        observations.append({'key': key, 'live': entry['live_offset'], 'pointers': entry['pointer_offsets'],
                                 'expected_hex': encoded.hex(), 'layout': entry.get('layout'), 'target': targets.pop()})
    assert actual == expected, 'Écriture hors sélection avant patches'
    aliases.verify(actual, ready, combined_map)
    driver.apply_patches(replace(config, code='es-maint'), output, ready, build_number=0)
    actual = output.read_bytes()
    aliases.verify(actual, ready, combined_map)
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
    for key, entry in records.items():
        end = entry['live_offset'] + len(bytes.fromhex(entry['english_raw_hex']))
        assert actual[key:end] == source[key:end], 'Préfixe ou voisin modifié'
    assert {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in protected} == before
    report = {'rom': str(output), 'records': observations, 'consumers': sum(len(e['pointer_offsets']) for e in records.values()),
                  'sha256': hashlib.sha256(actual).hexdigest()}
    path = ROOT / 'output/reports/es008-alias-probe.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + '\n')
    return report


def test_seven_aliases_reach_every_consumer_without_other_writes(tmp_path):
    try:
        report = prepare_probe(tmp_path)
        assert len(report['records']) == 7
        assert report['consumers'] == 14
    finally:
        for suffix in ('translation_ready.json', 'trilingual_translation.csv', 'alias_base.csv'):
            (driver.TRANSLATION_DIR / f'es008-alias-probe_{suffix}').unlink(missing_ok=True)
