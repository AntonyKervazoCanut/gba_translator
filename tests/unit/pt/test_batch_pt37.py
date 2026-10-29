"""PT-37 : glossaire, contrôles binaires, cellules et consommateurs exacts."""
import json
from collections import Counter
from pathlib import Path

import pytest

from scripts.apply_combined_fr import _load_combined
from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt37_audit.json').read_text())
ROWS = AUDIT['entries']


def test_exact_scope_glossary_and_binary_controls():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    manifest = next(b['offsets'] for b in batches if b['id'] == 'PT-37')
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    assert [r['offset'] for r in ROWS] == manifest
    assert Counter(r['kind'] for r in ROWS) == {
        'ability_name': 198, 'battle': 42, 'move_description': 42,
    }
    assert Counter(r['status'] for r in ROWS) == {'retained': 199, 'translated': 83}
    for row in ROWS:
        text = texts[int(row['offset'], 16)]
        assert text == row['expected'].replace(r'\n', '\n')
        encoded = TextEncoder.encode_pokemon(text.replace(r'\n', '\n'), strict=True)
        source = bytes.fromhex(row['source_hex'])
        controls = lambda raw: [c for c in _extract_control_sequences_from_raw(raw) if c[0] != 0xFE]
        assert controls(encoded) == controls(source)
        assert len(encoded) == row['pt_bytes']
        assert line_widths(text.replace(r'\n', '\n')) == row['pixels']
        if row['kind'] == 'ability_name':
            assert encoded == source
            assert len(encoded) <= row['cell_bytes'] == 17
            assert int(row['offset'], 16) == 0xA36398 + 17 * row['ability_id']
        else:
            assert row['references']
            assert max(row['pixels']) <= row['max_width']
            if row['kind'] == 'move_description':
                assert len(row['pixels']) <= 4
    assert 'congeladura' in texts[0xA37C6F]
    assert 'congelar' not in texts[0xA37C6F]  # Frostbite CFRU, pas le gel classique.
    assert 'PS' in texts[0xA37EC4]
    assert 'equipe' in texts[0xA37E7C]  # Howl augmente l’équipe dans cette révision.


def fixture_source():
    """Reconstruit uniquement les extraits binaires réels figés dans l'audit."""
    rom = bytearray(b'\xff' * 0x1000000)
    for row in ROWS:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        rom[offset:offset + len(raw)] = raw
        for ref in row['references']:
            rom[ref:ref + 4] = (offset + 0x08000000).to_bytes(4, 'little')
    return rom


def test_patch_is_atomic_bounded_and_idempotent():
    from languages.pt.patches.batch_37 import make_patch

    source = fixture_source()
    rom = bytearray(source)
    patch = make_patch(bytes(source))
    stats = patch.apply(rom)
    assert stats['verified'] == 84
    patch.verify(rom)
    allowed = set()
    for row in ROWS:
        if row['kind'] == 'ability_name':
            offset = int(row['offset'], 16)
            assert rom[offset:offset + 17] == source[offset:offset + 17]
        else:
            for ref in row['references']:
                allowed.update(range(ref, ref + 4))
                target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
                allowed.update(range(target, target + row['pt_bytes']))
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(source, rom)))
    assert patch.apply(rom)['relocated'] == 0
    before = bytes(rom)
    patch.source = bytes(source[:0xA37734]) + b'\x00' + bytes(source[0xA37735:])
    with pytest.raises(ValueError, match='préimage'):
        patch.apply(rom)
    assert rom == before
