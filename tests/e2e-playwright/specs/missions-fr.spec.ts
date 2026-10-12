import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

test('les libellés de missions sont affichés en français par le moteur', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'missions-fr-'));
  const rom = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-fr.gba'));
  // Pointeurs vivants des scripts : aucun texte de substitution.
  // Le script PC sert uniquement de fenêtre de rendu; la mission n'est pas jouée.
  const pointers = [rom.readUInt32LE(0x1eaf5c8), rom.readUInt32LE(0x1ea5eff)];
  // Réutiliser le script PC éprouvé pour afficher les deux chaînes vivantes.
  rom.writeUInt32LE(pointers[0], 0x1a6a88);
  rom.writeUInt32LE(pointers[1], 0x1a6a90);
  rom[0x1a6a8d] = 6;
  rom[0x1a6a95] = 6;

  fs.writeFileSync(path.join(temp, 'game.gba'), rom);
  fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
  fs.writeFileSync(path.join(temp, 'probe.lua'), `
local f=0
local function show(pointer)
 assert(emu:read8(0x03000EA8)==2, 'Un script est déjà actif')
 -- Buffers FRLG vérifiés dans la ROM; le bilan attend un compteur terminé.
 for _,address in ipairs({0x02021CD0,0x02021CF0,0x02021D04}) do
  emu:write8(address,0xA1)
  emu:write8(address+1,0xFF)
 end
 emu:write8(0x03000EA8,0)
 emu:write8(0x03000EB1,1)
 emu:write32(0x03000EB8,pointer)
end
callbacks:add('frame',function()
 f=f+1
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 if f==2020 then show(${0x8000000+0x1a6a83}) end
 if f==2320 then emu:screenshot(${JSON.stringify(temp)}..'/page0.png') end
 if f==2350 then emu:addKey(0) end
 if f==2354 then emu:clearKey(0) end
 if f==2820 then emu:screenshot(${JSON.stringify(temp)}..'/page1.png') end
end)
`);
  const child = spawn(process.env.MGBA_PATH ?? '/opt/homebrew/opt/mgba/bin/mGBA', [
    '-C','mute=1','-C','videoDriver=1','-C','fpsTarget=240','-C','audioSync=0','-C','videoSync=0',
    ...['savegamePath','savestatePath','screenshotPath','cheatsPath'].flatMap(key=>['-C',`${key}=${temp}`]),
    '--script',path.join(temp,'probe.lua'),path.join(temp,'game.gba'),
  ], {env:{...process.env,QT_QPA_PLATFORM:'offscreen'},stdio:['ignore','pipe','pipe']});
  child.stdout?.on('data', data => { if (process.env.DEBUG) process.stdout.write(data); });
  child.stderr?.on('data', data => { if (process.env.DEBUG) process.stderr.write(data); });
  try {
    await expect.poll(()=>fs.existsSync(path.join(temp,'page1.png')),{timeout:90_000}).toBe(true);
    child.kill('SIGTERM');
    await new Promise<void>(resolve=>child.once('exit',()=>resolve()));
    const swift = path.join(temp, 'ocr.swift');
    fs.writeFileSync(swift, `
import Foundation
import Vision
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.recognitionLanguages = ["fr-FR", "en-US"]
request.usesLanguageCorrection = false
try VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([request])
print((request.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\\n"))
`);
    const ocr = path.join(temp, 'ocr');
    execFileSync('swiftc', [swift, '-o', ocr], { timeout: 60_000 });
    const pictures = [0,1].map(n=>`<img alt="Mission ${n}" src="data:image/png;base64,${fs.readFileSync(path.join(temp,`page${n}.png`)).toString('base64')}">`);
    await page.setContent(`<style>body{margin:0;background:#222}main{display:flex;gap:8px;padding:8px;width:max-content}img{width:480px;height:320px;image-rendering:pixelated}</style><main>${pictures.join('')}</main>`);
    const texts: string[] = [];
    for (let n=0;n<2;n++) {
      const enlarged=path.join(temp,`readable${n}.png`);
      await page.getByRole('img').nth(n).screenshot({path:enlarged});
      texts.push(execFileSync(ocr,[enlarged],{encoding:'utf8'}));
    }
    expect(texts[0]).toContain('Missions complétées');
    expect(texts[1]).toContain('Enfant perdue');
    expect(texts.join('\n')).not.toMatch(/Missions Completed|Abandonment Issues/);
    await page.locator('main').screenshot({path:path.join(os.tmpdir(),'issue210-missions-proof.png')});
  } finally {
    if (child.exitCode===null && child.signalCode===null) child.kill('SIGTERM');
  }
});
