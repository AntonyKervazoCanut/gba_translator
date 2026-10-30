"""PT-72 : consommateurs réels, police, suffixe vivant et faux pointeur audio."""
import hashlib
import re

import pytest

from languages.pt.patches.batch_72 import make_patch
from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextDecoder, TextEncoder
from tests.e2e.pt.test_batch_pt13_rom import widths
from tests.unit.pt.test_batch_pt72 import AUDIT, LIVE, ROOT

pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


@pytest.fixture(scope='module')
def built():
    return (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()


def test_exact_preimages_and_consumers(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[off:off + len(raw)] == raw
        matches = [m.start() for m in re.finditer(
            re.escape((off + 0x08000000).to_bytes(4, 'little')), source)]
        assert matches == sorted(row['references'] + row['non_text_references'])
        if row['status'] == 'exception':
            assert source[off - 24:off + 8] == bytes.fromhex(row['context_hex'])
            # Script actif précédent : msgbox 0x1f45482 puis fin ; pas de chute
            # dans la réplique non référencée 0x1f454a2.
            assert source[0x1E9DE06:0x1E9DE0F] == bytes.fromhex('0f008254f4090906c1')
        for ref in row.get('consumer_references', []):
            assert source[ref - 2:ref] == b'\x00\x05'  # trainerbattle : texte de défaite
            assert int.from_bytes(source[ref:ref + 4], 'little') == 0x09F4B6D0


def test_all_consumers_after_build_and_live_suffix(source, built):
    patch = make_patch(source)
    assert len(patch.entries()) == 299
    patch.verify(built)
    row = AUDIT['entries'][248]
    target = int.from_bytes(built[0x1E7E9BE:0x1E7E9C2], 'little') - 0x08000000
    expected = TextEncoder.encode_pokemon(
        (row['prefix_portuguese'] + row['portuguese']).replace(r'\n', '\n'), strict=True)
    assert built[target:target + len(expected)] == expected
    probe = bytearray(built)
    assert patch.apply(probe) == {'verified': 299, 'relocated': 0}
    assert probe == built


def test_native_five_font_budgets_with_expanded_buffers(built):
    for row in LIVE:
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        buffers = {(0xFD, int(k)): v for k, v in row['buffers'].items()}
        for font, expected in zip(LATIN_FONTS, row['native_widths']):
            _, table = font.offsets(built)
            measured = [w for part in re.split(b'[\xfa\xfb]', raw)
                        for w in widths(part, built, table, buffers)]
            assert measured == expected
            assert max(measured) <= row['max_width'], (row['offset'], measured)


def test_false_pointer_is_inside_referenced_pcm_sample(source, built):
    row = next(r for r in LIVE if r['non_text_references'])
    owner = row['binary_owner']
    start, end = int(owner['wave_base'], 16), int(owner['sample_end'], 16)
    assert source[start:start + 16] == bytes.fromhex(owner['header_hex'])
    assert end == start + 16 + int.from_bytes(source[start + 12:start + 16], 'little')
    for ref in owner['instrument_pointers']:
        assert int.from_bytes(source[ref:ref + 4], 'little') == start + 0x08000000
    for site in row['non_text_references']:
        assert start + 16 <= site < end
        assert built[site:site + 4] == source[site:site + 4]
    probe = bytearray(built)
    probe[0x11383A0:0x11383A4] = b'\0\0\0\x08'
    make_patch(source).apply(probe)
    assert probe == built


def test_patch_bounded_atomic_and_idempotent(source):
    patch = make_patch(source)
    rom = bytearray(source)
    assert patch.apply(rom)['verified'] == 299
    after = bytes(rom)
    assert patch.apply(rom) == {'verified': 299, 'relocated': 0}
    assert rom == after
    allowed = set()
    for _, refs, raw in patch.entries():
        for ref in refs:
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            allowed.update(range(ref, ref + 4))
            allowed.update(range(target, target + len(raw)))
    for item in patch.context_buffers:
        site = int(item['call_site'], 16)
        target = int.from_bytes(rom[site + 1:site + 5], 'little') - 0x08000000
        allowed.update(range(site + 1, site + 5))
        allowed.update(range(target, target + len(patch.wrapper(item, target))))
    assert {i for i, (a, b) in enumerate(zip(source, rom)) if a != b} <= allowed
    patch.definitions[-1] = dict(patch.definitions[-1], source_hex='00ff')
    with pytest.raises(ValueError, match='préimage'):
        patch.apply(rom)
    assert rom == after


def run_buffer_script(rom, call_site, gender):
    """Exécute les opcodes des helpers réels pour les deux genres, sans ROMReader simulé."""
    pc, stack, buffers, result, equal = call_site, [], {}, -1, False
    for _ in range(100):
        op = rom[pc]
        if op == 0xA0:  # checkgender
            result, pc = gender, pc + 1
        elif op == 0x21:  # compare VAR_RESULT, immédiat
            assert rom[pc + 1:pc + 3] == b'\x0d\x80'
            equal = result == int.from_bytes(rom[pc + 3:pc + 5], 'little')
            pc += 5
        elif op in (0x06, 0x07):  # goto_if / call_if
            assert rom[pc + 1] in (1, 5)
            take = equal if rom[pc + 1] == 1 else not equal
            target = int.from_bytes(rom[pc + 2:pc + 6], 'little') - 0x08000000
            if take:
                if op == 7:
                    stack.append(pc + 6)
                pc = target
            else:
                pc += 6
        elif op == 0x04:
            stack.append(pc + 5)
            pc = int.from_bytes(rom[pc + 1:pc + 5], 'little') - 0x08000000
        elif op == 0x85:
            target = int.from_bytes(rom[pc + 2:pc + 6], 'little') - 0x08000000
            end = rom.index(0xFF, target)
            buffers[rom[pc + 1]] = TextDecoder.decode_pokemon(rom[target:end + 1])
            pc += 6
        elif op == 3:
            pc = stack.pop()
            if not stack:
                assert pc == call_site + 5
                return buffers, result
        else:
            raise AssertionError(f'Opcode hors helper audité : {op:02x} à {pc:x}')
    raise AssertionError('Boucle dans le helper des tampons')


@pytest.mark.parametrize('gender', [0, 1], ids=['garçon', 'fille'])
def test_local_buffers_both_genders_and_original_routines(source, built, gender):
    patch = make_patch(source)
    for item in patch.context_buffers:
        site = int(item['call_site'], 16)
        old, old_result = run_buffer_script(source, site, gender)
        new, new_result = run_buffer_script(built, site, gender)
        assert new_result == old_result == gender
        routine = int(item['routine'], 16)
        size = min(24, len(bytes.fromhex(item['routine_hex'])))
        assert built[routine:routine + size] == source[routine:routine + size]
        if item['kind'] == 'fixed':
            assert new[0] == item['text']
            assert old[0] in ('his', 'her', 'boy', 'dear')
        else:
            assert old[1] == ('son' if gender == 0 else 'daughter')
            assert new[1] == (item['male'] if gender == 0 else item['female'])
            assert new[0] == old[0]
