/** F-768 : mots livrés et template de combat, sondes mGBA hors écran. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

test('PT-09 : mots et message de combat rendu avec un nom long', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'pt09-'));
  const original = fs.readFileSync(path.join(root, 'output/roms/GenedRom-pt.gba'));
  const scenes = [
    { site: 0x3ec560, mode: 'message', matches: [/EXPECTATIVA/] },
    { site: 0x3ecbbc, mode: 'message', matches: [/Cancelar/i] },
    { site: 0x3f1cb0, mode: 'message', matches: [/Bellin Town/i] },
    { site: 0x3fe010, mode: 'battle-template', matches: [/Foe CHARMANDER/i, /confuso/i] },
  ];
  for (let n = 0; n < scenes.length; n++) {
    const scene = scenes[n];
    const rom = Buffer.from(original);
    const target = rom.readUInt32LE(scene.site) - 0x08000000;
    expect(target).toBeGreaterThan(0);
    expect(target).toBeLessThan(rom.length);
    const expected = rom.subarray(target, rom.indexOf(255, target) + 1);
    expect(expected.length).toBeGreaterThan(5);
    const script = rom.lastIndexOf(Buffer.alloc(128, 255));
    expect(script).toBeGreaterThan(0x1000000);
    // Les mots et lieux sont lus à leur pointeur vivant sans modifier le texte.
    // Pour le template combat, résoudre FD0F en nom représentatif dans une
    // copie temporaire permet au moteur msgbox de rendre la phrase livrée.
    // Cette scène est une sonde typographique, pas une bataille jouée.
    let renderTarget = target;
    if (scene.mode === 'battle-template') {
      expect(expected.subarray(0, 2)).toEqual(Buffer.from([0xfd, 0x0f]));
      const name = Buffer.from(execFileSync('python3', ['-c',
        'from src.core.text_codec import TextEncoder; import sys; sys.stdout.buffer.write(TextEncoder.encode_pokemon("Foe CHARMANDER"))'], { cwd: root }));
      renderTarget = script + 32;
      rom.set(Buffer.concat([name.subarray(0, -1), expected.subarray(2)]), renderTarget);
    }
    rom.set([0x0f, 0], script);
    rom.writeUInt32LE(renderTarget + 0x08000000, script + 2);
    rom.set([0x09, 6, 2], script + 6);
    const romPath = path.join(temp, 'game.gba');
    fs.writeFileSync(romPath, rom);
    fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
    const lua = path.join(temp, 'probe.lua');
    fs.writeFileSync(lua, `
local f=0
callbacks:add('frame', function()
 f=f+1
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 if f==2020 then
  assert(emu:read8(0x03000EA8)==2, 'Script actif')
  emu:write8(0x03000EA8,0); emu:write8(0x03000EB1,1)
  emu:write32(0x03000EB8,${script + 0x08000000})
 end
 if f==2450 then emu:screenshot(${JSON.stringify(path.join(temp, `scene${n}.png`))}) end
end)
`);
    const child = spawn(process.env.MGBA_PATH ?? '/opt/homebrew/opt/mgba/bin/mGBA', [
      '-C', 'mute=1', '-C', 'videoDriver=1', '-C', 'fpsTarget=240',
      '-C', 'audioSync=0', '-C', 'videoSync=0',
      ...['savegamePath', 'savestatePath', 'screenshotPath', 'cheatsPath'].flatMap(key => ['-C', `${key}=${temp}`]),
      '--script', lua, romPath,
    ], { env: { ...process.env, QT_QPA_PLATFORM: 'offscreen' }, stdio: 'ignore' });
    let launchError: Error | undefined;
    child.on('error', error => { launchError = error; });
    try {
      await expect.poll(() => {
        if (launchError) throw launchError;
        if (child.exitCode !== null) throw new Error(`mGBA terminé : ${child.exitCode}`);
        const file = path.join(temp, `scene${n}.png`);
        return fs.existsSync(file) && fs.readFileSync(file).subarray(-12).equals(Buffer.from('0000000049454e44ae426082', 'hex'));
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
  const images = scenes.map((_, n) => `<figure><figcaption>PT-09 — ${n === 3 ? 'Template combat, nom représentatif' : n === 2 ? 'Nom propre conservé' : 'Mot de phrase facile'}</figcaption><img alt="Sonde PT-09 ${n}" src="data:image/png;base64,${fs.readFileSync(path.join(temp, `scene${n}.png`)).toString('base64')}"></figure>`);
  await page.setContent(`<style>body{margin:0;background:#222;color:white;font:18px sans-serif}main{display:grid;grid-template-columns:repeat(2,720px);gap:8px;padding:8px;width:max-content}figure{margin:0}img{width:720px;height:480px;image-rendering:pixelated}</style><main>${images.join('')}</main>`);
  await expect(page.getByRole('img')).toHaveCount(4);
  await page.getByRole('img').evaluateAll(images => Promise.all(images.map(image => (image as HTMLImageElement).decode())));
  for (let n = 0; n < scenes.length; n++) {
    const readable = path.join(temp, `readable${n}.png`);
    await page.getByRole('img').nth(n).screenshot({ path: readable });
    const text = execFileSync(ocr, [readable], { encoding: 'utf8', timeout: 60_000 });
    console.log(n, text);
    // L'OCR peut insérer des ruptures ; les octets exacts sont vérifiés en ROM.
    const normalized = text.normalize('NFD').replace(/\p{M}/gu, '').replace(/\s+/g, ' ');
    for (const expected of scenes[n].matches) expect(normalized).toMatch(expected);
    expect(text).not.toMatch(/ANTICIPATION|confused|Cancel$/);
  }
  const proof = path.join(os.tmpdir(), 'f768-pt09-proof.png');
  await page.locator('main').screenshot({ path: proof });
  console.log(`Preuve : ${proof}`);
});
