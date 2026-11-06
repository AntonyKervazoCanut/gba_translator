"""Prépare la mire moteur ES-011 en RAM, sans sauvegarde ni patch de production."""
import argparse
import importlib
import json
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
Builder = importlib.import_module('src.translators.19_build_translated_rom_generic').TranslatedROMBuilder
SELECTED = (0x41D04D, 0x41D056, 0x41D096, 0x41D0D1, 0x41D0E6, 0x41D0FD, 0x41D147)


def prepare(destination: Path, report_path: Path) -> None:
    """Compile le lecteur, gèle les assertions et les lectures des consommateurs."""
    records = json.loads(report_path.read_text())['records']
    candidates = {int(e['contract_offset'], 16): e for e in json.loads(
        (ROOT / 'docs/analysis/es/011_ROUTES.json').read_text())['aliases_candidates']}
    obj = destination / 'probe.o'
    subprocess.run([
        'clang', '--target=armv4t-none-eabi', '-mthumb', '-Os', '-ffreestanding',
        '-fno-builtin', '-c', str(Path(__file__).with_name('es011-text-probe.c')),
        '-o', str(obj),
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
    selected = []
    expectations = []
    observations = []
    for index, record in enumerate(records):
        raw = bytes.fromhex(record['expected_hex'])
        source = bytes.fromhex(candidates[record['key']]['english_raw_hex'])
        commands = Builder._extract_control_sequences_from_raw(raw)
        assert commands == Builder._extract_control_sequences_from_raw(source)
        layout = record.get('layout')
        expected = {'key': record['key'], 'commands': commands}
        if layout:
            widths = Builder._encoded_layout_widths(raw, layout)
            assert max(widths) <= layout['max_width']
            assert len(widths) <= layout['max_lines']
            expected['widths'] = widths
        expectations.append(expected)
        if record['key'] in SELECTED:
            assert layout and 'glyph_widths_hex' in layout
            font = layout.get('font_id', {'small': 0, 'normal': 2, 'normal_copy': 3,
                                         'normal_copy_1': 3, 'short': 4}.get(layout['font']))
            if font is None:
                raise ValueError(f"Police inconnue : {layout['font']}")
            selected.append({'index': index, 'key': record['key'], 'font': font,
                             'pointer': record['pointers'][0], 'widths': expected['widths'],
                             'max_width': layout['max_width'], 'x': 2, 'y': 4})
        for pointer in record['pointers']:
            observations.append(f'''do
 local p=emu:read32({0x8000000 + pointer})
 local raw=''
 for j=0,{len(raw)-1} do raw=raw..string.format('%02x',emu:read8(p+j)) end
 table.insert(observations,'{{"index":{index},"pointer":{pointer},"target":'..tostring(p)..',"raw":"'..raw..'"}}')
end''')
    assert len(selected) == len(SELECTED)
    params = [[0x8000000 + e['pointer'], e['font'], e['max_width'], e['x'], e['y']]
              for e in selected]
    lua = f'''
local frames=0
local phase=0
local finished=false
local widths={{}}
local params={{{','.join('{' + ','.join(map(str,p)) + '}' for p in params)}}}
callbacks:add('frame', function()
 if finished then return end
 frames=frames+1
 if frames>=300 and (frames-300)%40==0 and phase<{len(selected)} then
  phase=phase+1
  local code={{{','.join(map(str, code))}}}
  for i,v in ipairs(code) do emu:write8(0x2030000+i-1,v) end
  for i,v in ipairs(params[phase]) do emu:write32(0x202f000+(i-1)*4,v) end
  emu:write32(0x202e01c,0)
  emu:writeRegister('cpsr',0x3f)
  emu:writeRegister('sp',0x3007e00)
  emu:writeRegister('pc',0x2030000)
 end
 if frames>=320 and (frames-320)%40==0 and phase<={len(selected)} then
  emu:screenshot({json.dumps(str(destination))}..'/render-'..tostring(phase-1)..'.png')
  table.insert(widths,'{{"target":'..tostring(emu:read32(0x202e000))..',"width":'..tostring(emu:read32(0x202e004))..',"marker":'..tostring(emu:read32(0x202e01c))..'}}')
  if phase=={len(selected)} then
   local observations={{}}
   {chr(10).join(observations)}
   local f=io.open({json.dumps(str(destination / 'result.json'))},'w')
   f:write('{{"observations":['..table.concat(observations,',')..'],"widths":['..table.concat(widths,',')..']}}')
   f:close()
   finished=true
  end
 end
end)
'''
    (destination / 'probe.lua').write_text(lua)
    (destination / 'expectations.json').write_text(json.dumps({'records': expectations, 'selected': selected}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    parser.add_argument('report', type=Path)
    args = parser.parse_args()
    prepare(args.destination, args.report)
