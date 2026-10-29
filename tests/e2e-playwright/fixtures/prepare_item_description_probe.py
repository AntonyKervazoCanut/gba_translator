"""Construit une ROM sentinelle via le vrai pipeline, sans modifier les sources."""
import sys
import tempfile
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts import build_language as driver
from src.core.item_description_routes import ItemDescriptionRoutes
from src.core.text_codec import TextEncoder


def sentinel(index: int) -> str:
    """Force la relocalisation réelle, sauf la description affichée dans le Cube."""
    lines = [f'TEST ITEM {index:02d}', 'SECOND LINE', 'THIRD LINE']
    return '\n'.join(lines if index == 15 else [line.ljust(32, 'i') for line in lines])


def main() -> None:
    """Prépare les dix-sept descriptions puis vérifie leurs 34 consommateurs."""
    routes = ItemDescriptionRoutes.load(
        ROOT / 'languages/es-maint/item_descriptions.json', driver.ENGLISH_ROM.read_bytes()
    )
    with tempfile.TemporaryDirectory(prefix='b1031-sentinel-') as directory:
        combined = Path(directory) / 'combined.txt'
        combined.write_text(''.join(
            f'0x{key:08X}: ' + sentinel(n).replace('\n', r'\n') + '\n'
            for n, key in enumerate(routes.entries)
        ))
        config = replace(driver.load_registry().get('es-maint'), code='es-maint-probe',
                         combined=str(combined), output_rom='GenedRom-b1031-sentinel.gba')
        try:
            ready = driver.generate_translation_json(config)
            rom = driver.build_rom(config, ready)
            result = rom.read_bytes()
            routes.verify(result, ready)
            expected = bytearray(driver.ENGLISH_ROM.read_bytes())
            for n, entry in enumerate(routes.entries.values()):
                raw = TextEncoder.encode_pokemon(sentinel(n))
                for ref in entry['pointer_offsets']:
                    expected[ref:ref+4] = result[ref:ref+4]
                    target = int.from_bytes(result[ref:ref+4], 'little') - 0x08000000
                    if n != 15 and target == int(entry['offset'], 16):
                        raise ValueError('Sentinelle longue non relocalisée')
                    expected[target:target+len(raw)] = raw
            if expected != result:
                raise ValueError('La ROM sentinelle modifie des octets hors des textes et pointeurs attendus')
            driver.apply_patches(replace(config, code='es-maint'), rom, ready, build_number=0)
            routes.verify(rom.read_bytes(), ready)
            print('17 descriptions et 34 consommateurs vérifiés après tous les patches es-maint')
        finally:
            for suffix in ['translation_ready.json', 'trilingual_translation.csv', 'alias_base.csv']:
                (driver.TRANSLATION_DIR / f'es-maint-probe_{suffix}').unlink(missing_ok=True)


if __name__ == '__main__':
    main()
