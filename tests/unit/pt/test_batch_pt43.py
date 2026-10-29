"""PT-43 : périmètre, contrats binaires et règles de combat CFRU."""
import json
from collections import Counter
from pathlib import Path

import pytest

from scripts.apply_combined_fr import _load_combined
from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt43_audit.json').read_text())
ROWS = AUDIT['entries']


def test_manifest_controls_glossary_and_budgets():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    manifest = next(b['offsets'] for b in batches if b['id'] == 'PT-43')
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    en, _ = _load_combined(ROOT / 'languages/en/combined_en.txt')
    fr, _ = _load_combined(ROOT / 'languages/fr/combined_fr.txt')
    assert [r['offset'] for r in ROWS] == manifest
    assert len(manifest) == 282
    assert Counter(r['status'] for r in ROWS) == {'translated': 77, 'retained': 203, 'exception': 2}
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
        assert max(row['pixels']) <= row['max_width'] == 204
        assert row['references']
        if row['status'] == 'translated':
            assert texts[offset] == expected
        else:
            assert encoded == source
            assert texts.get(offset, expected) == expected
    # Effets spécifiques CFRU : Misty Terrain renforce aussi le type Fada.
    assert 'Fada ganham força' in texts[0xA443EE]
    assert 'Psíquicos' in texts[0xA44464]
    assert 'Unaware, Oblivious ou Magic Guard' in texts[0xA44745]
    assert texts[0xA44835].count('<0xFB>') == 2
    assert 'Primal Reversion, Ultra Burst' in texts[0xA44835]


def fixture_source():
    """Extraits binaires réels de l'audit aux adresses originales."""
    source = bytearray(b'\xff' * 0x1000000)
    for row in ROWS:
        offset = int(row['live_offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        source[offset:offset + len(raw)] = raw
        for ref in row['references']:
            source[ref:ref + 4] = (offset + 0x08000000).to_bytes(4, 'little')
    return source


def test_patch_is_atomic_bounded_idempotent():
    from languages.pt.patches.batch_43 import make_patch

    source = fixture_source()
    rom = bytearray(source)
    patch = make_patch(bytes(source))
    assert patch.apply(rom)['verified'] == 77
    patch.verify(rom)
    allowed = set()
    for row in ROWS:
        if row['status'] != 'translated':
            continue
        for ref in row['references']:
            allowed.update(range(ref, ref + 4))
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(target, target + row['pt_bytes']))
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(source, rom)))
    assert patch.apply(rom)['relocated'] == 0
    before = bytes(rom)
    damaged = bytearray(source)
    damaged[0xA43D50] ^= 1
    patch.source = bytes(damaged)
    with pytest.raises(ValueError, match='préimage'):
        patch.apply(rom)
    assert bytes(rom) == before


def test_visual_probe_texts_keep_exact_spelling_despite_ocr_ambiguity():
    """La tolérance OCR a/o ne doit jamais autoriser une faute dans la source."""
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    assert texts[0xA43D50] == 'Ué? O DexNav detectou um\nPokémon incomum!'
    assert texts[0xA4432A] == (
        'com o campo eletrificado!<0xFB>No chão, Pokémon não adormecem\n'
        'e golpes Elétricos ganham força!'
    )
