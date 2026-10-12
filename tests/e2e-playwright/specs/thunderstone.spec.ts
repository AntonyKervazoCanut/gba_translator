/** #218 : réplique du script réel, rendue par mGBA hors écran et vérifiée par OCR. */
import { test, expect } from '@playwright/test';
import { decodePokemonText } from '../helpers/charmap.js';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

test('Le dialogue affiche une Pierre Foudre', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'thunderstone-'));
  const rom = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-fr.gba'));
  // Pointeur utilisé par le script du PNJ, même après relocation.
  const offset = rom.readUInt32LE(0x1E6A759) - 0x08000000;
  expect(offset).toBeGreaterThan(0);
  expect(offset).toBeLessThan(rom.length);
  const end = rom.indexOf(0xFF, offset);
  const decoded = decodePokemonText(rom.subarray(offset, end + 1));
  expect(decoded).toContain("J'ai utilisé une ");
  expect(decoded).toContain('Pierre Foudre');
  const scriptBase = rom.lastIndexOf(Buffer.alloc(16, 255));
  expect(scriptBase).toBeGreaterThan(0x1000000);
  rom[scriptBase] = 0x0F; rom[scriptBase + 1] = 0;
  rom.writeUInt32LE(offset + 0x08000000, scriptBase + 2);
  rom.set([0x09, 6, 2], scriptBase + 6);
  fs.writeFileSync(path.join(temp, 'game.gba'), rom);
  fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
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
 if f==2500 then emu:screenshot(${JSON.stringify(temp)}..'/dialogue.png') end
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
      return fs.existsSync(path.join(temp, 'dialogue.png'));
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
    const image = fs.readFileSync(path.join(temp, 'dialogue.png')).toString('base64');
    await page.setContent(`<style>body{margin:0}img{width:720px;height:480px;image-rendering:pixelated}</style><img alt="Pierre Foudre" src="data:image/png;base64,${image}">`);
    const readable = path.join(temp, 'readable.png');
    await page.getByRole('img').screenshot({ path: readable });
    const text = execFileSync(ocr, [readable], { encoding: 'utf8', timeout: 60_000 });
    console.log(text);
    expect(text).toMatch(/utilisé une/i);
    expect(text).toMatch(/Pierre Foudre/i);
    const proof = process.env.THUNDERSTONE_PROOF ?? path.join(os.tmpdir(), 'issue218-thunderstone-proof.png');
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
