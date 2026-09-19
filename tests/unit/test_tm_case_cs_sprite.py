"""Régression #189 : bitmap CS, fond et empreinte ROM préservés."""
from pathlib import Path

from languages.fr.sprites import SPRITES
from src.graphics.sprite_image import read_indexed_image
from src.graphics.sprite_rom import grid_to_tiles, tiles_to_grid

ROOT = Path(__file__).resolve().parents[2]


def test_tm_case_sprite_is_raw_and_reaches_the_live_pointer():
    sprite = SPRITES['tm_case_cs']
    assert sprite.blocks == (0xE99118,)
    assert sprite.block_pointers == ((0x1335DC,),)
    assert (sprite.tiles_wide, sprite.tiles_tall) == (2, 2)
    assert not sprite.compressed


def test_cs_letters_preserve_original_background_and_padding():
    original = (ROOT / 'tests/unit/fixtures/tm_case/hm.4bpp').read_bytes()
    before = tiles_to_grid(original, 2, 2)
    width, height, after = read_indexed_image(ROOT / 'languages/fr/sprites/tm_case_cs.png')
    assert (width, height) == (16, 16)
    c = ['.##.', '#..#', '#...', '#...', '#..#', '.##.']
    s = ['.###', '#...', '.##.', '...#', '...#', '###.']
    for start, expected in ((3, c), (9, s)):
        assert [''.join('#' if p == 7 else '.' for p in row[start:start+4])
                for row in after[3:9]] == expected
    for y in range(16):
        for x in range(16):
            if not (3 <= y < 9 and 3 <= x < 13):
                assert after[y][x] == before[y][x]
    assert len(grid_to_tiles(after, 2, 2)) == len(original) == 128
    assert {p for row in after for p in row} == {0, 6, 7}


def test_french_build_inserts_cs_after_graphics_repairs():
    recipe = (ROOT / 'Makefile').read_text()
    command = '--sprite tm_case_cs --image languages/fr/sprites/tm_case_cs.png'
    assert command in recipe
    assert recipe.index(command) > recipe.index('@$(PYTHON) $(REPAIR_LOCALIZED_LZ77_SCRIPT)')
