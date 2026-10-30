"""PT-47 : périmètre, contrats binaires et règles de combat CFRU."""
import json
from collections import Counter
from pathlib import Path

import pytest

from scripts.apply_combined_fr import _load_combined
from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt47_audit.json').read_text())
ROWS = AUDIT['entries']


def test_manifest_controls_glossary_and_budgets():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    manifest = next(b['offsets'] for b in batches if b['id'] == 'PT-47')
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    en, _ = _load_combined(ROOT / 'languages/en/combined_en.txt')
    fr, _ = _load_combined(ROOT / 'languages/fr/combined_fr.txt')
    assert [r['offset'] for r in ROWS] == manifest
    assert len(manifest) == 283
    assert Counter(r['status'] for r in ROWS) == {'translated': 162, 'retained': 50, 'exception': 71}
    for row in ROWS:
        offset = int(row['offset'], 16)
        assert row['corpus_en'] == en[offset]
        assert row['comparison_fr'] == fr.get(offset)
        assert row['reason']
        if row['status'] == 'exception':
            assert not row['references']
            assert offset not in texts
            continue
        expected = row['expected'].replace(r'\n', '\n')
        encoded = TextEncoder.encode_pokemon(expected, strict=True)
        source = bytes.fromhex(row['source_hex'])
        controls = lambda raw: [c for c in _extract_control_sequences_from_raw(raw) if c[0] != 0xFE]
        assert controls(encoded) == controls(source)
        assert len(encoded) == row['pt_bytes']
        assert line_widths(expected) == row['pixels']
        assert max(row['pixels']) <= row['max_width']
        if 'cell_offset' in row:
            assert len(encoded) <= 7
            assert texts[offset] == expected
            continue
        assert row['references']
        if row['status'] == 'translated':
            assert texts[offset] == expected
        else:
            assert encoded == source
            assert texts.get(offset, expected) == expected

    # L'effet des baies conserve la distinction amitié/statistique de base.
    assert 'mais amigável' in texts[0xA4E240]
    assert 'Base de <0xFD><0x03>: mínima.' in texts[0xA4E299]
    assert 'Habilidade' in texts[0xA4E37C]
    assert texts[0xA4DDCA].count('<0xFB>') == 4
    assert texts[0xA4EB7C].count('<0xFB>') == 3
    assert texts[0xA4E474] == 'A batalha acaba se:\n4 Pokémon desmaiarem\n10 turnos passarem'
    assert 'Cube Corp.' in texts[0xA4DDCA]
    assert texts[0xA4EF14] == 'Black Hole Eclipse'
    # La tolérance D/O de Vision n'autorise aucune faute dans le texte livré.
    assert texts[0xA4DD24] == 'O ADM permitiu que você emergisse!'
    assert texts[0xA4E686] == (
        'Nem pensar<0xB0> NEM PENSAR!\nEnquanto eu for o chefão, não!<0xFB><0x00>'
    )


def fixture_source():
    """Extraits binaires réels de l'audit aux adresses originales."""
    source = bytearray(b'\xff' * 0x1000000)
    for row in ROWS:
        offset = int(row['live_offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        source[offset:offset + len(raw)] = raw
        if 'cell_hex' in row:
            source[offset:offset + 7] = bytes.fromhex(row['cell_hex'])
        for ref in row.get('table_references', []):
            source[ref:ref + 4] = (0x08A4EAD4).to_bytes(4, 'little')
        for ref in row['references']:
            source[ref:ref + 4] = (offset + 0x08000000).to_bytes(4, 'little')
    return source


def test_patch_is_atomic_bounded_idempotent():
    from languages.pt.patches.batch_47 import make_patch

    source = fixture_source()
    rom = bytearray(source)
    patch = make_patch(bytes(source))
    assert patch.apply(rom)['verified'] == 189
    patch.verify(rom)
    allowed = set()
    for row in ROWS:
        if row['status'] == 'exception':
            continue
        if 'cell_offset' in row:
            cell = int(row['cell_offset'], 16)
            allowed.update(range(cell, cell + 7))
        for ref in ([] if 'cell_offset' in row else row['references']):
            allowed.update(range(ref, ref + 4))
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(target, target + row['pt_bytes']))
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(source, rom)))
    assert patch.apply(rom)['relocated'] == 0
    before = bytes(rom)
    damaged = bytearray(source)
    damaged[0xA4D80A] ^= 1
    patch.source = bytes(damaged)
    with pytest.raises(ValueError, match='préimage'):
        patch.apply(rom)
    assert bytes(rom) == before
