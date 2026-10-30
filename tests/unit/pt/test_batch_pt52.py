"""PT-52 : couverture exacte, sémantique Pokédex et injection atomique bornée."""
import json
from collections import Counter
from pathlib import Path

import pytest

from scripts.apply_combined_fr import _load_combined
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt52_audit.json').read_text())
ROWS = AUDIT['entries']


def test_manifest_sources_controls_and_budgets():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    manifest = next(b['offsets'] for b in batches if b['id'] == 'PT-52')
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    en, _ = _load_combined(ROOT / 'languages/en/combined_en.txt')
    fr, _ = _load_combined(ROOT / 'languages/fr/combined_fr.txt')
    assert [r['offset'] for r in ROWS] == manifest
    assert len(manifest) == len(set(manifest)) == 299
    assert Counter(r['kind'] for r in ROWS) == {'description': 125, 'category': 19, 'species': 155}
    assert Counter(r['status'] for r in ROWS) == {'translated': 143, 'retained': 156}
    for row in ROWS:
        offset = int(row['offset'], 16)
        text = row['expected'].replace(r'\n', '\n')
        raw = TextEncoder.encode_pokemon(text, strict=True)
        source = bytes.fromhex(row['source_hex'])
        assert texts[offset] == text
        assert row['corpus_en'] == en.get(offset)
        assert row['comparison_fr'] == fr.get(offset)
        assert row['reason']
        assert len(raw) == row['pt_bytes']
        assert line_widths(text) == row['pixels']
        assert max(row['pixels']) <= row['max_width']
        # Prose simple, deux retours et aucun contrôle/tampon perdu ou ajouté.
        assert not set(raw[:-1]) & set(range(0xF7, 0xFE))
        if row['kind'] == 'description':
            assert raw.count(b'\xfe') == source.count(b'\xfe') == 2
        elif row['kind'] == 'species':
            assert raw == source
            assert len(raw) <= 11
        else:
            assert row['references']


def test_pokedex_meaning_uses_actual_english_not_contaminated_corpus():
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    flat = lambda off: texts[off].replace('\n', ' ')
    # Le corpus EN de Zacian parle d'absorption du métal ; la ROM parle de sa sœur.
    assert 'irmã mais velha de Zamazenta' in flat(0x1667C5F)
    assert '20 mil anos' in flat(0x1667D39)
    assert 'cipós' in flat(0x1667E8F)
    assert 'energia de dragão cristalizada' in flat(0x1667F7E)
    assert 'fantasma' in flat(0x1667B19)
    assert 'Strawberry Sweet' in flat(0x1667474)
    assert 'Water Gun' in flat(0x166970A) and 'Hydro Pump' in flat(0x166970A)
    assert texts[0x166A997] == 'Bulbasaur'
    assert texts[0x166AED5] == 'Scyther'
    assert texts[0x166B035] == 'Cyndaquil'
    assert texts[0x166AAD6] == 'Nidorina'


def fixture_source():
    """Reconstruit les vrais extraits binaires versionnés, sans ROMReader simulé."""
    source = bytearray(b'\xff' * 0x2000000)
    for row in ROWS:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row.get('cell_hex', row['source_hex']))
        source[offset:offset + len(raw)] = raw
        for ref in row['references']:
            source[ref:ref + 4] = (offset + 0x08000000).to_bytes(4, 'little')
    for table in AUDIT['indirect_tables']:
        start = int(table['code_offset'], 16)
        raw = bytes.fromhex(table['code_hex'])
        source[start:start + len(raw)] = raw
        ref = int(table['reader'], 16)
        source[ref:ref + 4] = (int(table['base'], 16) + 0x08000000).to_bytes(4, 'little')
    for row in ROWS:
        for consumer in row.get('indirect_consumers', []):
            ref = int(consumer['site'], 16)
            source[ref - 4:ref - 2] = consumer['species_id'].to_bytes(2, 'little')
    for ref in AUDIT['species_table_references']:
        source[ref:ref + 4] = (0x0966A98C).to_bytes(4, 'little')
    return source


def test_atomic_bounded_idempotent_patch_and_rejection():
    from languages.pt.patches.batch_52 import make_patch

    source = fixture_source()
    rom = bytearray(source)
    patch = make_patch(bytes(source))
    stats = patch.apply(rom)
    assert stats['verified'] == 144 and stats['fixed_cells'] == 155
    patch.verify(rom)
    first = bytes(rom)
    assert patch.apply(rom)['relocated'] == 0
    assert bytes(rom) == first
    allowed = set()
    for row in ROWS:
        offset = int(row['offset'], 16)
        if row['kind'] == 'species':
            allowed.update(range(offset, offset + 11))
        for ref in row['references']:
            allowed.update(range(ref, ref + 4))
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(target, target + row['pt_bytes']))
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(source, rom)))
    # Une préimage ou un lecteur altéré doit tout refuser, sans mutation partielle.
    broken = bytearray(source)
    broken[0x166A997] ^= 1
    with pytest.raises(ValueError, match='cellule canonique'):
        make_patch(bytes(broken)).apply(rom)
    assert bytes(rom) == first
    damaged = bytearray(rom)
    damaged[AUDIT['species_table_references'][0]] ^= 1
    before = bytes(damaged)
    with pytest.raises(ValueError, match='lecteur'):
        patch.apply(damaged)
    assert bytes(damaged) == before


def test_changed_regional_reader_is_rejected_atomically():
    from languages.pt.patches.batch_52 import make_patch

    source = fixture_source()
    rom = bytearray(source)
    rom[0x165BBEC] ^= 1
    before = bytes(rom)
    with pytest.raises(ValueError, match='lecteur Pokédex'):
        make_patch(bytes(source)).apply(rom)
    assert bytes(rom) == before
