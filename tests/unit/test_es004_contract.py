"""Recette du lot ES-004 : sélection fermée, sens et fenêtres sans fallback."""
import importlib
import json
from collections import Counter
from pathlib import Path

from scripts.audit_translation_coverage import parse_combined
from src.core.item_description_routes import ItemDescriptionRoutes, SystemTextRoutes
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder

ROOT = Path(__file__).resolve().parents[2]


def test_exact_contract_values_exclusions_and_encoded_budgets():
    report = json.loads((ROOT / 'docs/analysis/es/004_TRAITEMENT.json').read_text())
    lots = json.loads((ROOT / 'docs/analysis/es/lots.json').read_text())
    expected = next(lot['offsets'] for lot in lots if lot['id'] == 'ES-004')
    rows = report['entries']
    assert [row['offset'] for row in rows] == expected
    assert len({row['offset'] for row in rows}) == 374
    combined = parse_combined(ROOT / 'languages/es-maint/combined_es-maint.txt')
    normalizer = importlib.import_module('src.translators.19_build_translated_rom_generic').TranslatedROMBuilder
    counts = Counter()
    for row in rows:
        offset = int(row['offset'], 16)
        assert row['surface'] and row['justification_finale']
        if row['value'] is None:
            assert row['decision'] == 'exclu sans injection'
            assert not combined.get(offset)
            counts['excluded'] += 1
            continue
        assert combined[offset].replace('\\n', '\n') == row['value']
        raw = TextEncoder.encode_pokemon(row['value'], skip_aliases=SPANISH_GLYPH_CHARS, strict=True)
        assert raw.hex() == row['encoded_hex']
        assert raw.count(0xFF) == 1 and raw[-1] == 0xFF
        assert not {0xFA, 0xFB} & set(raw)
        assert row['control_signature'] == row['source_control_signature'] == []
        assert normalizer._encoded_layout_widths(raw) == row['widths']
        assert len(row['widths']) <= row['layout']['max_lines']
        assert max(row['widths']) <= row['layout']['max_width']
        assert len(raw) <= row['layout'].get('max_bytes', 512)
        counts['active'] += 1
    assert counts == {'active': 256, 'excluded': 118}


def test_current_manifests_cover_all_active_values_and_block_every_exclusion():
    rows = json.loads((ROOT / 'docs/analysis/es/004_TRAITEMENT.json').read_text())['entries']
    manifests = {}
    excluded = set()
    for filename, cls in [('item_descriptions', ItemDescriptionRoutes), ('system_texts', SystemTextRoutes)]:
        manifest = json.loads((ROOT / f'languages/es-maint/{filename}.json').read_text())
        excluded.update(int(row['offset'], 16) for row in manifest.get('excluded', []))
        for entry in manifest['entries']:
            manifests[int(entry['offset'], 16)] = (cls, entry)
    for row in rows:
        offset = int(row['offset'], 16)
        if row['value'] is None:
            assert offset in excluded
            continue
        cls, entry = manifests[offset]
        assert entry['pointer_offsets'] == row['pointer_offsets']
        cls.normalize({'offset': offset, 'translation': row['value'],
                       'english_raw_bytes': entry['source_hex'],
                       'max_length': entry.get('fixed_capacity', 512),
                       **cls.layout_metadata(entry)})


def test_numeric_effects_factions_and_names_do_not_regress():
    actual = parse_combined(ROOT / 'languages/es-maint/combined_es-maint.txt')
    flat = {key: value.replace('\\n', ' ') for key, value in actual.items()}
    assert 'Restaura 10 PP' in flat[0x3D5883]
    assert 'todos los PP' in flat[0x3D5934]
    assert 'todos los Pokémon debilitados' in flat[0x3D5B49]
    assert 'aumenta el nivel' in flat[0x3D5A6A]
    assert 'reduce el nivel' in flat[0x3D5AB8]
    assert 'alto precio' in flat[0x3D6778]
    assert 'rojizo' in flat[0x3DA95A]
    assert 'Shadows' in flat[0x3D90D7] and 'Thundercap' in flat[0x3D90D7]
    assert 'Profesor Log' in flat[0x3DA7D1] and 'Pueblo Bellin' in flat[0x3DA7D1]
    assert actual[0x3DF7E8] == 'ZREZA'
    assert actual[0x3E81AE] == 'SOMBRATRAMPA'
    for key, value in {0x3E7F9A: 'Pokémon', 0x3E7FA6: 'Pokédex',
                       0x3E7F92: 'POKéNAV', 0x3E8160: 'COLOR'}.items():
        assert actual[key] == value


def test_es004_and_es005_share_a_group_without_sharing_any_word_cell():
    """Un groupe traduit par deux lots ne peut être gelé au périmètre d'un seul."""
    es004 = json.loads((ROOT / 'docs/analysis/es/004_TRAITEMENT.json').read_text())
    es005 = json.loads((ROOT / 'docs/analysis/es/005_TRAITEMENT.json').read_text())
    manifest = json.loads((ROOT / 'languages/es-maint/system_texts.json').read_text())
    descriptor = next(guard for guard in manifest['guards']
                      if int(guard['offset'], 16) <= 0x3ECEE4
                      and int(guard['offset'], 16) + len(bytes.fromhex(guard['hex'])) >= 0x3ECEEC)
    within_guard = 0x3ECEE4 - int(descriptor['offset'], 16)
    raw = bytes.fromhex(descriptor['hex'])[within_guard:within_guard + 8]
    base = int.from_bytes(raw[:4], 'little') - 0x08000000
    count = int.from_bytes(raw[4:6], 'little')
    assert base == 0x3E8504 and count == 109
    earlier = [row for row in es004['entries'] if row.get('group') == 2]
    later = [row for row in es005['entries'] if row['group'] == 2]
    assert earlier and later
    cells = {}
    for rows, field in ((earlier, 'pointer_offsets'), (later, 'pointer_site')):
        for row in rows:
            site = row[field][0] if field == 'pointer_offsets' else int(row[field], 16)
            assert site == base + row['word_index'] * 12
            assert 0 <= row['word_index'] < count
            assert site not in cells, (row['offset'], hex(site))
            cells[site] = row['value']
    assert 'HEDOR' in cells.values() and 'ACLIMATACIÓN' in cells.values()
