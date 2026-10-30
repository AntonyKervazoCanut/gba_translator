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


def test_battle_pages_fit_with_long_names_and_stat_buffers():
    from src.core.font_glyphs import LATIN_FONTS
    from src.core.text_codec import TextEncoder
    from tests.e2e.pt.test_batch_pt13_rom import widths

    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    for row in ROWS:
        if row.get('kind') != 'battle':
            continue
        buffers = {(0xFD, k): 'W' * 10 for k in range(64)}
        buffers.update({(0xFD, k): 'O adversário ' + 'W' * 10 for k in (15, 16, 17, 19)})
        buffers.update({(0xFD, k): 'adversária' for k in (0x35, 0x36, 0x37, 0x38)})
        buffers.update({(0xFD, k): 'W' * 13 for k in (0x1C, 0x32)})
        buffers.update({(0xFD, k): 'W' * 12 for k in (0x1D, 0x33)})
        buffers[(0xFD, 20)] = 'W' * 12  # mouvement : cellule de 13 octets
        buffers[(0xFD, 22)] = 'W' * 13  # objet
        # Les buffers de stat sont plus longs qu'un surnom de dix lettres.
        if row['offset'] in ('0xa4b2f9', '0xa4be45', '0xa4c200'):
            buffers[(0xFD, 0)] = 'Defesa Especial'
        if row['offset'] == '0xa4c200':
            buffers[(0xFD, 1)] = 'subiu drasticamente!'
        raw = TextEncoder.encode_pokemon(row['expected'].replace(r'\n', '\n'), strict=True)
        for font in LATIN_FONTS:
            _, table = font.offsets(built)
            for page in re.split(b'[\xfa\xfb]', raw):
                assert max(widths(page, built, table, buffers)) <= 214, row['offset']
