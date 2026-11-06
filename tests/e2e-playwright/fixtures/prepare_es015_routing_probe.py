"""Compile une mire RAM indépendante ; les ROM et sauvegardes restent immuables."""
import argparse
import json
import struct
import subprocess
from pathlib import Path

ALIAS_KEYS = {0x721427, 0x745A54, 0x74BE3C, 0x74ED62, 0x75100E,
              0x75350F, 0x755532, 0x75B4BB, 0x75B6F4}


def prepare(destination: Path, report_path: Path, all_records: bool = False, lot: str = "es015") -> None:
    """Prépare les impressions sélectionnées et les observations de tous les lecteurs."""
    records = json.loads(report_path.read_text())['records']
    aliases = records if all_records or lot == 'es016' else [row for row in records if row['key'] in ALIAS_KEYS]
    assert all_records or len(aliases) == 9
    obj = destination / 'probe.o'
    subprocess.run(['clang', '--target=armv4t-none-eabi', '-mthumb', '-Os',
                    '-ffreestanding', '-fno-builtin', '-c',
                    str(Path(__file__).with_name('es015-routing-probe.c')),
                    '-o', str(obj)], check=True)
    data = obj.read_bytes()
    offset = struct.unpack_from('<I', data, 32)[0]
    size, count, names_index = struct.unpack_from('<HHH', data, 46)
    sections = [struct.unpack_from('<10I', data, offset+i*size) for i in range(count)]
    section = sections[names_index]
    names = data[section[4]:section[4]+section[5]]
    code = b''
    for section in sections:
        name = names[section[0]:].split(b'\0')[0]
        if name == b'.rel.text':
            raise ValueError('Sonde non relogeable')
        if name == b'.text':
            code = data[section[4]:section[4]+section[5]]
    assert code and len(code) < 0x8000
    observations = []
    for index, row in enumerate(records):
        for pointer in row['pointers']:
            observations.append(f'''do
 local target=read32({0x8000000+pointer})
 local raw=''
 for j=0,{len(bytes.fromhex(row['expected_hex']))-1} do
  raw=raw..string.format('%02x',emu:read8(target+j))
 end
 table.insert(observations,'{{"index":{index},"pointer":{pointer},"target":'..target..',"raw":"'..raw..'"}}')
end''')
    cases = []
    for index, row in enumerate(aliases):
        cases.append(f'''
 if frames=={300+index*60} then
  emu:write32(0x202f000,{0x8000000+row['pointers'][0]})
  emu:write32(0x202e000,0)
  emu:writeRegister('cpsr',0x3f)
  emu:writeRegister('sp',0x3007e00)
  emu:writeRegister('pc',0x2030000)
 end
 if frames=={350+index*60} then
  local widths={{}}
  local count=emu:read32(0x202e008)
  for j=0,count-1 do table.insert(widths,emu:read32(0x202e010+j*4)) end
  table.insert(renders,'{{"key":{row['key']},"marker":'..emu:read32(0x202e000)..',"target":'..emu:read32(0x202e004)..',"widths":['..table.concat(widths,',')..']}}')
  emu:screenshot({json.dumps(str(destination / f'render-{index}.png'))})
 end''')
    lua = f'''
local function read32(address)
 return emu:read8(address)+emu:read8(address+1)*256+emu:read8(address+2)*65536+emu:read8(address+3)*16777216
end
local frames=0
local renders={{}}
callbacks:add('frame',function()
 frames=frames+1
 if frames==299 then
  local code={{{','.join(map(str, code))}}}
  for i,v in ipairs(code)do emu:write8(0x2030000+i-1,v)end
 end
 {chr(10).join(cases)}
 if frames=={310+len(aliases)*60} then
  local observations={{}}
  {chr(10).join(observations)}
  local f=io.open({json.dumps(str(destination / 'result.json'))},'w')
  f:write('{{"observations":['..table.concat(observations,',')..'],"renders":['..table.concat(renders,',')..']}}')
  f:close()
 end
end)
'''
    (destination / 'probe.lua').write_text(lua)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    parser.add_argument('report', type=Path)
    parser.add_argument('--all-records', action='store_true')
    parser.add_argument('--lot', choices=['es015', 'es016'], default='es015')
    args = parser.parse_args()
    prepare(args.destination, args.report, args.all_records, args.lot)
