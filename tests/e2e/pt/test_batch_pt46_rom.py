"""PT-46 : préimages, références et textes atteints dans le build final."""
import hashlib
import re

import pytest

from languages.pt.patches.batch_46 import make_patch
from tests.unit.pt.test_batch_pt46 import AUDIT, ROOT, ROWS

pytestmark = pytest.mark.rom


def test_real_source_preimages_and_all_references():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in ROWS:
        off = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[off:off + len(raw)] == raw
        pointer = (off + 0x08000000).to_bytes(4, 'little')
        assert [m.start() for m in re.finditer(re.escape(pointer), source)] == row['references']


def test_final_consumers_exact_bytes_and_non_overlapping_spans():
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    patch = make_patch(source)
    patch.verify(built)
    probe = bytearray(built)
    assert patch.apply(probe) == {'verified': 263, 'relocated': 0}
    assert probe == built


def test_effect_labels_and_menu_columns_fit_real_built_fonts():
    from src.core.font_glyphs import LATIN_FONTS
    from src.core.text_codec import TextEncoder

    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    labels = [r['expected'] for r in ROWS if r.get('kind') == 'move_detail']
    for font in LATIN_FONTS:
        _, widths = font.offsets(built)
        for text in labels:
            encoded = TextEncoder.encode_pokemon(text, strict=True)
            assert all(c < 0xF7 for c in encoded[:-1])
            assert sum(built[widths + c] for c in encoded[:-1]) <= 160, text
        for text in ('Lutar', 'Cube', 'Pokémon', 'Fugir', 'Voltar', 'Pegar', 'Fim'):
            encoded = TextEncoder.encode_pokemon(text, strict=True)
            assert sum(built[widths + c] for c in encoded[:-1]) <= 56, text
