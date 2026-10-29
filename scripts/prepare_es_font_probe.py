"""Prépare une sonde temporaire appelant les cinq décompresseurs du moteur GBA."""
import argparse
import json
import struct
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def prepare(destination: Path) -> None:
    """Compile le code Thumb sans lien externe et génère le script mGBA."""
    obj = destination / 'probe.o'
    subprocess.run(['clang', '--target=armv4t-none-eabi', '-mthumb', '-Os', '-ffreestanding', '-fno-builtin', '-c', str(ROOT / 'tests/e2e-playwright/fixtures/es-font-probe.c'), '-o', str(obj)], check=True)
    data = obj.read_bytes()
    offset = struct.unpack_from('<I', data, 32)[0]
    size, count, names_index = struct.unpack_from('<HHH', data, 46)
    sections = [struct.unpack_from('<10I', data, offset + i * size) for i in range(count)]
    names_section = sections[names_index]
    names = data[names_section[4]:names_section[4] + names_section[5]]
    code = None
    for section in sections:
        name = names[section[0]:].split(b'\0')[0]
        if name == b'.rel.text':
            raise ValueError('La sonde doit être entièrement relogeable')
        if name == b'.text':
            code = data[section[4]:section[4] + section[5]]
    if not code:
        raise ValueError('Code Thumb absent')
    glyphs = bytes.fromhex('17 1b 6f 23 27 f6 29 02 06 5a 0e 12 f3 14 52 51')
    params = [0x8006449, 0x80064F1, 0x80065B9, 0x8006725, 0x80067ED, *glyphs, 0x8B1E11C, 0x8B1E280, 0x8E82EA0, 0x8E9BF48]
    lua = f'''
local frames=0
callbacks:add('frame', function()
 frames=frames+1
 if frames==300 then
  emu:screenshot('{destination}/boot.png')
  local code={{{','.join(map(str, code))}}}
  for i,v in ipairs(code) do emu:write8(0x2030000+i-1,v) end
  local params={{{','.join(map(str, params))}}}
  for i,v in ipairs(params) do emu:write32(0x202f000+(i-1)*4,v) end
  emu:writeRegister('cpsr',0x3f)
  emu:writeRegister('sp',0x3007e00)
  emu:writeRegister('pc',0x2030000)
 end
 if frames==320 then
  emu:screenshot('{destination}/render.png')
  local f=io.open('{destination}/result.json','w')
  f:write('{{"marker":'..tostring(emu:read32(0x202eff0))..',"pc":'..tostring(emu:readRegister('pc'))..'}}')
  f:close()
 end
end)
'''
    (destination / 'probe.lua').write_text(lua)
    (destination / 'glyphs.json').write_text(json.dumps(list(glyphs)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    prepare(parser.parse_args().destination)
