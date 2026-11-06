"""Exécute les cinq branches originales ; aucun texte ES livré dans ces fixtures."""
from __future__ import annotations

import json
import struct
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from unicorn import Uc

FIXTURE = json.loads((Path(__file__).parent / 'fixtures/es008_grammar.json').read_text())


def machine(rom: bytes | None = None) -> Uc:
    """Charge les octets réels, sans remplacer les routines de copie du moteur."""
    from unicorn import UC_ARCH_ARM, UC_MODE_THUMB, Uc

    cpu = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    for address, size in [(0x08000000, 0x2000000), (0x02000000, 0x40000), (0x03000000, 0x8000), (0x04000000, 0x1000)]:
        cpu.mem_map(address, size)
    if rom is not None:
        cpu.mem_write(0x08000000, rom)
    else:
        for address, value in FIXTURE['segments'].items():
            cpu.mem_write(0x08000000 + int(address, 16), bytes.fromhex(value))
    cpu.mem_write(0x02039A34, struct.pack('<I', 0x02022BC8))
    return cpu


def call(cpu: Uc, address: int, argument: int) -> None:
    """Appelle du Thumb et exige un retour normal, pas une limite d'instructions."""
    from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_SP

    cpu.reg_write(UC_ARM_REG_SP, 0x03007000)
    cpu.reg_write(UC_ARM_REG_LR, 0x03007F01)
    cpu.reg_write(UC_ARM_REG_R0, argument)
    cpu.emu_start(address | 1, 0x03007F00, count=100000)
    from unicorn.arm_const import UC_ARM_REG_PC
    assert cpu.reg_read(UC_ARM_REG_PC) == 0x03007F00


@pytest.mark.emulator
@pytest.mark.parametrize('move,suffix', [(14, '00dde7ff'), (100, '00dde7ff'),
                                        (96, '00dde7ff'), (1, 'b4e7ff'), (2, 'b4e7ff')])
def test_original_groups_copy_particle_and_append_only_exclamation(move, suffix):
    # Arrange : buffers de 16 octets avec sentinelles ; nom long de 14 octets.
    cpu = machine()
    cpu.mem_write(0x02022BC8, struct.pack('<H', move))
    cpu.mem_write(0x02022AB7, b'\xa5' * 50)
    cpu.mem_write(0x02022AC8, b'\xbb' * 14 + b'\xff')

    # Act : fonctions réellement appelées par CFRU.
    call(cpu, 0x080D86C8, 0x02022AB8)
    call(cpu, 0x080D8720, 0x02022AC8)

    # Assert : copie (pas concaténation), FF et aucune écriture hors tampon.
    expected = bytes.fromhex(suffix)
    assert bytes(cpu.mem_read(0x02022AB8, len(expected))) == expected
    assert bytes(cpu.mem_read(0x02022AB8 + len(expected), 16 - len(expected))) == b'\xa5' * (16 - len(expected))
    assert bytes(cpu.mem_read(0x02022AC8, 16)) == b'\xbb' * 14 + b'\xab\xff'
    assert bytes(cpu.mem_read(0x02022AB7, 1)) == b'\xa5'
    assert bytes(cpu.mem_read(0x02022AD8, 16)) == b'\xa5' * 16


def test_particle_fixture_has_five_bounded_groups_and_live_literals():
    segments = {int(k, 16): bytes.fromhex(v) for k, v in FIXTURE['segments'].items()}
    routine = segments[0xd86c8]
    assert struct.unpack_from('<I', routine, 0xd8704 - 0xd86c8)[0] == 0x083fe88b
    assert struct.unpack_from('<I', routine, 0xd871c - 0xd86c8)[0] == 0x083fe88f
    groups = struct.unpack('<118H', segments[0x3fea70])
    assert groups.count(0) == 4
    assert len(segments[0x3fd586]) == 10
    assert segments[0x3fd586] == b'\xab\xff' * 5


@pytest.mark.rom
@pytest.mark.emulator
@pytest.mark.parametrize('rom_name', ['input/roms/englishrom.gba', 'output/roms/GenedRom-es-maint.gba'])
@pytest.mark.parametrize('move,move_name,z_move', [
    (14, 'Danza Espada', 0), (100, 'ABCDEFGHIJKL', 0), (96, 'Meditación', 0),
    (1, 'Destructor', 0), (2, 'Golpe Kárate', 0), (14, 'Danza Espada', 1),
    (1000, 'NORMAL', 0),
])
def test_live_root_ignores_particle_in_complete_spanish_sentence(rom_name, move, move_name, z_move):
    """Sonde temporaire : traduction des phrases réservée à F-858, jamais persistée."""
    from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE

    from src.core.text_codec import SPANISH_GLYPH_TABLE, TextEncoder

    encode = lambda text: TextEncoder.encode_pokemon(text, skip_aliases=frozenset(SPANISH_GLYPH_TABLE))
    rom = Path(rom_name).read_bytes()
    cpu = machine(rom)
    cpu.mem_write(0x08B22C20, struct.pack('<I', 0x0203A000))
    cpu.mem_write(0x02023FE8, struct.pack('<I', 0x0203B000))
    cpu.mem_write(0x02022BC8, struct.pack('<H', move))
    cpu.mem_write(0x02022BD4, bytes([z_move]))
    cpu.mem_write(0x0202428C, encode('ABCDEFGHIJ'))  # nickname: maximum 10 caractères
    cpu.mem_write(0x02022AB7, b'\xa5' * 50)
    cpu.mem_write(0x0202298B, b'\xa5' * 257)
    # Les pointeurs du vrai sélecteur, pas une expansion Python de FD.
    template = bytes.fromhex('fd0f') + encode(' ha usado\n')[:-1] + bytes.fromhex('fd01ff')
    cpu.mem_write(0x09FFF000, template)
    cpu.mem_write(0x089BE13C, struct.pack('<I', 0x09FFF000))
    z_template = bytes.fromhex('fd0f') + encode(' ha usado\nZ-')[:-1] + bytes.fromhex('fd01ff')
    cpu.mem_write(0x09FFF100, z_template)
    cpu.mem_write(0x089BE0EC, struct.pack('<I', 0x09FFF100))
    if move < 1000:
        name_table = struct.unpack_from('<I', rom, 0x9bd04c)[0]
        cpu.mem_write(name_table + move * 13, encode(move_name))
    else:
        # Branche type générique : conserve les octets source pour le nom réel.
        move_name = 'a NORMAL move'
    reads, writes, templates = [], [], []
    expanding = [False]

    def trace(machine, address, size, data):
        if address == 0x080D77F4:
            templates.append(machine.reg_read(UC_ARM_REG_R0))
            expanding[0] = True

    def read(machine, access, address, size, value, data):
        if expanding[0] and 0x02022AB8 <= address < 0x02022AC8:
            reads.append(address)

    def write(machine, access, address, size, value, data):
        if 0x0202298B <= address < 0x02022AE9:
            writes.append((address, size))

    from unicorn.arm_const import UC_ARM_REG_R0
    cpu.hook_add(UC_HOOK_CODE, trace)
    cpu.hook_add(UC_HOOK_MEM_READ, read)
    cpu.hook_add(UC_HOOK_MEM_WRITE, write)
    call(cpu, 0x080D7274, 4)  # point d'entrée public → trampoline CFRU

    expected = encode('ABCDEFGHIJ ha usado\n' + ('Z-' if z_move else '') + move_name + '!')
    assert templates == [0x09FFF100 if z_move else 0x09FFF000]
    assert bytes(cpu.mem_read(0x0202298C, len(expected))) == expected
    assert reads == [], 'Le fragment grammatical ne doit pas être lu par la phrase'
    assert all(0x0202298C <= a and a + n <= 0x0202298C + len(expected)
               or 0x02022AB8 <= a and a + n <= 0x02022AE9 for a, n in writes)
    assert bytes(cpu.mem_read(0x0202298B, 1)) == b'\xa5'
    assert bytes(cpu.mem_read(0x0202298C + len(expected), 1)) == b'\xa5'


@pytest.mark.rom
@pytest.mark.parametrize('rom_name', ['input/roms/englishrom.gba', 'output/roms/GenedRom-es-maint.gba'])
def test_particle_consumers_and_cfru_entry_are_unchanged(rom_name):
    """Fige les lecteurs réels, pas seulement les faux débuts du combined."""
    rom = Path(rom_name).read_bytes()
    for at, raw in FIXTURE['segments'].items():
        start, expected = int(at, 16), bytes.fromhex(raw)
        assert rom[start:start + len(expected)] == expected
    assert rom[0xd7274:0xd727c] == bytes.fromhex('0049084789da9b08')
    assert struct.unpack_from('<I', rom, 0x9be0d0)[0] == 0x080d86c9
    assert struct.unpack_from('<I', rom, 0x9be0e0)[0] == 0x080d8721
    for pointer in [0x9be13c, 0x9be0ec]:
        target = struct.unpack_from('<I', rom, pointer)[0] - 0x08000000
        assert 0 <= target < len(rom) - 128
        end = rom.index(0xff, target, target + 128)
        raw = rom[target:end + 1]
        # Ces deux templates n'ont que FD + son argument, FE et FF.
        # Contrôler le pointeur vivant permet la traduction/relocalisation F-858.
        assert not any(code in raw for code in [0xfc, 0xf8, 0xf9, 0xf7])
        assert [raw[i:i + 2] for i, code in enumerate(raw) if code == 0xfd] == [b'\xfd\x0f', b'\xfd\x01']
        assert raw.count(0xfe) == 1
    if rom_name.startswith('input/'):
        assert struct.unpack_from('<I', rom, 0x9be13c)[0] == 0x083fd57b
        assert struct.unpack_from('<I', rom, 0x9be0ec)[0] == 0x08a4c42b
        assert rom[0x3fd57b:0x3fd586] == bytes.fromhex('fd0f00e9e7d9d8fefd01ff')
    for target, locations in [(0x3fe88b, [0xd8704]), (0x3fe88c, []), (0x3fe88f, [0xd871c])]:
        found, cursor = [], 0
        needle = struct.pack('<I', 0x08000000 + target)
        while (cursor := rom.find(needle, cursor)) >= 0:
            found.append(cursor)
            cursor += 1
        assert found == locations


@pytest.mark.rom
@pytest.mark.parametrize('rom_name', ['input/roms/englishrom.gba', 'output/roms/GenedRom-es-maint.gba'])
def test_particle_has_only_the_audited_direct_and_indirect_callers(rom_name):
    rom = Path(rom_name).read_bytes()
    assert rom.count(struct.pack('<I', 0x080d86c9)) == 1
    assert struct.pack('<I', 0x080d86c8) not in rom
    callers = []
    for address in range(0, len(rom) - 4, 2):
        first, second = struct.unpack_from('<HH', rom, address)
        if first & 0xf800 == 0xf000 and second & 0xf800 == 0xf800:
            delta = ((first & 0x7ff) << 12) | ((second & 0x7ff) << 1)
            if delta & (1 << 22):
                delta -= 1 << 23
            if address + 4 + delta == 0xd86c8:
                callers.append(address)
    assert callers == [0xd75f2]
