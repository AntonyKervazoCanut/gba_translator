"""Copie temporaire ES, textes de fixture uniquement ; jamais de combined modifié."""
import json
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder


def prepare(destination: Path) -> None:
    """Compile une sonde autonome et garde les phrases attendues indépendantes."""
    rom = bytearray((ROOT / 'output/roms/GenedRom-es-maint.gba').read_bytes())
    for pointer in (0x9be13c, 0x9be0ec):
        target = struct.unpack_from('<I', rom, pointer)[0] - 0x08000000
        assert 0 <= target < len(rom) - 128
        end = rom.index(0xff, target, target + 128)
        raw = rom[target:end + 1]
        assert not any(code in raw for code in (0xfc, 0xf8, 0xf9, 0xf7))
        assert [raw[i:i + 2] for i, code in enumerate(raw) if code == 0xfd] == [b'\xfd\x0f', b'\xfd\x01']
        assert raw.count(0xfe) == 1
    obj = destination / 'probe.o'
    subprocess.run(['clang', '--target=armv4t-none-eabi', '-mthumb', '-Os', '-ffreestanding',
                    '-fno-builtin', '-c', str(Path(__file__).with_name('es008-grammar-probe.c')),
                    '-o', str(obj)], check=True)
    data = obj.read_bytes()
    offset = struct.unpack_from('<I', data, 32)[0]
    size, count, names_index = struct.unpack_from('<HHH', data, 46)
    sections = [struct.unpack_from('<10I', data, offset + i * size) for i in range(count)]
    name_section = sections[names_index]
    names = data[name_section[4]:name_section[4] + name_section[5]]
    code = b''
    for section in sections:
        name = names[section[0]:].split(b'\0')[0]
        if name == b'.rel.text':
            raise ValueError('Sonde non relogeable')
        if name == b'.text':
            code = data[section[4]:section[4] + section[5]]
    assert code and len(code) < 0x800
    assert rom[0x1fff000:] == b'\xff' * 0x1000
    rom[0x1fff000:0x1fff000 + len(code)] = code
    struct.pack_into('<I', rom, 0xb22c20, 0x203a000)

    def encode(text):
        return TextEncoder.encode_pokemon(text, skip_aliases=SPANISH_GLYPH_CHARS)

    template = bytes.fromhex('fd0f') + encode(' ha usado\n')[:-1] + bytes.fromhex('fd01ff')
    z_template = bytes.fromhex('fd0f') + encode(' ha usado\nZ-')[:-1] + bytes.fromhex('fd01ff')
    rom[0x1fffa00:0x1fffa00 + len(template)] = template
    rom[0x1fffb00:0x1fffb00 + len(z_template)] = z_template
    struct.pack_into('<I', rom, 0x9be13c, 0x9fffa00)
    struct.pack_into('<I', rom, 0x9be0ec, 0x9fffb00)
    cases = [(14, 'Danza Espada', 0), (100, 'ABCDEFGHIJKL', 0), (96, 'Meditación', 0),
             (1, 'Destructor', 0), (2, 'Golpe Kárate', 0), (14, 'Danza Espada', 1),
             (1000, 'a NORMAL move', 0)]
    table = struct.unpack_from('<I', rom, 0x9bd04c)[0] - 0x8000000
    expected = []
    for n, (move, name, z) in enumerate(cases):
        struct.pack_into('<II', rom, 0x1fff800 + n * 8, move, z)
        if move < 1000:
            raw = encode(name)
            assert len(raw) <= 13
            at = table + move * 13
            rom[at:at + len(raw)] = raw
        expected.append(encode('ABCDEFGHIJ ha usado\n' + ('Z-' if z else '') + name + '!').hex())
    struct.pack_into('<I', rom, 0x1fff838, struct.unpack_from('<I', rom, 0x6594)[0])
    (destination / 'game.gba').write_bytes(rom)
    (destination / 'expected.json').write_text(json.dumps(expected))
    (destination / 'probe.lua').write_text(f'''
local frames=0
callbacks:add('frame',function()
 frames=frames+1
 if frames==300 then
  emu:writeRegister('cpsr',0x3f)
  emu:writeRegister('sp',0x3007e00)
  emu:writeRegister('pc',0x9fff000)
 end
 if frames==320 then
  emu:screenshot('{destination}/render.png')
  local f=io.open('{destination}/result.json','w')
  f:write('{{"marker":'..emu:read32(0x202eff0)..',"buffers":[')
  for n=0,6 do
   if n>0 then f:write(',') end
   f:write('"')
   for k=0,255 do f:write(string.format('%02x',emu:read8(0x203c000+n*256+k))) end
   f:write('"')
  end
  f:write(']}}'); f:close()
 end
end)
''')


if __name__ == '__main__':
    prepare(Path(sys.argv[1]))
