/** HI-01 : garde d'exclusion du script Reflect Type historique supplanté.
 * La sonde donne Reflect Type au premier Pokémon en RAM pour réutiliser la
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

test('HI-01 : Reflect Type conserve sa copie active EN hors lot et exclut la copie historique', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'hi01-battle-'));
  const original = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-indie.gba'));
  const values = new Map<number, string>();
  for (const line of fs.readFileSync(path.join(root, 'languages/indie/combined_indie.txt'), 'utf8').split(/\r?\n/)) {
    const match = /^0x([\da-f]+):\s*(.*)$/i.exec(line);
    if (match) values.set(parseInt(match[1], 16), match[2]);
  }
  expect(values.has(0x028780), 'Copie historique exclue du lot HI-01').toBe(false);
  const source = fs.readFileSync(path.join(root, 'input/roms/englishrom.gba'));
  const expected = execFileSync('python3', ['-c',
    'from src.core.text_codec import TextEncoder; import sys; sys.stdout.buffer.write(TextEncoder.encode_pokemon(sys.argv[1].replace(chr(92)+"n",chr(10)),strict=True))',
    "<0xFD><0x0F>'s type became\\nthe same as <0xFD><0x10>'s!"], { cwd: root });
  for (const [offset, site] of [[0x028780, 0x02874c], [0x96be0c, 0x96806e]]) {
    expect(source.readUInt32LE(site)).toBe(offset + 0x08000000);
    expect(original.readUInt32LE(site), 'Pointeur EN inchangé').toBe(source.readUInt32LE(site));
    expect(source.subarray(offset, offset + expected.length)).toEqual(expected);
    expect(original.subarray(offset, offset + expected.length), 'Texte EN inchangé').toEqual(expected);
  }

  const rom = Buffer.from(original);
  const moves = rom.readUInt32LE(0x1cc) - 0x08000000;
  const metalClaw = moves + 232 * 12;
  // CFRU utilise ici l'identifiant 654 (513 désigne Defend Order).
  const reflectType = moves + 654 * 12;
  const names = rom.readUInt32LE(0x308a4) - 0x08000000;
  expect(rom.subarray(names + 654 * 13, names + 655 * 13)).toEqual(Buffer.from('ccd9dae0d9d7e800ceede4d9ff', 'hex'));
  // Vérification de la version et des structures avant modification du scénario.
  expect(rom.subarray(metalClaw, metalClaw + 12)).toEqual(Buffer.from('8b32085f230a000013640000', 'hex'));
  expect(rom.subarray(reflectType, reflectType + 12)).toEqual(Buffer.from('1e0000000f0000000200020b', 'hex'));
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
  -- CFRU conserve les sous-structures de l'équipe déchiffrées en RAM.
  -- Modifier l'identifiant est nécessaire : l'effet Conversion est partagé,
  -- puis le moteur choisit la branche Reflect Type selon le mouvement 654.
  local party=0x02024284
  assert(emu:read16(party+0x2C)==232, 'Premier mouvement fixture inattendu')
  emu:write16(party+0x2C,654); emu:write8(party+0x34,15)
  local checksum=0
  for address=party+0x20,party+0x4E,2 do checksum=(checksum+emu:read16(address))%65536 end
  emu:write16(party+0x1C,checksum)
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
    await page.setContent(`<style>body{margin:0}img{width:1440px;height:960px;image-rendering:pixelated}</style><img alt="Reflect Type hors lot, anglais conservé" src="data:image/png;base64,${data}">`);
    await page.getByRole('img').evaluate(img => (img as HTMLImageElement).decode());
    const readable = path.join(temp, 'readable.png');
    await page.getByRole('img').screenshot({ path: readable });
    const text = normalize(execFileSync(ocr, [readable], { encoding: 'utf8', timeout: 60_000 }));
    observations.push(`${frame}: ${text}`);
    // Deux noms réellement résolus par les buffers de combat, dans leur ordre.
    if (/Griknot's type became/i.test(text) && /the same as the wild Rattata's!/i.test(text)) {
      expect(text).not.toMatch(/prakaar|jaisaa|gayaa/i);
      expect(text.indexOf("Griknot's type became")).toBeLessThan(text.indexOf("the same as the wild Rattata's!"));
      found = data;
      break;
    }
  }
  console.log(`Sonde : ${temp}\n${observations.join('\n')}`);
  expect(found, `Le combat doit rendre la copie active EN hors lot : ${observations.join('\n')}`).toBeTruthy();
  await page.setContent(`<style>body{margin:0;background:#222;color:white;font:18px sans-serif}figure{margin:12px;width:max-content}img{width:960px;height:640px;image-rendering:pixelated}figcaption{padding:8px}</style><figure><figcaption>HI-01 — 0x028780 exclu : script historique supplanté<br>Reflect Type réel : copie active 0x96BE0C hors lot, anglais conservé</figcaption><img alt="Exclusion HI-01 vérifiée en combat natif" src="data:image/png;base64,${found}"></figure>`);
  await expect(page.getByRole('img')).toBeVisible();
  await page.getByRole('img').evaluate(img => (img as HTMLImageElement).decode());
  const proof = path.join(os.tmpdir(), 'f693-hi01-battle.png');
  await page.locator('figure').screenshot({ path: proof });
  console.log(`Preuve : ${proof}`);
});
