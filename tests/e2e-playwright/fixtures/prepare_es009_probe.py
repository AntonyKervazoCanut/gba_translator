"""Prépare la sonde RAM des colonnes et expansions natives, sans écriture ROM."""
import argparse
import json
from pathlib import Path


def compile_probe(destination: Path, source: Path) -> bytes:
    """Compile un programme Thumb relogeable pour les sondes RAM natives."""
    import struct
    import subprocess
    obj = destination / 'probe.o'
    subprocess.run(['clang', '--target=armv4t-none-eabi', '-mthumb', '-Os',
                    '-ffreestanding', '-fno-builtin', '-c',
                    str(source),
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
    return code


def prepare(destination: Path, report: Path) -> None:
    """Compile avec la primitive ELF existante puis pilote chaque surface."""
    # Même compilation ELF que la sonde précédente, sans réinsertion parallèle.
    records = json.loads(report.read_text())['records']
    code = compile_probe(destination, Path(__file__).with_name('es009-formatted-probe.c'))
    cases = []
    selected = [(index, record, False) for index, record in enumerate(records)]
    selected += [(index, record, True) for index, record in enumerate(records)
                 if record.get('source_hex') and record['source_hex'] != record['expected_hex']
                 and record['layout'].get('buffers')]
    for case_index, (index, record, negative) in enumerate(selected):
        layout = record['layout']
        buffer = layout.get('buffers', {}).get('0')
        # Le surnom maximal est volontairement une valeur runtime temporaire.
        probe = bytes.fromhex(buffer.get('probe_hex', 'd1' * buffer['max_bytes'] + 'ff')) if buffer else b''
        if probe and probe[-1] != 255:
            probe += b'\xff'
        width = 144 if buffer else layout['max_width'] + 8
        raw = bytes.fromhex(record['source_hex']) if negative else b''
        pc_index = (record['pointers'][0] - 0x3CEA88) // 8 if buffer else 0
        if record['key'] == 0x41825C:
            pc_index = 23  # même texte aux lecteurs nickname et item sélectionné
        cases.append(f'''{{case={case_index},index={index},negative={str(negative).lower()},pc_index={pc_index},raw={{{','.join(map(str, raw))}}},pointer={0x8000000 + record['pointers'][0]},font={layout['initial_font']},width={width},buffer={{{','.join(map(str, probe))}}}}}''')
    refs = []
    for index, record in enumerate(records):
        for site in record['pointers']:
            refs.append(f"{{index={index},site={site},length={len(bytes.fromhex(record['expected_hex']))}}}")
    lua = f'''
local cases={{{','.join(cases)}}}
local refs={{{','.join(refs)}}}
local frames=0
local results={{}}
local function hex(address,length)
 local s=''
 for j=0,length-1 do s=s..string.format('%02x',emu:read8(address+j)) end
 return s
end
callbacks:add('frame', function()
 frames=frames+1
 local n=math.floor((frames-300)/40)+1
 if n>=1 and n<=#cases then
  local c=cases[n]
  if (frames-300)%40==0 then
   local code={{{','.join(map(str, code))}}}
   for i,v in ipairs(code) do emu:write8(0x2030000+i-1,v) end
   for i,v in ipairs(c.buffer) do emu:write8(0x202f200+i-1,v) end
   local pointer=c.pointer
   if c.negative then
    for i,v in ipairs(c.raw) do emu:write8(0x202f400+i-1,v) end
    emu:write32(0x202f300,0x202f400);pointer=0x202f300
   end
   emu:write32(0x202f000,pointer)
   emu:write32(0x202f004,c.font)
   emu:write32(0x202f008,c.width)
   emu:write32(0x202f00c,#c.buffer)
   emu:write32(0x202f010,c.pc_index)
   emu:write32(0x202f014,not c.negative and #c.buffer>0 and 1 or 0)
   emu:write32(0x202e07c,0)
   emu:writeRegister('cpsr',0x3f)
   emu:writeRegister('sp',0x3007e00)
   emu:writeRegister('pc',0x2030000)
  elseif (frames-300)%40==30 then
   emu:screenshot({json.dumps(str(destination))}..'/case'..tostring(c.case)..'.png')
   local dynamic=emu:read32(0x203f34c)
   table.insert(results,'{{"case":'..tostring(c.case)..',"negative":'..tostring(c.negative)..',"index":'..tostring(c.index)..',"marker":'..tostring(emu:read32(0x202e07c))..',"target":'..tostring(emu:read32(0x202e000))..',"width":'..tostring(emu:read32(0x202e004))..',"window":'..tostring(emu:read32(0x202e008))..',"x":'..tostring(emu:read32(0x202e00c))..',"column":'..tostring(emu:read32(0x202e010))..',"guards":'..tostring(emu:read32(0x202e018))..',"expanded":"'..hex(0x202d000,not c.negative and #c.buffer>0 and 80 or 256)..'","buffer":"'..hex(#c.buffer>0 and dynamic or 0x202f200,#c.buffer)..'"}}')
   if n==#cases then
    local readers={{}}
    for _,r in ipairs(refs) do
     local target=emu:read32(0x8000000+r.site)
     table.insert(readers,'{{"index":'..r.index..',"site":'..r.site..',"target":'..target..',"raw":"'..hex(target,r.length)..'"}}')
    end
    local f=io.open({json.dumps(str(destination / 'result.json'))},'w')
    f:write('{{"cases":['..table.concat(results,',')..'],"readers":['..table.concat(readers,',')..']}}');f:close()
   end
  end
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
