"""PT-86 : lecteurs natifs, tables fixes, PCM et mesure des polices finales."""
import hashlib
import re

import pytest

from languages.pt.patches.batch_86 import Batch86Patch, make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths
from tests.unit.pt.test_batch_pt86 import AUDIT, LIVE, ROOT, ROWS

pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_every_live_pointer_delivers_complete_text(source, built):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    patch = make_patch(source)
    assert len(patch.entries()) == 295
    patch.verify(built)
    for row in ROWS:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        matches = [m.start() for m in re.finditer(
            re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert matches == sorted(row['references'] + row['non_text_references'])
        for ref, context in zip(row['references'], row['reference_contexts']):
            assert source[ref - 2:ref + 5].hex() == context
        for site in row['non_text_references']:
            assert built[site:site + 4] == source[site:site + 4]


def test_font_budgets_and_fixed_price_columns(built):
    for row in LIVE:
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        buffers = {(0xFD, n): 'W' * 10 for n in range(256)}
        # FD04 is a plural suffix in the streak result and gendered pronoun in Big Mo's speech.
        if row['index'] == 41:
            buffers[(0xFD, 4)] = 's'
            for code in (7, 8, 9):
                buffers[(0xFD, code)] = 'W' * 13
        elif row['index'] in (45, 46):
            for code in (2, 3, 4):
                buffers[(0xFD, code)] = 'W' * 13
        elif row['index'] == 56:
            buffers[(0xFD, 4)] = 'você'
        for font in LATIN_FONTS:
            measured = [width for segment in re.split(b'[\xfa\xfb]', raw)
                        for width in widths(segment, built, font.offsets(built)[1], buffers)]
            assert max(measured) <= row['max_width'], (row['index'], row['offset'], measured)


def test_false_pointer_instructions_and_pcm_remain_intact(source, built):
    for row in ROWS:
        for pcm in row.get('pcm_matches', []):
            base, ref, site = pcm['wave_base'], pcm['instrument_pointer'], pcm['site']
            assert source[base:base + 16].hex() == pcm['header_hex']
            assert int.from_bytes(source[ref:ref + 4], 'little') == base + 0x08000000
            assert base + 16 <= site <= base + 12 + int.from_bytes(source[base + 12:base + 16], 'little')
            assert built[site:site + 4] == source[site:site + 4]
        for block in row.get('binary_matches', []):
            base, raw = block['base'], bytes.fromhex(block['source_hex'])
            assert source[base:base + len(raw)] == raw
            assert built[base:base + len(raw)] == raw
    for child, parent in ((89, 88), (165, 164), (206, 205)):
        row, owner = ROWS[child], ROWS[parent]
        delta = int(row['offset'], 16) - int(owner['offset'], 16)
        assert bytes.fromhex(owner['source_hex'])[delta:] == bytes.fromhex(row['source_hex'])
        assert not row['references'] and owner['references']
    orphan = ROWS[212]
    offset = int(orphan['offset'], 16)
    assert not orphan['references'] and not orphan['non_text_references']
    assert built[offset:offset + 7] == source[offset:offset + 7]


def test_cfru_long_class_pointer_cells_and_lookup_tables(source, built):
    for index, class_id in ((279, 22), (280, 26)):
        ref = ROWS[index]['references'][0]
        assert ref == 0x23E558 + class_id * 13
        # Le padding de la cellule précédente appartient à PT-03 et peut être
        # remis à zéro par sa traduction. Seule cette cellule appartient au test.
        assert built[ref + 4:ref + 13] == source[ref + 4:ref + 13]
    for row in ROWS[23:33]:
        ref = row['references'][0]
        assert built[ref + 4:ref + 8] == source[ref + 4:ref + 8]


def test_patch_atomic_idempotent_and_bounded(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 295
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 295, 'relocated': 0}
    assert bytes(rom) == after
    allowed = set()
    for helper in patch.HELPERS:
        for site in helper[1]:
            target = int.from_bytes(rom[site:site + 4], 'little') - 0x08000000
            allowed.update(range(target, target + len(patch._helper_bytes(helper, target))))
            allowed.update(range(site, site + 4))
    for _, refs, encoded in patch.entries():
        for ref in refs:
            allowed.update(range(ref, ref + 4))
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(target, target + len(encoded)))
    assert {i for i, (a, b) in enumerate(zip(source, rom)) if a != b} <= allowed
    patch.definitions[0] = dict(patch.definitions[0], source_hex='00ff')
    with pytest.raises(ValueError, match='préimage'):
        patch.apply(rom)
    assert bytes(rom) == after
    with pytest.raises(ValueError, match='préimage ROM'):
        make_patch(bytes(1) + source[1:])


def test_big_mo_pronoun_is_scoped_to_one_call(source, built):
    target = int.from_bytes(built[Batch86Patch.PRONOUN_CALL:Batch86Patch.PRONOUN_CALL + 4], 'little') - 0x08000000
    assert built[target:target + 5] == b'\x04' + (Batch86Patch.ORIGINAL_HELPER + 0x08000000).to_bytes(4, 'little')
    assert built[target + 5:target + 7] == b'\x85\x02'
    text = int.from_bytes(built[target + 7:target + 11], 'little') - 0x08000000
    assert built[text:text + len(Batch86Patch.PRONOUN)] == Batch86Patch.PRONOUN
    assert built[target + 11] == 3
    # Autres appels et script genré global hors lot inchangés.
    for site in (0x1EAB697, 0x1EAB733):
        assert built[site:site + 4] == source[site:site + 4]
    # Les pointeurs de texte du helper peuvent être localisés par d'autres lots.
    # Son branchement de genre reste natif.
    assert built[0x1EAB8FD:0x1EAB915] == source[0x1EAB8FD:0x1EAB915]


def test_vocatives_preserve_out_of_batch_callers(source, built):
    patch = make_patch(source)
    for helper in patch.HELPERS:
        original, sites, _, _ = helper
        for site in sites:
            target = int.from_bytes(built[site:site + 4], 'little') - 0x08000000
            expected = patch._helper_bytes(helper, target)
            assert built[target:target + len(expected)] == expected
        for match in re.finditer(re.escape((original + 0x08000000).to_bytes(4, 'little')), source):
            if match.start() not in sites:
                assert built[match.start():match.start() + 4] == source[match.start():match.start() + 4]
    # Les autres appels utilisent toujours les préparateurs globaux.
    assert built[0x1EA7B75:0x1EA7B96] == source[0x1EA7B75:0x1EA7B96]
    assert built[0x1EA5F21:0x1EA5F3B] == source[0x1EA5F21:0x1EA5F3B]
