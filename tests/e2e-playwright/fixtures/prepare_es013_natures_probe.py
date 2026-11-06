"""Compile la sonde temporaire des natures et ses observations natives."""
import json
import struct
import subprocess
import sys
from pathlib import Path


def prepare(destination: Path) -> None:
    """Produit code Thumb relogeable et pilotage Lua, sans édition de ROM."""
    obj = destination / 'probe.o'
    subprocess.run(['clang', '--target=armv4t-none-eabi', '-mthumb', '-Os',
                    '-ffreestanding', '-fno-builtin', '-c',
                    str(Path(__file__).with_name('es013-natures-probe.c')),
                    '-o', str(obj)], check=True)
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
    lua = f'''
local frames=0
local results={{}}
local function hex(address,length)
 local s=''
 for j=0,length-1 do s=s..string.format('%02x',emu:read8(address+j)) end
 return s
end
callbacks:add('frame', function()
 frames=frames+1
 local id=math.floor((frames-300)/40)
 if id>=0 and id<25 then
  if (frames-300)%40==0 then
   local code={{{','.join(map(str, code))}}}
   for i,v in ipairs(code) do emu:write8(0x2030000+i-1,v) end
   emu:write32(0x202f000,id)
   emu:write32(0x202e07c,0)
   emu:writeRegister('cpsr',0x3f)
   emu:writeRegister('sp',0x3007e00)
   emu:writeRegister('pc',0x2030000)
  elseif (frames-300)%40==30 then
   emu:screenshot({json.dumps(str(destination))}..'/case'..tostring(id)..'.png')
   for t=0,1 do
    table.insert(results,'{{"id":'..id..',"table":'..t..',"marker":'..emu:read32(0x202e07c)..',"target":'..emu:read32(0x202e000+t*16)..',"width0":'..emu:read32(0x202e004+t*16)..',"width2":'..emu:read32(0x202e008+t*16)..',"buffer":"'..hex(0x202d000+t*32,32)..'"}}')
   end
   if id==24 then
    local f=io.open({json.dumps(str(destination / 'result.json'))},'w')
    f:write('['..table.concat(results,',')..']');f:close()
   end
  end
 end
end)
'''
    (destination / 'probe.lua').write_text(lua)


if __name__ == '__main__':
    prepare(Path(sys.argv[1]))
