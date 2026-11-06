"""Vue des glyphes natifs des autres textes ES-009, sans simulation de scénario."""
import argparse
import json
from pathlib import Path

from prepare_es009_probe import compile_probe


def prepare(destination: Path, report: Path) -> None:
    """Expanse les sentinelles attendues et prépare les appels natifs en RAM."""
    records = json.loads(report.read_text())['glyph_records']
    code = compile_probe(destination, Path(__file__).with_name('es009-glyph-probe.c'))
    cases = []
    for record in records:
        raw = bytes.fromhex(record['expected_hex'])
        expanded = bytearray()
        i = 0
        numeric = record['key'] == 0x418188
        while i < len(raw):
            value = raw[i]
            if value == 0xFD:
                argument = raw[i+1]
                assert argument in (1, 2, 3, 4)
                expanded.extend(b'\xd1' * 7 if argument == 1 else
                                b'\xaa' * 4 if numeric else b'\xd1' * 10)
                i += 2
            elif value == 0xFC:
                command = raw[i+1]
                size = {8: 3, 9: 2, 0x10: 4}[command]
                expanded.extend(raw[i:i+size])
                i += size
            else:
                expanded.append(value)
                i += 1
        pages = [bytearray()]
        i = 0
        while i < len(expanded)-1:
            value = expanded[i]
            if value in (0xFA, 0xFB):
                pages.append(bytearray())
                i += 1
            elif value == 0xFC:
                i += {8: 3, 9: 2, 0x10: 4}[expanded[i+1]]
            else:
                pages[-1].append(value)
                i += 1
        for page_index, page in enumerate(pages):
            if not page:
                continue
            cases.append({**record, 'page_index': page_index,
                          'page_hex': (page+b'\xff').hex(),
                          'expanded_hex': expanded.hex(), 'numeric': numeric,
                          'font': record.get('font') or (1 if b'\xfe' in page else 2)})
    (destination / 'cases.json').write_text(json.dumps(cases))
    lua_cases = ','.join(f"{{target={e['target'] + 0x8000000},page={e['page_index']},font={e['font']},numeric={int(e['numeric'])},std={0 if e.get('std_id') is None else e['std_id']+1},length={len(bytes.fromhex(e['expected_hex']))}}}" for e in cases)
    lua = f'''
local cases={{{lua_cases}}}
local frames=0
local result={{}}
local n=1
local started=false
local readyAt=nil
local function hex(address,length)
 local s=''
 for j=0,length-1 do s=s..string.format('%02x',emu:read8(address+j)) end
 return s
end
callbacks:add('frame', function()
 frames=frames+1
 if frames>=300 and n<=#cases then
  local c=cases[n]
  if not started then
   started=true
   local code={{{','.join(map(str, code))}}}
   for i,v in ipairs(code) do emu:write8(0x2030000+i-1,v) end
   emu:write32(0x202f000,c.target);emu:write32(0x202f004,c.page)
   emu:write32(0x202f008,c.font);emu:write32(0x202f00c,c.numeric)
   emu:write32(0x202f010,c.std)
   emu:write32(0x202e07c,0)
   emu:writeRegister('cpsr',0x3f);emu:writeRegister('sp',0x3007e00)
   emu:writeRegister('pc',0x2030000)
  elseif emu:read32(0x202e07c)==0xf859 then
   if not readyAt then readyAt=frames+1 end
   if frames>=readyAt then
   emu:screenshot({json.dumps(str(destination))}..'/glyph'..n..'.png')
   table.insert(result,'{{"marker":'..emu:read32(0x202e07c)..',"target":'..emu:read32(0x202e000)..',"width":'..emu:read32(0x202e004)..',"guards":'..emu:read32(0x202e010)..',"std_guards":'..emu:read32(0x202e01c)..',"std_status":'..emu:read32(0x202e020)..',"std_raw":"'..hex(0x202ec00,emu:read32(0x202e018))..'","page":"'..hex(0x202e800,emu:read32(0x202e008)+1)..'","expanded":"'..hex(0x202d000,emu:read32(0x202e00c))..'","raw":"'..hex(c.target,c.length)..'"}}')
   if n==#cases then
    local f=io.open({json.dumps(str(destination / 'result.json'))},'w')
    f:write('['..table.concat(result,',')..']');f:close()
   end
   n=n+1;started=false;readyAt=nil
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
