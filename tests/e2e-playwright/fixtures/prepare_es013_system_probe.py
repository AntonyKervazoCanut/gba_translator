"""Compile une sonde RAM des routes système ES-013, sans sauvegarde en jeu."""
import json
import struct
import subprocess
import sys
from pathlib import Path


def prepare(destination: Path, report: Path) -> None:
    """Vérifie les pointeurs livrés puis lance les routines natives d'expansion."""
    records = {e['key']: e for e in json.loads(report.read_text())['records']}
    keys = [0x457D44, 0x459378, 0x458FC6]
    selected = [records[key] for key in keys]
    obj = destination / 'probe.o'
    subprocess.run(['clang', '--target=armv4t-none-eabi', '-mthumb', '-Os', '-ffreestanding', '-fno-builtin', '-c', str(Path(__file__).with_name('es013-system-probe.c')), '-o', str(obj)], check=True)
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
            raise ValueError('Sonde non relogeable')
        if name == b'.text':
            code = data[section[4]:section[4] + section[5]]
    if not code:
        raise ValueError('Code Thumb absent')
    buffers = [bytes.fromhex('a2a1a1ff'), bytes.fromhex('d1' * 10 + 'ff'), bytes.fromhex('a2a1a1ff'), bytes.fromhex('d1' * 10 + 'ff')]
    pointer_values = ','.join(str(0x8000000 + e['pointers'][0]) for e in selected)
    lua = f'''
local frames=0
local function hex(address,length)
 local s=''
 for j=0,length-1 do s=s..string.format('%02x',emu:read8(address+j)) end
 return s
end
callbacks:add('frame', function()
 frames=frames+1
 if frames==300 then
  local code={{{','.join(map(str, code))}}}
  for i,v in ipairs(code) do emu:write8(0x2030000+i-1,v) end
  local pointers={{{pointer_values}}}
  for i,v in ipairs(pointers) do emu:write32(0x202f000+(i-1)*4,emu:read32(v)) end
  local buffers={{{','.join('{'+','.join(map(str,b))+'}' for b in buffers)}}}
  for n,b in ipairs(buffers) do for i,v in ipairs(b) do emu:write8(0x202f200+(n-1)*16+i-1,v) end end
  emu:write32(0x202e07c,0)
  emu:writeRegister('cpsr',0x3f);emu:writeRegister('sp',0x3007e00);emu:writeRegister('pc',0x2030000)
 elseif frames==340 then
  emu:screenshot({json.dumps(str(destination / 'native.png'))})
  local f=io.open({json.dumps(str(destination / 'result.json'))},'w')
  f:write('{{"marker":'..emu:read32(0x202e07c)..',"guards":'..emu:read32(0x202e004)..',"widths":['..emu:read32(0x202e010)..','..emu:read32(0x202e014)..','..emu:read32(0x202e018)..','..emu:read32(0x202e01c)..','..emu:read32(0x202e020)..'],"expanded":"'..hex(0x202d004,emu:read32(0x202e000))..'","tiles":"'..hex(0x2038000,20480)..'"}}');f:close()
 end
end)
'''
    (destination / 'probe.lua').write_text(lua)


if __name__ == '__main__':
    prepare(Path(sys.argv[1]), Path(sys.argv[2]))
