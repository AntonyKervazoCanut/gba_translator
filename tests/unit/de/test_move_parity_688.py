"""Garde des clés FR de référence et des descriptions DE rédigées par B-688."""
import json
from pathlib import Path

from languages.fr.patches.tm_item_descriptions import load_combined
from src.core import moves
from src.core.pokedex import line_width
from src.core.text_codec import GERMAN_UMLAUT_CHARS, TextEncoder

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / 'tests/unit/fixtures/de_move_parity_688.json'


def test_reference_inventory_excludes_only_the_metadata_key():
    evidence = json.loads(FIXTURE.read_text())
    rows = evidence['references']
    move_keys = json.loads((ROOT / 'languages/fr/data/move_descriptions_fr_overrides.json').read_text())
    tm_keys = json.loads((ROOT / 'languages/fr/data/tm_item_descriptions_fr.json').read_text())

    assert set(move_keys) - {str(row['index']) for row in rows if row['kind'] == 'move'} == {'_comment'}
    assert {str(row['index']) for row in rows if row['kind'] == 'tm'} == set(tm_keys)
    assert len(rows) == 228
    assert len({(row['kind'], row['index']) for row in rows}) == 228
    assert evidence['metadata_reference']['key'] == '_comment'


def test_authored_descriptions_fit_both_consumers_and_preserve_plain_text():
    rows = json.loads(FIXTURE.read_text())['references']
    combined = load_combined(ROOT / 'languages/de/combined_de.txt')
    authored = [row for row in rows if row['owner'] == 'B-688']

    assert len(authored) == 72
    assert len({row['offset'] for row in authored}) == 71
    for row in authored:
        text = combined[int(row['offset'], 16)]
        assert text == row['authored'], row['offset']
        text = text.replace('\\n', '\n')
        assert len(text.splitlines()) <= (5 if row['kind'] == 'move' else 4), row['offset']
        assert max(map(line_width, text.splitlines())) <= 122, row['offset']
        assert 'Spezial-Verteidigung' not in text
        assert 'Spezial-Angriff' not in text
        raw = TextEncoder.encode_pokemon(text, skip_aliases=GERMAN_UMLAUT_CHARS)
        assert raw[-1] == 0xFF
        assert not any(code in raw[:-1] for code in range(0xF7, 0xFE)), row['offset']
        assert not any(token in text for token in ('{', '}', '<0x', '\\l', '\\p'))


def test_tm_references_use_item_indices_and_keep_the_move_association():
    rows = json.loads(FIXTURE.read_text())['references']
    machines = {row['index']: row for row in rows if row['kind'] == 'tm'}
    expected = {323: 89, 326: 94, 399: 510, 401: 468, 409: 424, 429: 502, 452: 127, 432: 440}

    for item, move in expected.items():
        row = machines[item]
        assert int(row['pointer'], 16) == 0x876074 + item * 44 + 0x14
        assert row['move_indices'] == [move]
    for row in rows:
        if row['kind'] == 'move':
            assert int(row['pointer'], 16) == moves.struct_offset(row['index'])
    assert machines[409]['owner'] == 'B-669'
    assert machines[452]['offset'] == next(row['offset'] for row in rows if row['kind'] == 'move' and row['index'] == 127)


def test_schnueffler_has_ghost_identification_not_miracle_eye_effect():
    combined = load_combined(ROOT / 'languages/de/combined_de.txt')
    text = combined[0x487C8B].replace('\\n', ' ')

    assert 'Geist mit Normal und Kampf' in text
    assert 'Psycho' not in text
    assert 'Unlicht' not in text


def test_live_audit_reads_the_relocated_target_instead_of_the_old_cell():
    import importlib.util
    import struct

    spec = importlib.util.spec_from_file_location('audit_de_move_parity', ROOT / 'scripts/audit_de_move_parity.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    row = next(row for row in json.loads(FIXTURE.read_text())['references'] if row['kind'] == 'move' and row['index'] == 23)
    source = bytearray(0x1000000)
    rom = bytearray(source)
    original, target, pointer = int(row['offset'], 16), int(row['after']['target'], 16), int(row['pointer'], 16)
    raw = bytes.fromhex(row['after']['hex'])
    source_text = TextEncoder.encode_pokemon(row['source'])
    source[original:original + len(source_text)] = source_text
    source[pointer:pointer + 4] = struct.pack('<I', original + 0x08000000)
    rom[original:original + len(source_text)] = source_text
    rom[target:target + len(raw)] = raw
    rom[pointer:pointer + 4] = struct.pack('<I', target + 0x08000000)

    result = module.inspect_reference(bytes(rom), bytes(source), row, {original: row['authored']})

    assert target != original
    assert result['exact']
    assert result['ok']
    assert not result['english']

    untranslated = module.inspect_reference(bytes(source), bytes(source), row, {original: row['source']})
    assert untranslated['english']
    assert untranslated['exact']
    assert not untranslated['ok']
