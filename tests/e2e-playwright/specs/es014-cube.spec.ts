/** F-1042 : sentinelle ES-014, vrai pipeline puis fenêtre native du Cube.
 * La copie temporaire utilise le Repel de la sauvegarde comme porte d'entrée
 * vers le nom et le pointeur de Cut. Le texte livré n'est pas réécrit.
 * Par défaut : sentinelle de fenêtre. ES014_FINAL=1 vérifie le texte final F-864. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PNG } from 'pngjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const sentinel = '¡PRUEBA ES 014!\nNiño y pingüino\n¿ÚLTIMA LÍNEA?';
interface Observation { text: string; x: number; y: number; width: number; height: number }
const normalized = (text: string): string => text.normalize('NFD').replace(/\p{M}/gu, '').toUpperCase().replace(/[^A-Z0-9]+/g, ' ').trim();

test('ES-014 conserve ses consommateurs et ses trois lignes dans le Cube', async ({ page }) => {
  const final = process.env.ES014_FINAL === '1';
  const report = JSON.parse(fs.readFileSync(path.join(root, 'docs/analysis/es/014_TRAITEMENT.json'), 'utf8')) as { entries: { offset: string; translation?: string }[] };
  const text = final ? report.entries.find(entry => entry.offset === '0x00482BD5')!.translation! : sentinel;
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'f1042-cube-'));
  const delivered = fs.readFileSync(path.join(root, final ? 'output/roms/GenedRom-es-maint.gba' : 'output/roms/GenedRom-f1042-sentinel.gba'));
  const expected = execFileSync('python3', ['-c',
    'from src.core.text_codec import TextEncoder, SPANISH_GLYPH_CHARS; import sys; sys.stdout.buffer.write(TextEncoder.encode_pokemon(sys.argv[1], skip_aliases=SPANISH_GLYPH_CHARS))',
    text], { cwd: root });
  const cut = 0x876200 + 437 * 44;
  expect(delivered.readUInt32LE(0x9A98C)).toBe(0x08876200);
  const target = delivered.readUInt32LE(cut + 20) - 0x08000000;
  expect(delivered.subarray(target, target + expected.length)).toEqual(expected);
  expect([...expected].filter(byte => byte === 0xFE)).toHaveLength(2);
  expect([...expected]).not.toContain(0xFA);
  expect([...expected]).not.toContain(0xFB);

  // La fixture possède Repel. Seuls son nom et son pointeur description sont
  // adaptés dans la copie éphémère : la vraie chaîne ES-014 reste à sa cible.
  const fixture = 0x876200 + 86 * 44;
  const rom = Buffer.from(delivered);
  delivered.copy(rom, fixture, cut, cut + 14);
  delivered.copy(rom, fixture + 20, cut + 20, cut + 24);
  const restored = Buffer.from(rom);
  delivered.copy(restored, fixture, fixture, fixture + 14);
  delivered.copy(restored, fixture + 20, fixture + 20, fixture + 24);
  expect(restored.equals(delivered)).toBe(true);
  fs.writeFileSync(path.join(temp, 'game.gba'), rom);
  const saveFixture = fs.readFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'));
  fs.writeFileSync(path.join(temp, 'game.sav'), saveFixture);
  const lua = path.join(temp, 'probe.lua');
  fs.writeFileSync(lua, `
local f=0
local keys={[2020]=3,[2070]=4,[2100]=4,[2130]=0}
callbacks:add('frame', function()
 f=f+1
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 if keys[f] then emu:addKey(keys[f]) end
 if keys[f-4] then emu:clearKey(keys[f-4]) end
 if f==2450 then emu:screenshot(${JSON.stringify(path.join(temp, 'render.png'))}) end
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
    const capture = path.join(temp, 'render.png');
    await expect.poll(() => {
      if (launchError) throw launchError;
      if (child.exitCode !== null) throw new Error(`mGBA terminé : ${child.exitCode}`);
      return fs.existsSync(capture) && fs.readFileSync(capture).subarray(-12)
        .equals(Buffer.from('0000000049454e44ae426082', 'hex'));
    }, { timeout: 90_000 }).toBe(true);
    const png = fs.readFileSync(capture);
    const dimensions = PNG.sync.read(png);
    expect([dimensions.width, dimensions.height]).toEqual([240, 160]);
    await page.setContent(`<style>body{margin:0}img{width:960px;height:640px;image-rendering:pixelated}</style><img alt="ES-014 : sonde du champ description de Cut dans le Cube" src="data:image/png;base64,${png.toString('base64')}">`);
    await page.getByRole('img').evaluate(async (image: HTMLImageElement) => image.decode());
    await expect(page.getByRole('img')).toBeVisible();
    const readable = path.join(temp, 'readable.png');
    await page.getByRole('img').screenshot({ path: readable });
    const swift = path.join(temp, 'ocr.swift');
    fs.writeFileSync(swift, `import Foundation
import Vision
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.recognitionLanguages = ["es-ES", "en-US"]
request.usesLanguageCorrection = false
try VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([request])
let result = (request.results ?? []).compactMap { item -> [String: Any]? in
 guard let text = item.topCandidates(1).first?.string else { return nil }
 let box = item.boundingBox
 return ["text": text, "x": box.minX, "y": box.minY, "width": box.width, "height": box.height]
}
print(String(data: try JSONSerialization.data(withJSONObject: result), encoding: .utf8)!)
`);
    const ocr = path.join(temp, 'ocr');
    execFileSync('swiftc', [swift, '-o', ocr], { timeout: 60_000 });
    const observations = JSON.parse(execFileSync(ocr, [readable], { encoding: 'utf8' })) as Observation[];
    console.log(observations);
    // Vision peut segmenter une ligne en plusieurs mots : regrouper leurs
    // centres verticaux, puis conserver l'ordre horizontal et toute l'emprise.
    const rows: Observation[][] = [];
    for (const observation of observations.filter(item => item.y < 0.3)) {
      const center = observation.y + observation.height / 2;
      const row = rows.find(items => Math.abs(items[0].y + items[0].height / 2 - center) < 0.03);
      if (row) row.push(observation); else rows.push([observation]);
    }
    const joined = rows.map(items => {
      items.sort((a, b) => a.x - b.x);
      const x = Math.min(...items.map(item => item.x));
      const y = Math.min(...items.map(item => item.y));
      return { text: items.map(item => item.text).join(' '), x, y,
        width: Math.max(...items.map(item => item.x + item.width)) - x,
        height: Math.max(...items.map(item => item.y + item.height)) - y };
    });
    const lines = text.split('\n').map(line => normalized(line)).map(expectedLine => {
      const observation = joined.find(item => normalized(item.text) === expectedLine);
      expect(observation, `Ligne native absente : ${expectedLine}`).toBeDefined();
      return observation!;
    });
    for (const line of lines) {
      expect(line.width * 240).toBeLessThanOrEqual(176);
      expect(line.y).toBeGreaterThan(0);
      expect(line.y).toBeLessThan(0.4);
    }
    expect(lines[0].y - lines[1].y).toBeGreaterThan(0.04);
    expect(lines[1].y - lines[2].y).toBeGreaterThan(0.04);
    expect(fs.readFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'))).toEqual(saveFixture);
    const proof = path.join(os.tmpdir(), final ? 'f864-cube-proof.png' : 'f1042-cube-proof.png');
    await page.getByRole('img').screenshot({ path: proof });
    console.log(`Preuve après assertions : ${proof}`);
  } finally {
    child.kill('SIGTERM');
    await new Promise<void>(resolve => {
      if (child.exitCode !== null || child.signalCode !== null || launchError) resolve();
      else child.once('exit', () => resolve());
    });
  }
});
