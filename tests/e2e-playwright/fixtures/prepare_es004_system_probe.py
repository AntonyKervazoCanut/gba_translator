"""Sentinelles structurées ES-004 par le pipeline réel et comparaison ROM entière."""
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


def main() -> None:
    """Vérifie les 89 clés, les relocations et les structures après les patches."""
    source = driver.ENGLISH_ROM.read_bytes()
    routes = SystemTextRoutes.load(ROOT / 'languages/es-maint/system_texts.json', source)
    keys = [int(e['offset'], 16) for e in json.loads(
        (ROOT / 'tests/unit/fixtures/es004_system_contract.json').read_text())['entries']]
    combined_map = {key: ('ZREZA' if key == 0x3DF7E8 else f'{n:02d}áéíóúüñ¡¿')
                    for n, key in enumerate(keys)}
    with tempfile.TemporaryDirectory(prefix='f1035-system-') as directory:
        combined = Path(directory) / 'combined.txt'
        combined.write_text(''.join(f'0x{key:08X}: {text}\n' for key, text in combined_map.items()))
        config = replace(driver.load_registry().get('es-maint'), code='es-maint-system-probe',
                         combined=str(combined), output_rom='GenedRom-es004-system-probe.gba')
        ready = driver.generate_translation_json(config)
        output = driver.build_rom(config, ready)
        result = output.read_bytes()
        expected = bytearray(source)
        allowed = []
        relocated = 0
        for key, text in combined_map.items():
            raw = TextEncoder.encode_pokemon(text, skip_aliases=SPANISH_GLYPH_CHARS)
            entry = routes.entries[key]
            if entry.get('fixed_capacity'):
                allowed.append((key, key+len(raw)))
                expected[key:key+len(raw)] = raw
            else:
                for ref in entry['pointer_offsets']:
                    target = int.from_bytes(result[ref:ref+4], 'little')-0x08000000
                    relocated += target != key
                    expected[ref:ref+4] = result[ref:ref+4]
                    expected[target:target+len(raw)] = raw
                    allowed.extend([(ref, ref+4), (target, target+len(raw))])
        assert relocated > 0
        assert result == expected, 'Écriture hors des plages sélectionnées avant patches'
        routes.verify(result, ready, combined_map)
        driver.apply_patches(replace(config, code='es-maint'), output, ready, build_number=0)
        result = output.read_bytes()
        routes.verify(result, ready, combined_map)
        empty = Path(directory) / 'empty.txt'
        empty.write_text('')
        empty_json = Path(directory) / 'empty.json'
        empty_json.write_text('{"translations": [], "total_translations": 0}')
        baseline = Path(directory) / 'baseline.gba'
        baseline.write_bytes(source)
        driver.apply_patches(replace(config, code='es-maint', combined=str(empty)),
                             baseline, empty_json, build_number=0)
        expected = bytearray(baseline.read_bytes())
        for start, end in allowed:
            expected[start:end] = result[start:end]
        assert result == expected, 'Écriture hors sélection après patches'
        print(f'ES004 : 89 mots vérifiés, {relocated} relocations, ROM entière identique hors sélection')


if __name__ == '__main__':
    try:
        main()
    finally:
        for suffix in ['translation_ready.json', 'trilingual_translation.csv', 'alias_base.csv']:
            (driver.TRANSLATION_DIR / f'es-maint-system-probe_{suffix}').unlink(missing_ok=True)
