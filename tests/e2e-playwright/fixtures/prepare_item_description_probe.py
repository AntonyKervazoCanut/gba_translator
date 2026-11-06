"""Construit une ROM sentinelle via le vrai pipeline, sans modifier les sources."""
import argparse
import json
import sys
import tempfile
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts import build_language as driver
from src.core.item_description_routes import ItemDescriptionRoutes
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder

MOOMOO_MILK = 0x3D5706
VISIBLE_ES004 = '¡PRUEBA ES 004!\nNiño y pingüino\n¿ÚLTIMA LÍNEA?'


def sentinel(index: int, offset: int = 0, es004: bool = False) -> str:
    """Conserve B-1031 et force des relocations longues pour ES-004."""
    if es004:
        if offset == MOOMOO_MILK:
            return VISIBLE_ES004
        return '\n'.join([f'{index:03d}' + 'i' * 39, 'i' * 42, 'i' * 42])
    lines = [f'TEST ITEM {index:02d}', 'SECOND LINE', 'THIRD LINE']
    return '\n'.join(lines if index == 15 else [line.ljust(32, 'i') for line in lines])


def main() -> None:
    """Vérifie toutes les descriptions, les consommateurs et les patches réels."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--es004', action='store_true')
    args = parser.parse_args()
    source = driver.ENGLISH_ROM.read_bytes()
    routes = ItemDescriptionRoutes.load(
        ROOT / 'languages/es-maint/item_descriptions.json', source
    )
    translations = {key: sentinel(n, key, args.es004) for n, key in enumerate(routes.entries)}
    if args.es004:
        assert len(translations) == 184
        assert {0x3D5934, 0x3D5968, 0x3D5AB8} <= translations.keys()
    with tempfile.TemporaryDirectory(prefix='f1035-sentinel-') as directory:
        temporary = Path(directory)
        combined = temporary / 'combined.txt'
        combined.write_text(''.join(
            f'0x{key:08X}: ' + text.replace('\n', r'\n') + '\n'
            for key, text in translations.items()
        ))
        config = replace(driver.load_registry().get('es-maint'), code='es-maint-probe',
                         combined=str(combined), output_rom=(
                             'GenedRom-f1035-sentinel.gba' if args.es004
                             else 'GenedRom-b1031-sentinel.gba'))
        try:
            ready = driver.generate_translation_json(config)
            payload = json.loads(ready.read_text())
            assert {item['offset'] for item in payload['translations']} == translations.keys()
            rom = driver.build_rom(config, ready)
            result = rom.read_bytes()
            routes.verify(result, ready, translations)
            expected = bytearray(source)
            allowed = []
            relocated = 0
            for key, entry in routes.entries.items():
                raw = TextEncoder.encode_pokemon(translations[key], skip_aliases=SPANISH_GLYPH_CHARS)
                for ref in entry['pointer_offsets']:
                    expected[ref:ref+4] = result[ref:ref+4]
                    allowed.append((ref, ref+4))
                    target = int.from_bytes(result[ref:ref+4], 'little') - 0x08000000
                    if len(raw) > len(bytes.fromhex(entry['source_hex'])) and target == key:
                        raise ValueError('Sentinelle longue non relocalisée')
                    relocated += target != key
                    expected[target:target+len(raw)] = raw
                    allowed.append((target, target+len(raw)))
            if expected != result:
                raise ValueError('La ROM sentinelle modifie des octets hors des textes et pointeurs attendus')
            assert relocated > 0
            driver.apply_patches(replace(config, code='es-maint'), rom, ready, build_number=0)
            result = rom.read_bytes()
            routes.verify(result, ready, translations)
            if args.es004:
                # Le témoin subit exactement les mêmes patches, avec un combined
                # temporaire vide. La différence finale reste limitée aux routes.
                baseline = temporary / 'baseline.gba'
                baseline.write_bytes(source)
                empty_combined = temporary / 'empty.txt'
                empty_combined.write_text('')
                empty_json = temporary / 'empty.json'
                empty_json.write_text(json.dumps({'translations': [], 'total_translations': 0}))
                driver.apply_patches(replace(config, code='es-maint', combined=str(empty_combined)),
                                     baseline, empty_json, build_number=0)
                expected = bytearray(baseline.read_bytes())
                for start, end in allowed:
                    expected[start:end] = result[start:end]
                if expected != result:
                    first = next(i for i, (a, b) in enumerate(zip(expected, result)) if a != b)
                    raise ValueError(f'Patch hors plages autorisées de la sentinelle : 0x{first:X}')
            consumers = sum(len(entry['pointer_offsets']) for entry in routes.entries.values())
            print(f'{len(routes.entries)} descriptions et {consumers} consommateurs vérifiés '
                  f'après tous les patches es-maint ; {relocated} références relocalisées')
        finally:
            for suffix in ['translation_ready.json', 'trilingual_translation.csv', 'alias_base.csv']:
                (driver.TRANSLATION_DIR / f'es-maint-probe_{suffix}').unlink(missing_ok=True)


if __name__ == '__main__':
    main()
