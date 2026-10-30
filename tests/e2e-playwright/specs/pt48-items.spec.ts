/** PT-48 : le Cube rend les descriptions livrées des objets audités, via son pointeur vivant.
 * Seule une copie temporaire remplace les champs de la Repousse de la fixture. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

for (const sample of [
  { id: 'capsule', pointer: 0x87ca94, text: 'Cápsula que permite a um Pokémon\ncom duas Habilidades trocar\nentre elas ao ser usada.' },
  { id: 'x-accuracy', pointer: 0x876f7c, text: 'Aumenta muito a Precisão.\nO efeito acaba se o Pokémon\nfor retirado da batalha.' },
  { id: 'orb', pointer: 0x87bddc, text: 'Esfera rara para Giratina segurar.\nReforça movimentos dos tipos\nDragão e Fantasma.' },
]) {
 test(`le Cube affiche les trois lignes PT-48 de ${sample.id}`, async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'pt48-items-'));
  const rom = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-pt.gba'));
  // Les pointeurs proviennent de l'audit de la table active ; aucun texte inventé en sonde.
  const target = rom.readUInt32LE(sample.pointer) - 0x08000000;
  const expected = Buffer.from(execFileSync('python3', ['-c',
    'from src.core.text_codec import TextEncoder; import sys; sys.stdout.buffer.write(TextEncoder.encode_pokemon(sys.argv[1], strict=True))', sample.text], { cwd: root }));
  expect(rom.subarray(target, target + expected.length)).toEqual(expected);
  rom.copy(rom, 0x876074 + 95 * 44, sample.pointer - 20, sample.pointer - 6);
  rom.copy(rom, 0x876074 + 95 * 44 + 20, sample.pointer, sample.pointer + 4);
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
request.recognitionLanguages = ["pt-BR", "en-US"]
request.usesLanguageCorrection = true
try VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([request])
print((request.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\\n"))
`);
    const ocr = path.join(temp, 'ocr');
    execFileSync('swiftc', [swift, '-o', ocr], { timeout: 60_000 });
    await page.setContent(`<style>body{margin:0}img{width:1440px;height:960px;image-rendering:pixelated}</style><img alt="PT-48 : description de ${sample.id}" src="data:image/png;base64,${fs.readFileSync(path.join(temp, 'page0.png')).toString('base64')}">`);
    // Deux agrandissements entiers du même écran, sans substitutions OCR.
    // Vision confond D/O à 4x et peut omettre un mot court à 6x.
    const readings: string[] = [];
    for (const scale of [4, 6]) {
      await page.getByRole('img').evaluate((img, factor) => {
        img.style.width = `${240 * factor}px`;
        img.style.height = `${160 * factor}px`;
      }, scale);
      const readable = path.join(temp, `readable-${scale}.png`);
      await page.getByRole('img').screenshot({ path: readable });
      readings.push(execFileSync(ocr, [readable], { encoding: 'utf8', timeout: 60_000 }));
    }
    const text = readings.join('\n');
    console.log(text);
    const normalized = text.normalize('NFD').replace(/\p{M}/gu, '').replace(/\s+/g, ' ');
    for (const line of sample.text.split('\n')) {
      expect(normalized).toContain(line.normalize('NFD').replace(/\p{M}/gu, ''));
    }
    expect(text).not.toContain('An item to be held');
    await page.getByRole('img').screenshot({ path: path.join(os.tmpdir(), `pt48-${sample.id}-proof.png`) });
  } finally {
    child.kill('SIGTERM');
    await new Promise<void>(resolve => {
      if (child.exitCode !== null || child.signalCode !== null || launchError) resolve();
      else child.once('exit', () => resolve());
    });
  }
});
}
