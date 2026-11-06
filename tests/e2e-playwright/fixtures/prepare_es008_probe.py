"""Compile une sonde RAM des sept menus sans modifier la ROM ou sauvegarder."""
import argparse
import json
import struct
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def prepare(destination: Path, report: Path) -> None:
    """Prépare le code Thumb relogeable et les lectures des consommateurs mGBA."""
    records = json.loads(report.read_text())['records']
    obj = destination / 'probe.o'
    subprocess.run([
        'clang', '--target=armv4t-none-eabi', '-mthumb', '-Os',
        '-ffreestanding', '-fno-builtin', '-c',
        str(Path(__file__).with_name('es008-menu-probe.c')), '-o', str(obj),
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
    params = []
    observations = []
    for index, record in enumerate(records):
        params.extend([0x8000000 + record['pointers'][0],
                       0 if record['layout']['font'] == 'small' else 2,
                       record['layout']['max_width']])
        for pointer in record['pointers']:
            observations.append(f'''do
 local p=emu:read32({0x8000000 + pointer})
 local raw=''
 for j=0,{len(bytes.fromhex(record['expected_hex']))-1} do
  raw=raw..string.format('%02x',emu:read8(p+j))
 end
 table.insert(observations,'{{"index":{index},"pointer":{pointer},"target":'..tostring(p)..',"raw":"'..raw..'"}}')
end''')
    lua = f'''
local frames=0
callbacks:add('frame', function()
 frames=frames+1
 if frames==300 then
  local code={{{','.join(map(str, code))}}}
  for i,v in ipairs(code) do emu:write8(0x2030000+i-1,v) end
  local params={{{','.join(map(str, params))}}}
  for i,v in ipairs(params) do emu:write32(0x202f000+(i-1)*4,v) end
  emu:writeRegister('cpsr',0x3f)
  emu:writeRegister('sp',0x3007e00)
  emu:writeRegister('pc',0x2030000)
 end
 if frames==330 then
  emu:screenshot({json.dumps(str(destination / 'render.png'))})
  local observations={{}}
  {chr(10).join(observations)}
  local widths={{}}
  for n=0,6 do
   table.insert(widths,'{{"target":'..tostring(emu:read32(0x202e000+n*12))..',"width":'..tostring(emu:read32(0x202e004+n*12))..',"x":'..tostring(emu:read32(0x202e008+n*12))..'}}')
  end
  local f=io.open({json.dumps(str(destination / 'result.json'))},'w')
  f:write('{{"marker":'..tostring(emu:read32(0x202e07c))..',"observations":['..table.concat(observations,',')..'],"widths":['..table.concat(widths,',')..']}}')
  f:close()
 end
end)
'''
    (destination / 'probe.lua').write_text(lua)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    parser.add_argument('report', type=Path)
    args = parser.parse_args()
    prepare(args.destination, args.report)
