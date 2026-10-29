/** PT-43 : rendu natif des textes livrés, via une sonde msgbox temporaire.
 * Les textes proviennent des pointeurs du moteur ; aucune traduction de test
 * n'est injectée. Cette preuve ne simule pas une liaison multijoueur réelle.
 */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { normalizePortugueseOcr as normalize } from '../helpers/pt17-ocr.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

test('PT-43 : les messages de combat gardent leur texte et leurs accents dans mGBA', async ({ page }) => {
  // Arrange : une copie privée et les consommateurs réels de la ROM construite.
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'pt43-system-'));
  const original = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-pt.gba'));
  const values = new Map<number, string>();
  for (const line of fs.readFileSync(path.join(root, 'languages/pt/combined_pt.txt'), 'utf8').split('\n')) {
    const match = line.match(/^0x([\da-f]+): (.*)$/i);
    if (match) values.set(parseInt(match[1], 16), match[2]);
  }
  const scenes = [
    { offset: 0xa43d50, site: 0x9a47b8, title: 'DexNav — Pokémon incomum',
      matches: [/O DexNav detectou um/i, /Pokemon incomum/i], forbidden: /unusual|detecting/i, frames: [2450] },
    { offset: 0xa4432a, site: 0xa6b7a0, title: 'Terrain — effet CFRU et tilde PT',
      matches: [/No chao, Pokemon nao adormecem/i, /golpes Eletricos ganham forca/i], forbidden: /Grounded|fall asleep/i, frames: [2750, 3050, 3300] },
  ];
  for (let n = 0; n < scenes.length; n++) {
    const scene = scenes[n];
    const value = values.get(scene.offset);
    expect(value, `Traduction absente à ${scene.offset.toString(16)}`).toBeTruthy();
    const expected = execFileSync(process.env.PYTHON ?? 'python3', ['-c',
      'from src.core.text_codec import TextEncoder; import sys; text=sys.argv[1].replace(r"\\n", "\\n").replace(r"\\p", "<0xFB>").replace(r"\\l", "<0xFA>"); sys.stdout.buffer.write(TextEncoder.encode_pokemon(text, strict=True))', value!], { cwd: root });
    const target = original.readUInt32LE(scene.site) - 0x08000000;
    expect(target).toBeGreaterThan(0);
    expect(target + expected.length).toBeLessThanOrEqual(original.length);
    expect(original.subarray(target, target + expected.length)).toEqual(expected);
    const rom = Buffer.from(original);
    const script = rom.lastIndexOf(Buffer.alloc(128, 255));
    expect(script).toBeGreaterThan(0x1000000);
    rom.set([0x0f, 0], script);
    rom.writeUInt32LE(target + 0x08000000, script + 2);
    rom.set([0x09, 6, 2], script + 6);
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
  assert(emu:read8(0x03000EA8)==2, 'Script actif avant sonde')
  emu:write8(0x03000EA8,0); emu:write8(0x03000EB1,1)
  emu:write32(0x03000EB8,${script + 0x08000000})
 end
 if ${n === 1} then
  if f==2500 or f==2800 or f==3100 then emu:addKey(0) end
  if f==2504 or f==2804 or f==3104 then emu:clearKey(0) end
 end
 if ${scene.frames.map(frame => `f==${frame}`).join(' or ')} then
  emu:screenshot(${JSON.stringify(temp)}..'/scene${n}-'..f..'.png')
 end
 if f==3400 then local done=io.open(${JSON.stringify(path.join(temp, `scene${n}.done`))},'w'); done:write('ok'); done:close() end
end)
`);
    // Act : mGBA ne crée aucune fenêtre visible et n'écrit que dans temp.
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
        return fs.existsSync(path.join(temp, `scene${n}.done`));
      }, { timeout: 90_000 }).toBe(true);
    } finally {
      child.kill('SIGTERM');
      await new Promise<void>(resolve => {
        if (child.exitCode !== null || child.signalCode !== null || launchError) resolve();
        else child.once('exit', () => resolve());
      });
    }
  }

  const swift = path.join(temp, 'ocr.swift');
  fs.writeFileSync(swift, `
import Foundation
import Vision
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.recognitionLanguages = ["pt-BR", "en-US"]
request.usesLanguageCorrection = false
try VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([request])
print((request.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\\n"))
`);
  const ocr = path.join(temp, 'ocr');
  execFileSync('swiftc', [swift, '-o', ocr], { timeout: 60_000 });
  const verified: string[] = [];
  for (let n = 0; n < scenes.length; n++) {
    const scene = scenes[n];
    let found: string | undefined;
    const observations: string[] = [];
    for (const frame of scene.frames) {
      const data = fs.readFileSync(path.join(temp, `scene${n}-${frame}.png`)).toString('base64');
      await page.setContent(`<style>body{margin:0}img{width:960px;height:640px;image-rendering:pixelated}</style><img alt="${scene.title}" src="data:image/png;base64,${data}">`);
      await page.getByRole('img').evaluate(image => (image as HTMLImageElement).decode());
      const readable = path.join(temp, 'readable.png');
      await page.getByRole('img').screenshot({ path: readable });
      const text = normalize(execFileSync(ocr, [readable], { encoding: 'utf8', timeout: 60_000 }));
      observations.push(`${frame}: ${text}`);
      if (scene.matches.every(pattern => pattern.test(text))) {
        expect(text).not.toMatch(scene.forbidden);
        found = data;
        break;
      }
    }
    // Assert : le screenshot final est produit uniquement après reconnaissance.
    console.log(`${scene.title}: ${observations.join(' | ')}`);
    expect(found, `${scene.title}: ${observations.join(' | ')}`).toBeTruthy();
    verified.push(`<figure><figcaption>${scene.title}</figcaption><img alt="${scene.title}" src="data:image/png;base64,${found}"></figure>`);
  }
  await page.setContent(`<style>body{margin:0;background:#222;color:white;font:18px sans-serif}main{display:flex;gap:8px;padding:8px;width:max-content}figure{margin:0}img{width:720px;height:480px;image-rendering:pixelated}</style><main>${verified.join('')}</main>`);
  await expect(page.getByRole('img')).toHaveCount(2);
  await page.getByRole('img').evaluateAll(images => Promise.all(images.map(image => (image as HTMLImageElement).decode())));
  const proof = path.join(os.tmpdir(), 'f802-pt43-proof.png');
  await page.locator('main').screenshot({ path: proof });
  console.log(`Preuve : ${proof}`);
});
