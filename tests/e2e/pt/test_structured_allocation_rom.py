"""B-1034 : propriété des lecteurs et pression réelle sur l'espace autorisé."""
import copy
import importlib
from pathlib import Path

import pytest

from languages.pt.patches.batch_86 import make_patch
from src.core.structured_text import StructuredTextRoutes
from src.core.text_reinserter import FreeSpaceAllocator, SmartReinserter

ROOT = Path(__file__).resolve().parents[3]
pytestmark = pytest.mark.rom
OFFSET = 0x1F9B330


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


def single_patch(source):
    patch = make_patch(source)
    patch.definitions = [d for d in patch.definitions if int(d['offset'], 16) == OFFSET]
    # Le test isole la primitive texte, sans les préparateurs de PT-86.
    from languages.pt.patches.batch_20 import BorriusTextPatch
    return BorriusTextPatch(source, patch.definitions, ROOT / 'languages/pt/combined_pt.txt')


def payload(patch):
    return {'translations': [{'offset': OFFSET, 'translation': patch.texts[OFFSET].replace(r'\n', '\n'),
                              'category': 'dialogue', 'encoding': 'pokemon'}]}


def test_canonical_text_fits_under_real_rom_pressure_without_second_copy(source, tmp_path):
    patch = single_patch(source)
    routes = StructuredTextRoutes([patch])
    rom = bytearray(source)
    for start, size in FreeSpaceAllocator(rom).blocks:
        rom[start:start + size] = b'\xaa' * size
    assert not FreeSpaceAllocator(rom).blocks
    before = bytes(rom)
    builder_type = importlib.import_module('src.translators.19_build_translated_rom_generic').TranslatedROMBuilder
    builder = builder_type.__new__(builder_type)
    builder.english_texts = None
    data = routes.enrich(payload(patch))
    normalized = builder._normalize_translation_item(OFFSET, data['translations'][0])
    writer = SmartReinserter(rom, allow_relocate=True, allow_fallback=True)

    assert writer.reinsert_text(normalized)
    writer.flush_relocations()
    # La passe inline partage le même contrat et ne doit pas renormaliser la cellule.
    import json
    import subprocess
    import sys

    built = tmp_path / 'pressure.gba'
    built.write_bytes(rom)
    protected = tmp_path / 'canonical.json'
    protected.write_text(json.dumps(data))
    extraction = tmp_path / 'extracted.json'
    extraction.write_text(json.dumps({'texts': [{'offset': OFFSET,
        'encoding': 'pokemon', 'byte_length': 210,
        'raw_bytes': patch.definitions[0]['source_hex']}]}))
    subprocess.run([sys.executable, str(ROOT / 'scripts/apply_inline_overrides_fr.py'),
                    '--rom', str(built), '--source', str(ROOT / 'input/roms/englishrom.gba'),
                    '--combined', str(ROOT / 'languages/pt/combined_pt.txt'),
                    '--translations', str(protected), '--reference-texts', str(extraction),
                    '--english-texts', str(extraction), '--no-template-fallback'],
                   check=True, capture_output=True)
    rom = bytearray(built.read_bytes())
    assert patch.apply(rom)['relocated'] == 0
    routes.verify(rom)

    expected = patch.entries()[0][2]
    assert rom[OFFSET:OFFSET + len(expected)] == expected
    assert rom[:OFFSET] == before[:OFFSET]
    assert rom[OFFSET + 210:] == before[OFFSET + 210:]
    assert writer.get_report()['statistics']['fallback_used'] == 0
    assert writer.get_report()['statistics']['relocated'] == 0
    assert routes.enrich(data) == data
    snapshot = bytes(rom)
    assert patch.apply(rom)['relocated'] == 0
    assert bytes(rom) == snapshot


def test_unclassified_reader_is_rejected_before_json_mutation(source):
    patch = single_patch(source)
    changed = bytearray(source)
    changed[0x100:0x104] = (OFFSET + 0x08000000).to_bytes(4, 'little')
    patch.source = bytes(changed)
    data = payload(patch)
    before = copy.deepcopy(data)

    with pytest.raises(ValueError, match='lecteurs'):
        StructuredTextRoutes([patch]).enrich(data)

    assert data == before


def test_final_verifier_rejects_missing_delivery_and_out_of_bounds(source):
    patch = single_patch(source)
    routes = StructuredTextRoutes([patch])
    rom = bytearray(source)
    ref = patch.entries()[0][1][0]
    for target in (OFFSET, len(source) + 1):
        rom[ref:ref + 4] = (target + 0x08000000).to_bytes(4, 'little')
        with pytest.raises(ValueError):
            routes.verify(rom)


def test_rejected_preimage_leaves_payload_unchanged(source):
    patch = single_patch(source)
    rom = bytearray(source)
    rom[OFFSET] ^= 1
    patch.source = bytes(rom)
    data = payload(patch)
    before = copy.deepcopy(data)
    with pytest.raises(ValueError, match='préimage'):
        StructuredTextRoutes([patch]).enrich(data)
    assert data == before


def test_saturated_finalizer_rolls_back_without_claiming_engine_bytes(source):
    patch = single_patch(source)
    rom = bytearray(source)
    for start, size in FreeSpaceAllocator(rom).blocks:
        rom[start:start + size] = b'\xaa' * size
    before = bytes(rom)

    with pytest.raises(ValueError, match='espace libre insuffisant'):
        patch.apply(rom)

    assert bytes(rom) == before
    assert not FreeSpaceAllocator(rom).blocks
