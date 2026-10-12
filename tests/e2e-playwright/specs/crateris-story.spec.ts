import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { decodePokemonText } from '../helpers/charmap.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

test('le récit de Cratéris défile sans couper la téléportation ni la fin', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'crateris-'));
  const rom = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-fr.gba'));
  // Le véritable script du PNJ charge ce pointeur, même si le build reloge le texte.
  const offset = rom.readUInt32LE(0x1E5B206) - 0x08000000;
  expect(offset).toBeGreaterThanOrEqual(0);
  expect(offset).toBeLessThan(rom.length);
  const end = rom.indexOf(0xFF, offset);
  expect(end).toBeGreaterThan(offset);
  const bytes = rom.subarray(offset, end + 1);
  const text = decodePokemonText(bytes);
  expect(text).toContain('Borrius Est, en sécurité.');
  expect(text).toContain("Je n'oublierai jamais son acte\nhéroïque.");
  const screens = 1 + [...bytes].filter(byte => byte === 0xFA || byte === 0xFB).length;
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
  emu:write32(0x03000EB8,0x09E5B204)
 end
 for n=0,${screens - 1} do
  if f==2400+240*n then emu:screenshot(${JSON.stringify(temp)}..'/page'..n..'.png') end
  if n<${screens - 1} and f==2440+240*n then emu:addKey(0) end
  if n<${screens - 1} and f==2444+240*n then emu:clearKey(0) end
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
      return fs.existsSync(path.join(temp, `page${screens - 1}.png`));
    }, { timeout: 150_000 }).toBe(true);
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
    const pictures = Array.from({ length: screens }, (_, n) =>
      `<img alt="Étape ${n + 1}" src="data:image/png;base64,${fs.readFileSync(path.join(temp, `page${n}.png`)).toString('base64')}">`);
    await page.setContent(`<style>body{margin:0;background:#222}main{display:grid;grid-template-columns:repeat(2,480px);gap:8px;padding:8px;width:max-content}img{width:480px;height:320px;image-rendering:pixelated}</style><main>${pictures.join('')}</main>`);
    await expect(page.getByRole('img')).toHaveCount(screens);
    const texts: string[] = [];
    for (let n = 0; n < screens; n++) {
      const enlarged = path.join(temp, `readable${n}.png`);
      await page.getByRole('img').nth(n).screenshot({ path: enlarged });
      texts.push(execFileSync(ocr, [enlarged], { encoding: 'utf8', timeout: 60_000 }));
    }
    expect(texts[0]).toContain('Il y a vingt ans');
    const teleport = texts.findIndex(text => /Borrius Est, en sécurité/.test(text));
    expect(teleport, 'La phrase signalée doit être visible et complète').toBeGreaterThan(0);
    // La flèche animée voisine du point peut être reconnue comme de la ponctuation.
    // Le point final est déjà contrôlé dans les octets de la ROM ci-dessus.
    expect(texts[teleport].replace(/\s+/g, ' ')).toContain('téléporté tout le monde vers Borrius Est, en sécurité');
    // Vision confond parfois a/o, c/o et é/ê dans cette police pixelisée.
    // Garder la phrase entière et sa ponctuation ; les octets sont vérifiés exactement.
    expect(texts.at(-1)?.replace(/\s+/g, ' ')).toMatch(/Je n.oublierai j[ao]mais son a[co]te h[éê]ro[iï]que\./);
    const selected = [0, teleport - 1, teleport, screens - 1];
    await page.locator('main').evaluate((main, selected) => {
      [...main.children].forEach((child, index) => {
        if (!selected.includes(index)) child.remove();
      });
    }, selected);
    const proof = process.env.CRATERIS_PROOF ?? path.join(os.tmpdir(), 'issue203-crateris-proof.png');
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
