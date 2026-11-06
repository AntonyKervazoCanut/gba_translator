"""F-864 : couverture exacte, texte livré et consommateurs de chaque traduction."""
import json
from pathlib import Path

from scripts.apply_combined_fr import _load_combined
from src.core.item_description_routes import SystemTextRoutes
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder
from src.core.text_reinserter import SmartReinserter

ROOT = Path(__file__).resolve().parents[2]


def test_es014_complete_selection_and_real_consumer_roundtrip(tmp_path: Path) -> None:
    """Réinsère les textes finaux sur les vraies tranches moteur et contrôle tout le binaire."""
    report = json.loads((ROOT / 'docs/analysis/es/014_TRAITEMENT.json').read_text())
    technical = json.loads((ROOT / 'docs/analysis/es/014_ROUTES.json').read_text())
    fixture = json.loads((ROOT / 'tests/unit/fixtures/es014_rom.json').read_text())
    source = bytearray(fixture['rom_size'])
    for part in fixture['slices']:
        raw = bytes.fromhex(part['hex'])
        source[part['offset']:part['offset'] + len(raw)] = raw
    source[-65536:] = b'\xff' * 65536
    combined, _ = _load_combined(ROOT / 'languages/es-maint/combined_es-maint.txt')
    entries = {int(e['offset'], 16): e for e in report['entries']}
    translations = {key: e['translation'] for key, e in entries.items() if 'translation' in e}
    routes = SystemTextRoutes.load(ROOT / 'tests/unit/fixtures/es014_contract.json', source)
    ready = tmp_path / 'ready.json'
    ready.write_text('{"translations": []}')
    rom = bytearray(source)
    inserter = SmartReinserter(rom, allow_relocate=True, skip_encode_aliases=SPANISH_GLYPH_CHARS)

    routes.enrich_json(ready, translations)
    for item in json.loads(ready.read_text())['translations']:
        assert inserter.reinsert_text(routes.normalize(item)), inserter.stats
    inserter.flush_relocations()
    routes.verify(rom, ready, translations)

    assert len(entries) == 374
    assert set(entries) == {int(e['offset'], 16) for e in technical['entries']}
    assert len(translations) == 357
    assert set(translations) == set(routes.entries)
    assert all(combined[key] == value for key, value in translations.items())
    assert not (routes.excluded & set(combined))
    expected = bytearray(source)
    for key, entry in routes.entries.items():
        raw = TextEncoder.encode_pokemon(translations[key], strict=True, skip_aliases=SPANISH_GLYPH_CHARS)
        assert entries[key]['encoded_bytes_including_ff'] == len(raw)
        for ref in entry['pointer_offsets']:
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            assert rom[target:target + len(raw)] == raw
            expected[ref:ref + 4] = rom[ref:ref + 4]
            expected[target:target + len(raw)] = raw
    assert rom == expected
