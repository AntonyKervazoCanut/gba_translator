"""PT-54 : lecteurs vivants, cellules exactes et isolation du patch final."""
import hashlib
import re
import struct

import pytest

from languages.pt.patches.batch_54 import apply_patches
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt54 import AUDIT, ROOT

pytestmark = pytest.mark.rom


def test_source_and_final_live_cells_and_actual_font_widths():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    refs = [m.start() for m in re.finditer(re.escape(struct.pack('<I', 0x0966A98C)), source)]
    assert refs == AUDIT['table_references'] and len(refs) == 42
    for ref in refs:
        assert built[ref:ref + 4] == source[ref:ref + 4]
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        target = struct.unpack_from('<I', built, 0x144)[0] - 0x08000000 + row['species_id'] * 11
        assert target == off
        assert built[target:target + 11] == source[off:off + 11] == bytes.fromhex(row['source_hex'])
        raw = TextEncoder.encode_pokemon(row['portuguese'], strict=True)
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            assert sum(built[widths + c] for c in raw[:-1]) <= 60


def test_repairs_only_manifest_cells_and_is_idempotent():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    probe = bytearray(source)
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        probe[off:off + 11] = b'\xff' * 11
    assert apply_patches(probe, source) == 300
    assert probe == source  # Tous les octets hors lot restent identiques.
    assert apply_patches(probe, source) == 300
    assert probe == source
    built = bytearray((ROOT / 'output/roms/GenedRom-pt.gba').read_bytes())
    before = bytes(built)
    apply_patches(built, source)
    assert built == before


def test_changed_reader_or_source_rejected_atomically():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    probe = bytearray(source)
    probe[AUDIT['table_references'][-1]] ^= 1
    before = bytes(probe)
    with pytest.raises(ValueError, match='Lecteur'):
        apply_patches(probe, source)
    assert probe == before
    bad_source = bytearray(source)
    bad_source[int(AUDIT['entries'][-1]['offset'], 16)] ^= 1
    probe = bytearray(source)
    with pytest.raises(ValueError, match='Préimage'):
        apply_patches(probe, bytes(bad_source))
    assert probe == source


def test_species_reader_really_indexes_eleven_byte_cells():
    # Thumb @08040FE0: ldr r7,[pc,#8]; movs r0,#11; muls r0,r5; adds r3,r0,r7.
    # Le littéral chargé est à 08040FEC ; r5 contient l'identifiant d'espèce.
    for path in ('input/roms/englishrom.gba', 'output/roms/GenedRom-pt.gba'):
        rom = (ROOT / path).read_bytes()
        assert rom[0x40FE0:0x40FE8] == bytes.fromhex('024f0b206843c319')
        assert struct.unpack_from('<I', rom, 0x40FEC)[0] == 0x0966A98C
