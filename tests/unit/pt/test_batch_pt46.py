"""PT-46 : périmètre exact, contrôles CFRU et assemblages de combat."""
import json
from collections import Counter
from pathlib import Path

import pytest
import yaml

from scripts.apply_combined_fr import _load_combined
from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt46_audit.json').read_text())
ROWS = AUDIT['entries']


def commands(raw):
    return [s for s in _extract_control_sequences_from_raw(raw) if s[0] != 0xFE]


def test_closed_manifest_controls_and_exact_protections():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-46')
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    guards = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protected = {int(e['offset'], 16): e['expected'] for e in guards['entries']}
    assert [r['offset'] for r in ROWS] == manifest
    assert len(ROWS) == 282
    assert Counter(r['status'] == 'exception' for r in ROWS) == {False: 263, True: 19}
    for row in ROWS:
        offset = int(row['offset'], 16)
        if row['status'] == 'exception':
            assert not row['references'] and row['reason']
            assert offset not in texts
            continue
        expected = row['expected']
        assert texts[offset] == expected.replace(r'\n', '\n')
        assert protected[offset] == expected
        encoded = TextEncoder.encode_pokemon(texts[offset], strict=True)
        assert commands(encoded) == commands(bytes.fromhex(row['source_hex']))
        assert len(encoded) == row['pt_bytes']
        assert line_widths(texts[offset]) == row['pixels']
        assert max(row['pixels']) <= row['max_width'] == 214
        assert row['references']


def test_battle_buffers_spacing_glossary_and_complete_warnings():
    rows = {int(r['offset'], 16): r for r in ROWS}
    text = lambda o: rows[o]['expected']
    # Les buffers restent dans l'ordre EN, même pour les stats et équipes.
    assert text(0xA4C200) == '<0xFD><0x13>: <0xFD><0x00>\\n<0xFD><0x01>'
    assert 'não diminuiu' in text(0xA4B2F9)
    for offset in (0xA4C603, 0xA4C610, 0xA4C61A, 0xA4C628, 0xA4C636, 0xA4C640):
        assert text(offset).endswith('<0x00>')
    assert text(0xA4C915) == 'congeladura'
    assert 'PS' in text(0xA4B51F)
    assert text(0xA4C5DD) == 'Disable'
    assert text(0xA4C5FD) == 'Taunt'
    assert text(0xA4CB06) == 'Prec:<0x00>'  # vrai Acc: EN, pas None du corpus périmé
    assert 'Contato' == text(0xA4CB14)  # pas la catégorie Physique du FR
    assert 'PSN, PAR ou DRM' in text(0xA4CC1E)
    assert text(0xA4CDC8).endswith('use outro emulador.')
    assert 'GBA4iOS' in text(0xA4D138)
    for offset in (0xA4CDC8, 0xA4D138):
        assert len(bytes.fromhex(rows[offset]['source_hex'])) > 700
    # Les menus gardent les tabulations FC13 38 et les couleurs/fontes.
    for offset in (0xA4C7B7, 0xA4C7DA, 0xA4C807, 0xA4C82B):
        assert text(offset).count('<0xFC><0x13><0x38>') == 2
        assert max(line_widths('Lutar'), line_widths('Voltar'))[0] <= 56
    # Assemblages Z/Max : les espaces sont intentionnels.
    for offset in (0xA4CBBA, 0xA4CBD5, 0xA4CBEB):
        suffix = 0xA4CBA8 if offset == 0xA4CBBA else 0xA4CBB1
        assert max(line_widths(text(0xA4CBA3) + text(offset) + text(suffix))) <= 214


def fixture_source():
    """Extraits binaires EN réels, plus les références auditées."""
    source = bytearray(b'\xff' * 0x1000000)
    for row in ROWS:
        off = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        source[off:off + len(raw)] = raw
        for ref in row['references']:
            source[ref:ref + 4] = (off + 0x08000000).to_bytes(4, 'little')
    return source


def test_patch_atomic_bounded_and_idempotent():
    from languages.pt.patches.batch_46 import make_patch

    source = fixture_source()
    rom = bytearray(source)
    patch = make_patch(bytes(source))
    assert patch.apply(rom)['verified'] == 263
    patch.verify(rom)
    allowed = set()
    for row in ROWS:
        for ref in row['references']:
            allowed.update(range(ref, ref + 4))
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(target, target + row['pt_bytes']))
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(source, rom)))
    before = bytes(rom)
    assert patch.apply(rom)['relocated'] == 0
    assert rom == before
    patch.source = bytes(source[:0xA4AE61]) + b'\x00' + bytes(source[0xA4AE62:])
    with pytest.raises(ValueError, match='préimage'):
        patch.apply(rom)
    assert rom == before
