import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

test('maman affiche rapidement en entier dans le dialogue du Cube', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'mom-cube-'));
  fs.copyFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-fr.gba'), path.join(temp, 'game.gba'));
  fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
  const testRom = fs.readFileSync(path.join(temp, 'game.gba'));
  let textPointer = testRom.readUInt32LE(0x1E6E4E1);
  const textOffset = textPointer - 0x08000000;
  expect(textOffset).toBeGreaterThan(0);
  expect(textOffset).toBeLessThan(testRom.length);
  // Isoler la page concernée dans le dialogue vivant de maman ; conserver
  // ses octets et la vraie imprimante GBA, y compris les icônes L/R.
  let cursor = textOffset;
  for (let n = 0; n < 5; n++) {
    cursor = testRom.indexOf(0xFB, cursor) + 1;
    expect(cursor).toBeGreaterThan(textOffset);
  }
  const end = testRom.indexOf(0xFB, cursor);
  expect(end).toBeGreaterThan(cursor);
  expect(testRom.subarray(cursor, end)).not.toContain(0xFF);
  textPointer = cursor + 0x08000000;
  const scriptBase = testRom.lastIndexOf(Buffer.alloc(64, 255));
  expect(scriptBase).toBeGreaterThan(0x1000000);
  testRom.set([0x0F, 0], scriptBase);
  testRom.writeUInt32LE(textPointer, scriptBase + 2);
  testRom.set([0x09, 6, 2], scriptBase + 6);
  fs.writeFileSync(path.join(temp, 'game.gba'), testRom);
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
  emu:write32(0x03000EB8,${scriptBase + 0x08000000})
 end
 for n=0,3 do
  if f==2100+300*n then emu:screenshot(${JSON.stringify(temp)}..'/page'..n..'.png') end
  if n<3 and f==2150+300*n then emu:addKey(0) end
  if n<3 and f==2154+300*n then emu:clearKey(0) end
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
      return fs.existsSync(path.join(temp, 'page3.png'));
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
    const pictures = Array.from({ length: 4 }, (_, n) =>
      `<img alt="Étape ${n + 1}" src="data:image/png;base64,${fs.readFileSync(path.join(temp, `page${n}.png`)).toString('base64')}">`);
    await page.setContent(`<style>body{margin:0;background:#222}main{display:grid;grid-template-columns:repeat(2,720px);gap:8px;padding:8px;width:max-content}img{width:720px;height:480px;image-rendering:pixelated}</style><main>${pictures.join('')}</main>`);
    await expect(page.getByRole('img')).toHaveCount(4);
    const texts: string[] = [];
    for (let n = 0; n < 4; n++) {
      const enlarged = path.join(temp, `readable${n}.png`);
      await page.getByRole('img').nth(n).screenshot({ path: enlarged });
      texts.push(execFileSync(ocr, [enlarged], { encoding: 'utf8', timeout: 60_000 }));
    }
    const rendered = texts.join(' ').replace(/\s+/g, ' ');
    console.log(rendered);
    expect(rendered).toMatch(/parcourir rapidement\./i);
    const proof = process.env.MOM_CUBE_PROOF ?? path.join(os.tmpdir(), 'issue213-mom-cube-proof.png');
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
