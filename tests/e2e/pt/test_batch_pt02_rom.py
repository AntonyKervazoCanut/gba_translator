"""F-761 : preuve binaire du lot PT-02 sur ROM reconstruite localement."""
import json
import re
import struct
from pathlib import Path

import pytest

from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.dialogue_linewrap import line_width
from src.core.fixed_tables import FIXED_TABLE_RANGES
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
pytestmark = pytest.mark.rom


def control_signature(raw):
    """Variables, couleur, police et pages ; les retours doux peuvent être repliés."""
    return [seq for seq in _extract_control_sequences_from_raw(raw)
            if seq[0] not in (0xFA, 0xFE)]


def words(raw):
    return raw.replace(b'\xfe', b'\x00').replace(b'\xfa', b'\x00').split(b'\x00')


@pytest.fixture(scope='module')
def audit():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    offsets = {int(x, 16) for b in batches if b['id'] == 'PT-02' for x in b['offsets']}
    actual = {}
    for line in (ROOT / 'languages/pt/combined_pt.txt').read_text().splitlines():
        match = re.match(r'0x([0-9a-f]+): (.*)', line)
        if match and int(match[1], 16) in offsets:
            actual[int(match[1], 16)] = match[2]
    return source, built, actual


def test_every_translation_is_injected_and_reachable(audit):
    source, built, actual = audit
    failures = []
    for offset, text in actual.items():
        normalized = text.replace(r'\n', '\n').replace(r'\p', '<0xFB>').replace(r'\l', '<0xFA>')
        expected = TextEncoder.encode_pokemon(normalized)[:-1]
        original = source[offset:source.index(b'\xff', offset)]
        assert control_signature(expected) == control_signature(original), hex(offset)
        sites = []
        needle = struct.pack('<I', offset + 0x08000000)
        site = source.find(needle)
        while site >= 0:
            sites.append(site)
            site = source.find(needle, site + 1)
        # Sans pointeur, l'entrée doit tenir exactement dans la cellule EN.
        if not sites:
            assert len(expected) <= len(original), hex(offset)
        targets = [struct.unpack_from('<I', built, site)[0] - 0x08000000 for site in sites] or [offset]
        for target in targets:
            assert 0 <= target < len(built), (hex(offset), target)
            raw = built[target:built.index(b'\xff', target)]
            if words(raw) != words(expected) or control_signature(raw) != control_signature(original):
                failures.append((hex(offset), hex(target), raw.hex(), expected.hex()))
        for line in re.split(r'\\[nlp]', text):
            assert line_width(line) <= 192, (hex(offset), line)
    assert not failures, failures


def test_batch_does_not_need_fixed_table_patch(audit):
    _, _, actual = audit
    assert not any(start <= offset < end for offset in actual
                   for start, end, _ in FIXED_TABLE_RANGES)


def test_false_fragment_pointers_are_untouched(audit):
    source, built, _ = audit
    # Deux adresses fortuites dans des flux graphiques et une adresse emboîtée
    # dans un opérande de script : aucun de ces mots ne doit être repointé.
    for site in [0x51BD6C, 0x4E9294, 0x1BDF64]:
        assert built[site:site + 4] == source[site:site + 4], hex(site)


def test_dedicated_patch_is_idempotent_and_bounded(audit):
    from languages.fr.patches.meteorite_dialogue import load_combined
    from languages.pt.patches.historical_dialogue import apply

    source, built, _ = audit
    texts = load_combined(ROOT / 'languages/pt/combined_pt.txt')
    working = bytearray(built)
    assert apply(working, source, texts) == 19
    assert working == built


def test_dedicated_patch_rejects_overflow_before_any_write(audit):
    from languages.fr.patches.meteorite_dialogue import load_combined
    from languages.pt.patches.historical_dialogue import apply

    source, built, _ = audit
    texts = load_combined(ROOT / 'languages/pt/combined_pt.txt')
    texts[0x19A650] = 'a' * 200
    working = bytearray(built)
    with pytest.raises(ValueError, match='dépassement de cellule'):
        apply(working, source, texts)
    assert working == built


def test_dedicated_patch_rejects_wrong_consumer_atomically(audit):
    from languages.fr.patches.meteorite_dialogue import load_combined
    from languages.pt.patches.historical_dialogue import apply

    source, built, _ = audit
    damaged = bytearray(source)
    damaged[0x1A682F] ^= 1
    working = bytearray(built)
    texts = load_combined(ROOT / 'languages/pt/combined_pt.txt')
    with pytest.raises(ValueError, match='pointeur EN inattendu'):
        apply(working, damaged, texts)
    assert working == built


def test_dedicated_patch_rejects_changed_variable_atomically(audit):
    from languages.fr.patches.meteorite_dialogue import load_combined
    from languages.pt.patches.historical_dialogue import apply

    source, built, _ = audit
    texts = load_combined(ROOT / 'languages/pt/combined_pt.txt')
    texts[0x1A51D0] = texts[0x1A51D0].replace('<0xFD><0x05>', '<0xFD><0x06>')
    working = bytearray(built)
    with pytest.raises(ValueError, match='commandes ou pages différentes'):
        apply(working, source, texts)
    assert working == built
