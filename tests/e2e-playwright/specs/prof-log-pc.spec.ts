/** #191 : moteur mGBA réel, hors écran, puis assertions OCR sur ses pixels.
 * Prérequis macOS : mGBA avec Lua et Swift/Vision (comme le test Boîte CT).
 * La sauvegarde démarre sur une route. On lance le script existant du PC
 * dans le contexte global, juste après le contrôle d'accès au Pokédex.
 * Les textes, compteurs et pages sont produits par le jeu sans les injecter.
 * Aucun déplacement au Centre Pokémon ni sauvegarde en jeu n'est simulé.
 */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

test('le PC du Prof. Log affiche connexion, bilan et avis en français', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'prof-log-pc-'));
  fs.copyFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-fr.gba'), path.join(temp, 'game.gba'));
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
 for n=0,5 do
  if f==2300+300*n then emu:screenshot(${JSON.stringify(temp)}..'/page'..n..'.png') end
  if n<5 and f==2350+300*n then emu:addKey(0) end
  if n<5 and f==2354+300*n then emu:clearKey(0) end
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
      return fs.existsSync(path.join(temp, 'page5.png'));
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
    const pictures = Array.from({ length: 6 }, (_, n) =>
      `<img alt="Étape ${n + 1}" src="data:image/png;base64,${fs.readFileSync(path.join(temp, `page${n}.png`)).toString('base64')}">`);
    await page.setContent(`<style>body{margin:0;background:#222}main{display:grid;grid-template-columns:repeat(2,480px);gap:8px;padding:8px;width:max-content}img{width:480px;height:320px;image-rendering:pixelated}</style><main>${pictures.join('')}</main>`);
    await expect(page.getByRole('img')).toHaveCount(6);
    const texts: string[] = [];
    for (let n = 0; n < 6; n++) {
      const enlarged = path.join(temp, `readable${n}.png`);
      await page.getByRole('img').nth(n).screenshot({ path: enlarged });
      texts.push(execFileSync(ocr, [enlarged], { encoding: 'utf8', timeout: 60_000 }));
    }
    expect(texts[0]).toContain('Connexion au PC du Prof. Log');
    // Vision confond parfois les pixels de « o » et « a » dans cette police.
    // Le test ROM vérifie séparément l'orthographe exacte de chaque octet.
    expect(texts[1]).toMatch(/Évaluation du P[oa]kédex/);
    expect(texts[2]).toContain('Veux-tu une évaluation');
    expect(texts[3]).toContain('Voici ton bilan Pokédex');
    expect(texts[4]).toContain('44 Pokémon vus et');
    expect(texts[4]).toMatch(/9 P[oa]kémon capturés/);
    // Capture notamment le « A » perdu par la normalisation de FONT_NORMAL.
    expect(texts[5]).toContain('Avis du Prof. Log');
    expect(texts.join('\n')).not.toMatch(/Accessed|rating|progress|seen|owned/i);
    const proof = process.env.PROF_LOG_PROOF ?? path.join(os.tmpdir(), 'prof-log-pc-proof.png');
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
