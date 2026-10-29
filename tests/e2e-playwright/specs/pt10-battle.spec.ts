/** PT-10 : vrai combat et hausse de statistique ; météo livrée via msgbox.
 * Le combat utilise les buffers FD du moteur, sans injecter de texte en RAM.
 * La copie temporaire ajoute le script de lancement et garantit la précision
 * et l'effet secondaire de Metal Claw, sans modifier les textes ni les buffers.
 */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const normalize = (text: string): string => text.normalize('NFD').replace(/\p{M}/gu, '').replace(/\s+/g, ' ').trim();

test('PT-10 : attaque et hausse de statistique natives, météo au pointeur vivant', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'pt10-battle-'));
  const original = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-pt.gba'));
  const values = new Map<number, string>();
  for (const line of fs.readFileSync(path.join(root, 'languages/pt/combined_pt.txt'), 'utf8').split('\n')) {
    const match = line.match(/^0x([\da-f]+): (.*)$/i);
    if (match) values.set(parseInt(match[1], 16), match[2]);
  }
  // Chaque chaîne vérifiée est prise au consommateur vivant, jamais par recherche
  // d'une copie morte. Les tests Python contrôlent tous les autres consommateurs.
  for (const [offset, site] of [[0x3fd57b, 0x9be13c], [0x3fcb5f, 0x3fe260],
    [0x3fcb4a, 0x42d9c], [0x3fd593, 0x1fb2340], [0x3fd850, 0x3fe34c]]) {
    const value = values.get(offset);
    expect(value, `Traduction absente à ${offset.toString(16)}`).toBeTruthy();
    const expected = execFileSync('python3', ['-c',
      'from src.core.text_codec import TextEncoder; import sys; sys.stdout.buffer.write(TextEncoder.encode_pokemon(sys.argv[1].replace(r"\\n", "\\n"), strict=True))', value!], { cwd: root });
    const target = original.readUInt32LE(site) - 0x08000000;
    expect(target).toBeGreaterThan(0);
    expect(target + expected.length).toBeLessThanOrEqual(original.length);
    expect(original.subarray(target, target + expected.length)).toEqual(expected);
  }

  for (const mode of ['battle', 'weather']) {
    const rom = Buffer.from(original);
    const script = rom.lastIndexOf(Buffer.alloc(128, 255));
    expect(script).toBeGreaterThan(0x1000000);
    if (mode === 'battle') {
      // La hausse native a normalement 10 % de chance : les autres traductions
      // changent les durées d'affichage et donc la suite RNG. Garantir uniquement
      // les deux probabilités rend le scénario indépendant de cette durée.
      // 0x1cc contient le pointeur de la table CFRU, également consommée par le
      // moteur ; Metal Claw est le mouvement 232, struct BattleMove de 12 octets.
      const moves = rom.readUInt32LE(0x1cc) - 0x08000000;
      const metalClaw = moves + 232 * 12;
      expect(rom.subarray(metalClaw, metalClaw + 12)).toEqual(Buffer.from('8b32085f230a000013640000', 'hex'));
      rom[metalClaw + 3] = 100; // Précision (95 % dans la ROM livrée).
      rom[metalClaw + 5] = 100; // Hausse d'Attaque (10 % dans la ROM livrée).
      // setwildbattle Rattata, niveau 5, aucun objet ; dowildbattle ; end.
      rom.set([0xb6, 19, 0, 5, 0, 0, 0xb7, 2], script);
    } else {
      rom.set([0x0f, 0], script);
      rom.writeUInt32LE(rom.readUInt32LE(0x3fe34c), script + 2);
      rom.set([0x09, 6, 2], script + 6);
    }
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
 if ${mode === 'battle'} then
  if f>=2500 and f<=3200 and f%150==100 then emu:addKey(0) end
  if f>=2504 and f<=3204 and f%150==104 then emu:clearKey(0) end
  if f==3050 or f==3150 or f==3250 or (f>=3400 and f<=3525 and f%25==0) then
   emu:screenshot(${JSON.stringify(temp)}..'/battle-'..f..'.png')
  end
 else
  if f==2450 then emu:screenshot(${JSON.stringify(path.join(temp, 'weather.png'))}) end
 end
 if f==3550 then local done=io.open(${JSON.stringify(path.join(temp, `${mode}.done`))},'w'); done:write('ok'); done:close() end
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
        return fs.existsSync(path.join(temp, `${mode}.done`));
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
  const scenes = [
    { title: 'Combat réel — mouvement', files: [3050, 3150, 3250].map(n => `battle-${n}.png`), matches: [/Griknot usou/i, /Metal Claw/i], forbidden: /Griknot used/ },
    { title: 'Combat réel — hausse de statistique', files: [3400, 3425, 3450, 3475, 3500, 3525].map(n => `battle-${n}.png`), matches: [/Griknot.*Ataque/i, /aumentou\s*!/i], forbidden: /Attack rose/ },
    { title: 'Météo — msgbox au pointeur vivant', files: ['weather.png'], matches: [/Esta chovendo\./i], forbidden: /It is raining/ },
  ];
  const verified: string[] = [];
  for (const scene of scenes) {
    let found: string | undefined;
    const observed: string[] = [];
    for (const file of scene.files) {
      const data = fs.readFileSync(path.join(temp, file)).toString('base64');
      await page.setContent(`<style>body{margin:0}img{width:960px;height:640px;image-rendering:pixelated}</style><img alt="${scene.title}" src="data:image/png;base64,${data}">`);
      await page.getByRole('img').evaluate(image => (image as HTMLImageElement).decode());
      const readable = path.join(temp, 'readable.png');
      await page.getByRole('img').screenshot({ path: readable });
      const text = normalize(execFileSync(ocr, [readable], { encoding: 'utf8', timeout: 60_000 }));
      observed.push(`${file}: ${text}`);
      if (scene.matches.every(pattern => pattern.test(text))) {
        expect(text).not.toMatch(scene.forbidden);
        found = data;
        break;
      }
    }
    console.log(observed.join('\n'));
    expect(found, `${scene.title}: ${observed.join('\n')}`).toBeTruthy();
    verified.push(`<figure><figcaption>${scene.title}</figcaption><img alt="${scene.title}" src="data:image/png;base64,${found}"></figure>`);
  }
  await page.setContent(`<style>body{margin:0;background:#222;color:white;font:18px sans-serif}main{display:flex;gap:8px;padding:8px;width:max-content}figure{margin:0}img{width:720px;height:480px;image-rendering:pixelated}</style><main>${verified.join('')}</main>`);
  await expect(page.getByRole('img')).toHaveCount(3);
  await page.getByRole('img').evaluateAll(images => Promise.all(images.map(image => (image as HTMLImageElement).decode())));
  const proof = path.join(os.tmpdir(), 'f769-pt10-proof.png');
  await page.locator('main').screenshot({ path: proof });
  console.log(`Preuve : ${proof}`);
});
