"""PT-20 : pointeurs réels, isolation et injection finale dans la ROM PT."""
import hashlib
import re
import struct
from pathlib import Path

import pytest

from languages.pt.patches.batch_20 import make_patch
from tests.unit.pt.test_batch_pt20 import AUDIT

ROOT = Path(__file__).resolve().parents[3]
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


def test_source_references_and_consumer_contexts(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        hits = [m.start() for m in re.finditer(re.escape(struct.pack('<I', offset + 0x08000000)), source)]
        assert hits == row['references']
        for ref, context in zip(hits, row['reference_contexts']):
            assert source[ref - 2:ref + 5].hex() == context
    # Fausses chaînes : les pointeurs mènent à des scripts, pas à une msgbox.
    assert source[0x744F97:0x744F99] == b'\x06\x01'
    assert source[0x762EE4] == 0
    assert source[0x777C0C:0x777C10] == struct.pack('<I', 0x08721344)


def test_every_live_entry_reaches_final_rom(source):
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    patch = make_patch(source)
    assert len(patch.entries()) == 201
    patch.verify(built)
    # Préserver la connexion sud de Route 3, gardée hors de la liste de textes.
    assert built[0x72132C:0x72134C] == source[0x72132C:0x72134C]
    for offset in (0x74037D, 0x745132):
        # Les scripts continuent d'exécuter les mêmes opcodes avant leur texte.
        assert built[offset:offset + 2] == source[offset:offset + 2]
        if offset == 0x745132:
            # 0F 00 <pointeur> 09 06 02 : PT-25 traduit légitimement la cible
            # 0x7C56CA. Son test vérifie le texte livré ; seuls les opcodes
            # doivent rester identiques ici, pas les quatre octets du pointeur.
            assert built[offset + 6:offset + 9] == source[offset + 6:offset + 9]


def test_patch_is_atomic_idempotent_and_bounded(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 201
    first = bytes(rom)
    assert patch.apply(rom) == {'verified': 201, 'relocated': 0}
    assert bytes(rom) == first
    allowed = set()
    for _, refs, encoded in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = struct.unpack_from('<I', rom, ref)[0] - 0x08000000
            allowed.update(range(target, target + len(encoded)))
    assert all(i in allowed for i, (a, b) in enumerate(zip(source, rom)) if a != b)
    broken = bytearray(source)
    broken[0x741625] ^= 1
    with pytest.raises(ValueError, match='préimage'):
        make_patch(bytes(broken)).apply(rom)
    assert bytes(rom) == first


def test_actual_font_budgets_in_final_rom(source):
    from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
    from src.core.font_glyphs import LATIN_FONTS

    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    rows = {int(r['offset'], 16): r for r in AUDIT['entries']}
    for offset, _, raw in make_patch(source).entries():
        # Les tampons runtime réservent neuf glyphes larges ; les couleurs ne
        # consomment aucun pixel. Les limites sont mesurées aux pointeurs finaux.
        for command in _extract_control_sequences_from_raw(raw):
            if command[0] == 0xFD:
                raw = raw.replace(bytes(command), b'\xd1' * 9)
            elif command[0] not in (0xFA, 0xFB, 0xFE):
                raw = raw.replace(bytes(command), b'')
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            for line in re.split(b'[\xfa\xfb\xfe\xff]', raw):
                assert sum(built[widths + c] for c in line) <= rows[offset]['max_width'], (
                    hex(offset), hex(font.glyph_pointer), line.hex())
