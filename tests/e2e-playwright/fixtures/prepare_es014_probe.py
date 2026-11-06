"""ES-014 : vrai pipeline sur sentinelles privées et comparaison intégrale."""
import json
import sys
import tempfile
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts import build_language as driver
from src.core.item_description_routes import SystemTextRoutes
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder

VISIBLE = '¡PRUEBA ES 014!\nNiño y pingüino\nPrimera prueba\nSegunda prueba\n¿ÚLTIMA LÍNEA?'
SHARED = '¡PRUEBA ES 014!\nNiño y pingüino\n¿ÚLTIMA LÍNEA?'


def main() -> None:
    """Vérifie chaque consommateur après les patches, sans toucher aux sources."""
    source = driver.ENGLISH_ROM.read_bytes()
    contract = ROOT / 'tests/unit/fixtures/es014_contract.json'
    routes = SystemTextRoutes.load(contract, source)
    translations = {key: '\n'.join([f'{n:03d}'+'i'*25]+['i'*28]*(e.get('layout', {'max_lines': 1})['max_lines']-1))
                    for n, (key, e) in enumerate(routes.entries.items())}
    from importlib import import_module
    builder = import_module('src.translators.19_build_translated_rom_generic').TranslatedROMBuilder
    for key, entry in routes.entries.items():
        if 'layout' not in entry:
            commands = builder._extract_control_sequences_from_raw(bytes.fromhex(entry['source_hex']), include_breaks=True)
            translations[key] = 'PRUEBA ' + ''.join(''.join(f'<0x{b:02X}>' for b in cmd)+'i' for cmd in commands)
    translations[0x482AA0] = VISIBLE
    translations[0x482BD5] = SHARED
    with tempfile.TemporaryDirectory(prefix='f1042-pipeline-') as directory:
        temporary = Path(directory)
        combined = temporary / 'combined.txt'
        combined.write_text(''.join(f'0x{k:08X}: '+v.replace('\n', r'\n')+'\n'
                                   for k, v in translations.items()))
        config = replace(driver.load_registry().get('es-maint'), code='es014-probe',
                         combined=str(combined), output_rom='GenedRom-f1042-sentinel.gba')
        ready = driver.generate_translation_json(config)
        payload = json.loads(ready.read_text())
        assert {i['offset'] for i in payload['translations']} == translations.keys()
        for item in payload['translations']:
            assert item['english_raw_bytes'] == routes.entries[item['offset']]['source_hex']
            assert item['pointer_offsets'] == routes.entries[item['offset']]['pointer_offsets']
            assert item['translation'] == translations[item['offset']]
        rom = driver.build_rom(config, ready)
        result = rom.read_bytes()
        routes.verify(result, ready, translations)
        expected = bytearray(source)
        allowed = []
        relocated = 0
        for key, entry in routes.entries.items():
            raw = TextEncoder.encode_pokemon(translations[key], skip_aliases=SPANISH_GLYPH_CHARS)
            for ref in entry['pointer_offsets']:
                target = int.from_bytes(result[ref:ref+4], 'little')-0x08000000
                if len(raw) > len(bytes.fromhex(entry['source_hex'])):
                    assert target != key
                relocated += target != key
                expected[ref:ref+4] = result[ref:ref+4]
                expected[target:target+len(raw)] = raw
                allowed.extend([(ref, ref+4), (target, target+len(raw))])
        assert result == expected, 'Écriture builder hors sélection'
        assert relocated > 300
        driver.apply_patches(replace(config, code='es-maint'), rom, ready, build_number=0)
        result = rom.read_bytes()
        routes.verify(result, ready, translations)
        baseline = temporary / 'baseline.gba'
        baseline.write_bytes(source)
        empty = temporary / 'empty.txt'
        empty.write_text('')
        empty_json = temporary / 'empty.json'
        empty_json.write_text(json.dumps({'translations': [], 'total_translations': 0}))
        driver.apply_patches(replace(config, code='es-maint', combined=str(empty)),
                             baseline, empty_json, build_number=0)
        expected = bytearray(baseline.read_bytes())
        for start, end in allowed:
            expected[start:end] = result[start:end]
        assert result == expected, 'Écriture post-patches hors sélection'
        for suffix in ['translation_ready.json', 'trilingual_translation.csv', 'alias_base.csv']:
            (driver.TRANSLATION_DIR / f'es014-probe_{suffix}').unlink(missing_ok=True)
        print(f'ES-014 : {len(translations)} chaînes, '
              f'{sum(len(e["pointer_offsets"]) for e in routes.entries.values())} consommateurs, '
              f'{relocated} références relocalisées ; ROM intégralement comparée avant/après patches')


if __name__ == '__main__':
    main()
