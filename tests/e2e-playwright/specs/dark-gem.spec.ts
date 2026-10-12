/** #200 : nom réel du Joyau Ténébr rendu dans le Cube, hors écran.
 * Une copie temporaire remplace le nom de la Repousse possédée par celui du joyau. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

test('le Cube affiche Joyau Ténébr sans texte anglais', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'dark-gem-'));
  const rom = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-fr.gba'));
  const name = rom.subarray(0x87CA28, 0x87CA28 + 14);
  expect(name.subarray(0, 13).toString('hex')).toBe('c4e3edd5e900ce1be21bd6e6ff');
  // La Repousse de la sauvegarde permet d'exercer le rendu du même champ fixe.
  name.copy(rom, 0x876074 + 95 * 44);
  // Le descriptif associé au joyau garde la capture cohérente.
  rom.copy(rom, 0x876074 + 95 * 44 + 20, 0x87CA28 + 20, 0x87CA28 + 24);
  fs.writeFileSync(path.join(temp, 'game.gba'), rom);
  fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
  const lua = path.join(temp, 'probe.lua');
  fs.writeFileSync(lua, `
local f=0
callbacks:add('frame', function()
 f=f+1
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 local keys={[2020]=3,[2070]=4,[2100]=4,[2130]=0}
 if keys[f] then emu:addKey(keys[f]) end
 if keys[f-4] then emu:clearKey(keys[f-4]) end
 if f==2450 then emu:screenshot(${JSON.stringify(temp)}..'/page0.png') end
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
    await page.setContent(`<style>body{margin:0}img{width:960px;height:640px;image-rendering:pixelated}</style><img alt="Cube : Joyau Ténébr" src="data:image/png;base64,${fs.readFileSync(path.join(temp, 'page0.png')).toString('base64')}">`);
    const readable = path.join(temp, 'readable.png');
    await page.getByRole('img').screenshot({ path: readable });
    const text = execFileSync(ocr, [readable], { encoding: 'utf8', timeout: 60_000 });
    console.log(text);
    // L'OCR varie sur les accents de la police pixel ; les octets sont
    // vérifiés exactement avant le lancement de l'émulateur.
    expect(text.normalize('NFD').replace(/\p{M}/gu, '')).toContain('Joyau Tenebr');
    expect(text).not.toContain('Dark Gem');
    await page.getByRole('img').screenshot({ path: path.join(os.tmpdir(), 'dark-gem-proof.png') });
  } finally {
    child.kill('SIGTERM');
    await new Promise<void>(resolve => {
      if (child.exitCode !== null || child.signalCode !== null || launchError) resolve();
      else child.once('exit', () => resolve());
    });
  }
});
