/** F-783 : textes PT-24 affichés par le moteur via leurs pointeurs vivants.
 * Une copie temporaire reçoit uniquement un script msgbox. Aucun texte ni glyphe
 * n'est injecté et aucune sauvegarde n'est effectuée. Ce sont des sondes de rendu,
 * pas une validation des parcours réseau ni de la sauvegarde native.
 */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PNG } from 'pngjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const normalize = (text: string): string => text.normalize('NFD').replace(/\p{M}/gu, '').replace(/\s+/g, ' ').trim();

test('PT-24 : dialogues Borrius et tildes lisibles', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'pt24-system-'));
  const original = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-pt.gba'));
  const values = new Map<number, string>();
  for (const line of fs.readFileSync(path.join(root, 'languages/pt/combined_pt.txt'), 'utf8').split('\n')) {
    const match = line.match(/^0x([\da-f]+): (.*)$/i);
    if (match) values.set(parseInt(match[1], 16), match[2]);
  }
  const scenes = [
    { offset: 0x7b659a, site: 0x78bfdc, title: 'PT-24 - barriere electrique',
      matches: [/A barreira eletrica foi/i, /desativada/i], forbidden: /electric barrier|disengaged/ },
    { offset: 0x7bb1b2, site: 0x7bb129, title: 'PT-24 - campeur de Thundercap',
      matches: [/Eu nao estou perdido/i, /Estou acampando/i, /Essa e a verdade/i], forbidden: /not lost|camping|my story/ },
  ];
  for (const [n, scene] of scenes.entries()) {
    const value = values.get(scene.offset);
    expect(value, `Traduction absente à ${scene.offset.toString(16)}`).toBeTruthy();
    const expected = execFileSync('python3', ['-c',
      'from src.core.text_codec import TextEncoder; import sys; sys.stdout.buffer.write(TextEncoder.encode_pokemon(sys.argv[1].replace(r"\\n", "\\n"), strict=True))', value!], { cwd: root });
    const target = original.readUInt32LE(scene.site) - 0x08000000;
    expect(target).toBeGreaterThan(0);
    expect(target + expected.length).toBeLessThanOrEqual(original.length);
    expect(original.subarray(target, target + expected.length)).toEqual(expected);

    const rom = Buffer.from(original);
    const script = rom.lastIndexOf(Buffer.alloc(128, 255));
    expect(script).toBeGreaterThan(0x1000000);
    rom.set([0x0f, 0], script);
    rom.writeUInt32LE(original.readUInt32LE(scene.site), script + 2);
    rom.set([0x09, 6, 2], script + 6);
    const directory = path.join(temp, `scene-${n}`);
    fs.mkdirSync(directory);
    const game = path.join(directory, 'game.gba');
    fs.writeFileSync(game, rom);
    const save = path.join(directory, 'game.sav');
    const saveBytes = fs.readFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'));
    fs.writeFileSync(save, saveBytes);
    const capture = path.join(temp, `scene-${n}.png`);
    const lua = path.join(directory, 'probe.lua');
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
 if f==2600 then emu:screenshot(${JSON.stringify(capture)}) end
end)
`);
    const child = spawn(process.env.MGBA_PATH ?? '/opt/homebrew/opt/mgba/bin/mGBA', [
      '-C', 'mute=1', '-C', 'videoDriver=1', '-C', 'fpsTarget=240',
      '-C', 'audioSync=0', '-C', 'videoSync=0',
      ...['savegamePath', 'savestatePath', 'screenshotPath', 'cheatsPath'].flatMap(key => ['-C', `${key}=${directory}`]),
      '--script', lua, game,
    ], { env: { ...process.env, QT_QPA_PLATFORM: 'offscreen' }, stdio: 'ignore' });
    let launchError: Error | undefined;
    child.on('error', error => { launchError = error; });
    try {
      await expect.poll(() => {
        if (launchError) throw launchError;
        if (child.exitCode !== null) throw new Error(`mGBA terminé : ${child.exitCode}`);
        return fs.existsSync(capture) && fs.readFileSync(capture).subarray(-12).equals(Buffer.from('0000000049454e44ae426082', 'hex'));
      }, { timeout: 90_000 }).toBe(true);
    } finally {
      child.kill('SIGTERM');
      await new Promise<void>(resolve => {
        if (child.exitCode !== null || child.signalCode !== null || launchError) resolve();
        else child.once('exit', () => resolve());
      });
    }
    expect(fs.readFileSync(save)).toEqual(saveBytes);
    const png = PNG.sync.read(fs.readFileSync(capture));
    expect([png.width, png.height]).toEqual([240, 160]);
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
  const images = scenes.map((scene, n) => `<figure><figcaption>${scene.title}</figcaption><img alt="${scene.title}" src="data:image/png;base64,${fs.readFileSync(path.join(temp, `scene-${n}.png`)).toString('base64')}"></figure>`);
  await page.setContent(`<style>body{margin:0;background:#222;color:white;font:18px sans-serif}main{display:flex;gap:8px;padding:8px;width:max-content}figure{margin:0}img{width:960px;height:640px;image-rendering:pixelated}figcaption{padding:8px}</style><main>${images.join('')}</main>`);
  await expect(page.getByRole('img')).toHaveCount(scenes.length);
  await page.getByRole('img').evaluateAll(images => Promise.all(images.map(image => (image as HTMLImageElement).decode())));
  for (let n = 0; n < scenes.length; n++) {
    const readable = path.join(temp, `readable-${n}.png`);
    await page.getByRole('img').nth(n).screenshot({ path: readable });
    const text = normalize(execFileSync(ocr, [readable], { encoding: 'utf8', timeout: 60_000 }));
    console.log(`${scenes[n].title}: ${text}`);
    for (const expected of scenes[n].matches) expect(text).toMatch(expected);
    expect(text).not.toMatch(scenes[n].forbidden);
  }
  const proof = path.join(os.tmpdir(), 'f783-pt24-proof.png');
  await page.locator('main').screenshot({ path: proof });
  console.log(`Preuve : ${proof} ; captures réelles : ${temp}`);
});
