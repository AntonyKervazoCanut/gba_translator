"""Compile la sonde RAM ES-012 sans modifier ROM, texte ou sauvegarde."""

import argparse
import json
import struct
import subprocess
from pathlib import Path


def prepare(destination: Path, report: Path, selected: int) -> None:
    """Charge les vrais sites de pointeurs et prépare une mire de trois lignes."""
    records = [entry for entry in json.loads(report.read_text())['entries'] if 'texte' in entry]
    obj = destination / 'probe.o'
    subprocess.run([
        'clang', '--target=armv4t-none-eabi', '-mthumb', '-Os',
        '-ffreestanding', '-fno-builtin', '-c',
        str(Path(__file__).with_name('es012-text-probe.c')), '-o', str(obj),
    ], check=True)
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
    params = [len(records), selected]
    for record in records:
        params.extend([0x8000000 + int(record['references'][0], 16),
                       record['budget_px'], len(record['texte'].splitlines())])
    lua = f'''
local frames=0
callbacks:add('frame', function()
 frames=frames+1
 if frames==300 then
  local code={{{','.join(map(str, code))}}}
  for i,v in ipairs(code) do emu:write8(0x2030000+i-1,v) end
  local params={{{','.join(map(str, params))}}}
  for i,v in ipairs(params) do emu:write32(0x202b000+(i-1)*4,v) end
  emu:write32(0x202f000,0)
  emu:writeRegister('cpsr',0x3f)
  emu:writeRegister('sp',0x3007e00)
  emu:writeRegister('pc',0x2030000)
 end
 if frames==380 then
  emu:screenshot({json.dumps(str(destination / 'render.png'))})
  local rows={{}}
  for n=0,{len(records)-1} do
   table.insert(rows,'{{"target":'..tostring(emu:read32(0x202d000+n*16))..',"width":'..tostring(emu:read32(0x202d004+n*16))..',"lines":'..tostring(emu:read32(0x202d008+n*16))..',"bytes":'..tostring(emu:read32(0x202d00c+n*16))..'}}')
  end
  local f=io.open({json.dumps(str(destination / 'result.json'))},'w')
  f:write('{{"marker":'..tostring(emu:read32(0x202f000))..',"failed_index":'..tostring(emu:read32(0x202f004))..',"rows":['..table.concat(rows,',')..']}}')
  f:close()
 end
end)
'''
    (destination / 'probe.lua').write_text(lua)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    parser.add_argument('report', type=Path)
    parser.add_argument('selected', type=int)
    args = parser.parse_args()
    prepare(args.destination, args.report, args.selected)
