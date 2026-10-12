/** #222 : première obtention de Rapide Ball, rendue par le moteur réel. */
import { test, expect } from '@playwright/test';
import { decodePokemonText } from '../helpers/charmap.js';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

test('la première obtention de Rapide Ball affiche sa description', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'quick-ball-'));
  const rom = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-fr.gba'));
  const offset = rom.readUInt32LE(0x876074 + 71 * 44 + 0x14) - 0x08000000;
  expect(offset).toBeGreaterThanOrEqual(0);
  expect(offset).toBeLessThan(rom.length);
  const end = rom.indexOf(0xff, offset);
  expect(end).toBeGreaterThan(offset);
  expect(decodePokemonText(rom.subarray(offset, end + 1))).toBe("Une Ball plus efficace si elle\nest lancée au début d'un combat\ncontre un Pokémon sauvage.");
  const itemId = rom.readUInt16LE(0x876074 + 71 * 44 + 14);
  // Déclencher STD_OBTAIN_ITEM avec le vrai objet, sans remplacer son texte.
  rom.set([0x1a, 0, 0x80, itemId & 0xff, itemId >> 8, 0x1a, 1, 0x80, 1, 0, 0x09, 0, 0x02], 0x1a6a83);
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
  emu:write32(0x03000EB8,0x081A6A83)
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
    await page.setContent(`<style>body{margin:0}img{width:720px;height:480px;image-rendering:pixelated}</style><img alt="Première obtention Rapide Ball" src="data:image/png;base64,${image}">`);
    const readable = path.join(temp, 'readable.png');
    await page.getByRole('img').screenshot({ path: readable });
    const text = execFileSync(ocr, [readable], { encoding: 'utf8', timeout: 60_000 });
    expect(text).toMatch(/Rapide Ball/i);
    expect(text).toMatch(/plus efficace/i);
    expect(text).toMatch(/début d.un combat/i);
    expect(text).toMatch(/Pok[éeê][mn]on s[aq]uvage/i);
    const proof = path.join(os.tmpdir(), 'issue222-quick-ball.png');
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
