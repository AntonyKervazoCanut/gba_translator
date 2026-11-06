/** HI-01 : Reflect Type dans un vrai combat, buffers FD0F/FD10 du moteur.
 * La copie privée donne l'effet Reflect Type à Metal Claw pour réutiliser la
 * sauvegarde de test. Aucun texte ni tampon de nom n'est injecté par la sonde.
 */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const normalize = (text: string): string => text.normalize('NFD').replace(/\p{M}/gu, '')
  .replace(/\s+/g, ' ').trim();

test('HI-01 : Reflect Type affiche les noms natifs et le changement de type en hindi', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'hi01-battle-'));
  const original = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-indie.gba'));
  const values = new Map<number, string>();
  for (const line of fs.readFileSync(path.join(root, 'languages/indie/combined_indie.txt'), 'utf8').split(/\r?\n/)) {
    const match = /^0x([\da-f]+):\s*(.*)$/i.exec(line);
    if (match) values.set(parseInt(match[1], 16), match[2]);
  }
  const translation = values.get(0x028780);
  expect(translation).toBe('<0xFD><0x0F> kaa prakaar ab\\n<0xFD><0x10> jaisaa ho gayaa!');
  const expected = execFileSync('python3', ['-c',
    'from src.core.text_codec import TextEncoder; import sys; sys.stdout.buffer.write(TextEncoder.encode_pokemon(sys.argv[1].replace(chr(92)+"n",chr(10)),strict=True))',
    translation!], { cwd: root });
  const target = original.readUInt32LE(0x02874c) - 0x08000000;
  expect(target).toBeGreaterThan(0);
  expect(target + expected.length).toBeLessThanOrEqual(original.length);
  expect(original.subarray(target, target + expected.length), 'Pointeur consommé par le script Reflect Type').toEqual(expected);

  const rom = Buffer.from(original);
  const moves = rom.readUInt32LE(0x1cc) - 0x08000000;
  const metalClaw = moves + 232 * 12;
  const reflectType = moves + 513 * 12;
  // Vérification de la version et des structures avant modification du scénario.
  expect(rom.subarray(metalClaw, metalClaw + 12)).toEqual(Buffer.from('8b32085f230a000013640000', 'hex'));
  expect(rom.subarray(reflectType, reflectType + 12)).toEqual(Buffer.from('ce0006000a00100008000209', 'hex'));
  rom.set(rom.subarray(reflectType, reflectType + 12), metalClaw);
  const script = rom.lastIndexOf(Buffer.alloc(128, 255));
  expect(script).toBeGreaterThan(0x1000000);
  // Rattata sauvage niveau 5 ; le Griknot de la fixture lance la capacité.
  rom.set([0xb6, 19, 0, 5, 0, 0, 0xb7, 2], script);
  fs.writeFileSync(path.join(temp, 'game.gba'), rom);
  const save = fs.readFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'));
  fs.writeFileSync(path.join(temp, 'game.sav'), save);
  const frames = Array.from({ length: 41 }, (_, n) => 3000 + n * 25);
  const lua = path.join(temp, 'probe.lua');
  const status = path.join(temp, 'status');
  const done = path.join(temp, 'done');
  fs.writeFileSync(lua, `
local f=0
callbacks:add('frame', function()
 f=f+1
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 if f==2020 then
  local s=io.open(${JSON.stringify(status)},'w'); s:write(tostring(emu:read8(0x03000EA8))); s:close()
  assert(emu:read8(0x03000EA8)==2, 'Script actif avant sonde')
  emu:write8(0x03000EA8,0); emu:write8(0x03000EB1,1)
  emu:write32(0x03000EB8,${script + 0x08000000})
 end
 if f>=2500 and f<=3200 and f%150==100 then emu:addKey(0) end
 if f>=2504 and f<=3204 and f%150==104 then emu:clearKey(0) end
 if f>=3000 and f<=4000 and f%25==0 then
  emu:screenshot(${JSON.stringify(temp)}..'/battle-'..f..'.png')
 end
 if f==4050 then local d=io.open(${JSON.stringify(done)},'w'); d:write('ok'); d:close() end
end)
`);
  const child = spawn(process.env.MGBA_PATH ?? '/opt/homebrew/opt/mgba/bin/mGBA', [
    '-C', 'pauseOnFocusLost=0', '-C', 'mute=1', '-C', 'videoDriver=1', '-C', 'fpsTarget=240',
    '-C', 'audioSync=0', '-C', 'videoSync=0',
    ...['savegamePath', 'savestatePath', 'screenshotPath', 'cheatsPath'].flatMap(key => ['-C', `${key}=${temp}`]),
    '--script', lua, path.join(temp, 'game.gba'),
  ], { env: { ...process.env, QT_QPA_PLATFORM: 'offscreen' }, stdio: ['ignore', 'pipe', 'pipe'] });
  let launchError: Error | undefined;
  let diagnostics = '';
  child.on('error', error => { launchError = error; });
  child.stdout?.on('data', data => { diagnostics += data.toString(); });
  child.stderr?.on('data', data => { diagnostics += data.toString(); });
  try {
    await expect.poll(() => {
      if (launchError) throw launchError;
      if (child.exitCode !== null) throw new Error(`mGBA terminé : ${child.exitCode}; ${diagnostics}`);
      if (fs.existsSync(status) && fs.readFileSync(status, 'utf8') !== '2') throw new Error(`Script déjà actif ; ${temp}`);
      return fs.existsSync(done);
    }, { timeout: 90_000 }).toBe(true);
  } finally {
    child.kill('SIGTERM');
    await new Promise<void>(resolve => {
      if (child.exitCode !== null || child.signalCode !== null || launchError) resolve();
      else child.once('exit', () => resolve());
    });
  }
  expect(fs.readFileSync(path.join(temp, 'game.sav')), 'Aucune sauvegarde en jeu').toEqual(save);
  const swift = path.join(temp, 'ocr.swift');
  fs.writeFileSync(swift, `import Foundation
import Vision
let r = VNRecognizeTextRequest()
r.recognitionLevel = .accurate
r.recognitionLanguages = ["en-US"]
r.usesLanguageCorrection = false
try VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([r])
print((r.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\\n"))
`);
  const ocr = path.join(temp, 'ocr');
  execFileSync('swiftc', [swift, '-o', ocr], { timeout: 60_000 });
  let found: string | undefined;
  const observations: string[] = [];
  for (const frame of frames) {
    const data = fs.readFileSync(path.join(temp, `battle-${frame}.png`)).toString('base64');
    await page.setContent(`<style>body{margin:0}img{width:1440px;height:960px;image-rendering:pixelated}</style><img alt="Combat Reflect Type HI-01" src="data:image/png;base64,${data}">`);
    await page.getByRole('img').evaluate(img => (img as HTMLImageElement).decode());
    const readable = path.join(temp, 'readable.png');
    await page.getByRole('img').screenshot({ path: readable });
    const text = normalize(execFileSync(ocr, [readable], { encoding: 'utf8', timeout: 60_000 }));
    observations.push(`${frame}: ${text}`);
    // Deux noms réellement résolus par les buffers de combat, dans leur ordre.
    if (/Griknot kaa prakaar ab/i.test(text) && /Rattata jaisaa ho gayaa/i.test(text)) {
      expect(text).not.toMatch(/type became|the same as/);
      expect(text.indexOf('Griknot kaa')).toBeLessThan(text.indexOf('Rattata jaisaa'));
      found = data;
      break;
    }
  }
  console.log(`Sonde : ${temp}\n${observations.join('\n')}`);
  expect(found, `Le combat doit rendre les deux lignes hindi : ${observations.join('\n')}`).toBeTruthy();
  await page.setContent(`<style>body{margin:0;background:#222;color:white;font:18px sans-serif}figure{margin:12px;width:max-content}img{width:960px;height:640px;image-rendering:pixelated}figcaption{padding:8px}</style><figure><figcaption>HI-01 — 0x028780 — Reflect Type, buffers natifs en combat</figcaption><img alt="Combat HI-01 vérifié" src="data:image/png;base64,${found}"></figure>`);
  await expect(page.getByRole('img')).toBeVisible();
  await page.getByRole('img').evaluate(img => (img as HTMLImageElement).decode());
  const proof = path.join(os.tmpdir(), 'f693-hi01-battle.png');
  await page.locator('figure').screenshot({ path: proof });
  console.log(`Preuve : ${proof}`);
});
