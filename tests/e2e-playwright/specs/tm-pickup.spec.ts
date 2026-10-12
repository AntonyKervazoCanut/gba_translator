import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

test('la découverte CT54 conserve deux lignes puis une page de rangement (#219)', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'tm-pickup-'));
  fs.copyFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-fr.gba'), path.join(temp, 'game.gba'));
  fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
  const rom = fs.readFileSync(path.join(temp, 'game.gba'));
  // Pointeurs vivants du script natif de ramassage, après le build.
  const found = rom.readUInt32LE(0x1a6822);
  const stored = rom.readUInt32LE(0x1a681a);
  expect(rom.subarray(found - 0x08000000, found - 0x08000000 + 2)).toEqual(Buffer.from([0xfd, 1]));
  const script = rom.lastIndexOf(Buffer.alloc(32, 255));
  expect(script).toBeGreaterThan(0x1000000);
  // Deux msgbox du moteur, lisant les textes du jeu sans réinjecter leur contenu.
  for (const [n, pointer] of [found, stored].entries()) {
    const at = script + n * 8;
    rom.set([0x0f, 0], at);
    rom.writeUInt32LE(pointer, at + 2);
    rom.set([0x09, 6], at + 6);
  }
  rom[script + 16] = 2;
  fs.writeFileSync(path.join(temp, 'game.gba'), rom);
  const lua = path.join(temp, 'probe.lua');
  fs.writeFileSync(lua, `
local f=0
callbacks:add('frame', function()
 f=f+1
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 if f==2020 then
  assert(emu:read32(0x03000F0C)==0x0815F9B4, 'ABI du contexte script inattendue')
  assert(emu:read8(0x03000EA8)==2, 'Un script est déjà actif')
  emu:write8(0x03000EA8,0)
  emu:write8(0x03000EB1,1)
  -- Buffers de CT54 : Faux-Chage, CT54 et Boîte CT, encodés CFRU.
  local values={
   [0x02021CD0]={0xC0,0xD5,0xE9,0xEC,0xAE,0xBD,0xDC,0xD5,0xDB,0xD9,0xFF},
   [0x02021CF0]={0xBD,0xCE,0xA6,0xA5,0xFF},
   [0x02021D04]={0xBC,0xE3,0x20,0xE8,0xD9,0,0xBD,0xCE,0xFF}}
  for address,bytes in pairs(values) do
   for i,b in ipairs(bytes) do emu:write8(address+i-1,b) end
  end
  emu:write32(0x03000EB8,${script + 0x08000000})
 end
 for n=0,1 do
  if f==2300+300*n then emu:screenshot(${JSON.stringify(temp)}..'/page'..n..'.png') end
  if n<1 and f==2350+300*n then emu:addKey(0) end
  if n<1 and f==2354+300*n then emu:clearKey(0) end
 end
end)
`);
  const child = spawn(process.env.MGBA_PATH ?? '/opt/homebrew/opt/mgba/bin/mGBA', [
    '-C', 'mute=1', '-C', 'videoDriver=1', '-C', 'fpsTarget=240',
    '-C', 'audioSync=0', '-C', 'videoSync=0',
    ...['savegamePath', 'savestatePath', 'screenshotPath', 'cheatsPath'].flatMap(key => ['-C', `${key}=${temp}`]),
    '--script', lua, path.join(temp, 'game.gba'),
  ], { env: { ...process.env, QT_QPA_PLATFORM: 'offscreen' }, stdio: 'ignore' });
  let launchError: Error | undefined;
  child.on('error', error => { launchError = error; });
  try {
    await expect.poll(() => {
      if (launchError) throw launchError;
      if (child.exitCode !== null) throw new Error(`mGBA terminé : ${child.exitCode}`);
      return fs.existsSync(path.join(temp, 'page1.png'));
    }, { timeout: 90_000 }).toBe(true);
    child.kill('SIGTERM');
    await new Promise<void>(resolve => child.once('exit', () => resolve()));
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
    const pictures = Array.from({ length: 2 }, (_, n) =>
      `<img alt="Étape ${n + 1}" src="data:image/png;base64,${fs.readFileSync(path.join(temp, `page${n}.png`)).toString('base64')}">`);
    await page.setContent(`<style>body{margin:0;background:#222}main{display:grid;grid-template-columns:repeat(2,480px);gap:8px;padding:8px;width:max-content}img{width:480px;height:320px;image-rendering:pixelated}</style><main>${pictures.join('')}</main>`);
    await expect(page.getByRole('img')).toHaveCount(2);
    const texts: string[] = [];
    for (let n = 0; n < 2; n++) {
      const enlarged = path.join(temp, `readable${n}.png`);
      await page.getByRole('img').nth(n).screenshot({ path: enlarged });
      texts.push(execFileSync(ocr, [enlarged], { encoding: 'utf8', timeout: 60_000 }));
    }
    console.log(texts);
    expect(texts[0]).toMatch(/a trouvé la CT54 !/);
    expect(texts[0]).toContain('Elle contient Faux-Chage.');
    expect(texts[0]).toMatch(/CT54 !\nElle contient/);
    expect(texts[0]).not.toContain('range');
    expect(texts[1]).toMatch(/range CT54/);
    expect(texts[1]).toMatch(/dans la Bo[iî]te CT/);
    expect(texts[1]).not.toContain('Elle contient');
    const proof = process.env.TM_PICKUP_PROOF ?? path.join(os.tmpdir(), 'tm-pickup-proof.png');
    await page.locator('main').screenshot({ path: proof });
    console.log(`Preuve : ${proof}`);
  } finally {
    child.kill('SIGTERM');
    await new Promise<void>(resolve => {
      if (child.exitCode !== null || child.signalCode !== null || launchError) resolve();
      else child.once('exit', () => resolve());
    });
  }
});
