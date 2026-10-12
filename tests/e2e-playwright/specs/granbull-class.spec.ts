import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

test('Le combat affiche Terreur Granbull avec son T initial (#221)', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'granbull-class-'));
  fs.copyFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-fr.gba'), path.join(temp, 'game.gba'));
  const testRom = fs.readFileSync(path.join(temp, 'game.gba'));
  const classPointer = testRom.readUInt32LE(0x23E60E) - 0x08000000;
  const expected = Buffer.from([0xCE,0xD9,0xE6,0xE6,0xD9,0xE9,0xE6,0,0xC1,0xE6,0xD5,0xE2,0xD6,0xE9,0xE0,0xE0,0xFF]);
  expect(testRom.subarray(classPointer, classPointer + expected.length)).toEqual(expected);
  // Trainer 527 is an actual Terreur Granbull Goon in gTrainers.
  expect(testRom[0x23EAC8 + 527 * 40 + 1]).toBe(14);
  const scriptBase = testRom.lastIndexOf(Buffer.alloc(64, 255));
  expect(scriptBase).toBeGreaterThan(0x1000000);
  // trainerbattle type 3 starts the real battle without an overworld intro.
  testRom.set([0x5C,3,0x0F,2,0,0], scriptBase);
  testRom.writeUInt32LE(0x08000000 + classPointer, scriptBase + 6);
  testRom[scriptBase + 10] = 2;
  fs.writeFileSync(path.join(temp, 'game.gba'), testRom);
  const lua = path.join(temp, 'probe.lua');
  fs.writeFileSync(lua, `
local f=0
callbacks:add('frame', function()
 f=f+1
 if f==1 then emu:loadStateFile(${JSON.stringify(path.join(root, 'output/roms/GenedRom-fr.ss2'))}) end
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 if f==2020 then
  assert(emu:read8(0x03000EA8)==2, 'Un script est déjà actif')
  emu:write8(0x03000EA8,0); emu:write8(0x03000EB1,1)
  emu:write32(0x03000EB8,${scriptBase + 0x08000000})
 end
 if f==2700 then emu:screenshot(${JSON.stringify(temp)}..'/page0.png') end
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
      return fs.existsSync(path.join(temp, 'page0.png'));
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
    const data = fs.readFileSync(path.join(temp, 'page0.png')).toString('base64');
    await page.setContent(`<style>body{margin:0;background:#222}img{width:480px;height:320px;image-rendering:pixelated}</style><img alt="Combat : Terreur Granbull" src="data:image/png;base64,${data}">`);
    await expect(page.getByRole('img')).toBeVisible();
    const enlarged = path.join(temp, 'readable.png');
    await page.getByRole('img').screenshot({ path: enlarged });
    const text = execFileSync(ocr, [enlarged], { encoding: 'utf8', timeout: 60_000 });
    expect(text).toMatch(/Terreur Granbull/);
    expect(text).toMatch(/Tu es d[ée]fi[ée] par/);
    const proof = path.join(os.tmpdir(), 'granbull-class-proof.png');
    await page.getByRole('img').screenshot({ path: proof });
    console.log(`Preuve : ${proof}`);
  } finally {
    child.kill('SIGTERM');
    await new Promise<void>(resolve => {
      if (child.exitCode !== null || child.signalCode !== null || launchError) resolve();
      else child.once('exit', () => resolve());
    });
  }
});
