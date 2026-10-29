/** B-1031 : fenêtre native du Cube, sans sauvegarde en jeu. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';


test('les trois lignes de la description gItems restent visibles', async ({ page }) => {

  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'b1031-cube-'));
  const rom = fs.readFileSync('output/roms/GenedRom-es-maint.gba');
  const contract = JSON.parse(fs.readFileSync('languages/es-maint/item_descriptions.json','utf8'));
  const report=JSON.parse(fs.readFileSync('docs/analysis/es/003_TRAITEMENT.json','utf8'));
  for(const entry of contract.entries) {
    const e=report.entries.find((e: {offset:string})=>Number(e.offset)===Number(entry.offset));
    for(const ref of entry.pointer_offsets) {
      const target=rom.readUInt32LE(ref)-0x08000000;
      const expected=Buffer.from(e.expected_hex,'hex');
      expect(rom.subarray(target,target+expected.length).equals(expected)).toBe(true);
    }
  }
  fs.writeFileSync(path.join(temp, 'game.gba'), rom);
  fs.copyFileSync('tests/fixtures/saves/party_hp_bar_fr.sav', path.join(temp, 'game.sav'));
  fs.writeFileSync(path.join(temp, 'probe.lua'), `
local f=0
local keys={[2020]=3,[2070]=4,[2100]=4,[2130]=0,[2220]=7,[2250]=7,[2280]=7,[2310]=7,[2340]=7}
callbacks:add('frame', function()
 f=f+1
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 if keys[f] then emu:addKey(keys[f]) end
 if keys[f-4] then emu:clearKey(keys[f-4]) end
 if f==2450 then emu:screenshot(${JSON.stringify(path.join(temp,'render.png'))}) end
end)
`);
  const child = spawn('/opt/homebrew/opt/mgba/bin/mGBA', [
    '-C','mute=1','-C','videoDriver=1','-C','fpsTarget=240','-C','audioSync=0','-C','videoSync=0',
    ...['savegamePath','savestatePath','screenshotPath','cheatsPath'].flatMap(k=>['-C',`${k}=${temp}`]),
    '--script',path.join(temp,'probe.lua'),path.join(temp,'game.gba'),
  ], {env:{...process.env,QT_QPA_PLATFORM:'offscreen'},stdio:'ignore'});
  try {
    await expect.poll(()=>fs.existsSync(path.join(temp,'render.png')),{timeout:90000}).toBe(true);
    const png=fs.readFileSync(path.join(temp,'render.png'));
    await page.setContent(`<img alt="Cube gItems" style="width:960px;image-rendering:pixelated" src="data:image/png;base64,${png.toString('base64')}">`);
    await page.getByRole('img').evaluate(async (i: HTMLImageElement)=>i.decode());
    await expect(page.getByRole('img')).toBeVisible();
    const readable=path.join(temp,'readable.png');
    await page.getByRole('img').screenshot({path:readable});
    const swift=path.join(temp,'ocr.swift');
    fs.writeFileSync(swift, `import Foundation
import Vision
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.usesLanguageCorrection = false
try VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([request])
print((request.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: " "))
`);
    execFileSync('swiftc',[swift,'-o',path.join(temp,'ocr')]);
    const text=execFileSync(path.join(temp,'ocr'),[readable],{encoding:'utf8'});
    expect(text).toMatch(/Medicina en espray que cura/i);
    expect(text).toMatch(/heridas y rest[ao]ura 50 PS/i);
    expect(text).toMatch(/de un Pokémon/i);
    await page.getByRole('img').screenshot({path:path.join(os.tmpdir(),'f853-cube-proof.png')});
    console.log(temp);
  } finally { child.kill('SIGTERM'); }
});
