/** PT-25 : sonde msgbox native de deux dialogues livrés.
 * Les pointeurs et les textes viennent de la ROM finale. Aucun texte, glyphe
 * ni template de fenêtre n'est modifié. La sonde contrôle les deux premières
 * lignes ; toutes les pages complètes sont vérifiées en binaire. Elle ne revendique pas
 * une navigation dans les 272 textes actifs.
 */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const normalize = (s: string): string => s.normalize('NFD').replace(/\p{M}/gu, '').replace(/\s+/g, ' ').trim().toLowerCase();

test('PT-25 : deux dialogues aux pointeurs vivants sont lisibles dans mGBA', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'pt25-borrius-'));
  const rom = fs.readFileSync(path.join(root, 'output/roms/GenedRom-pt.gba'));
  const audit = JSON.parse(fs.readFileSync(path.join(root, 'languages/pt/data/pt25_audit.json'), 'utf8'));
  const cases = ['0x7c060e', '0x7c6731'].map(offset => audit.entries.find((row: { offset: string }) => row.offset === offset));
  const script = rom.lastIndexOf(Buffer.alloc(128, 255));
  expect(script).toBeGreaterThan(0x1000000);
  for (let n = 0; n < cases.length; n++) {
    const row = cases[n];
    const pointer = rom.readUInt32LE(row.references[0]);
    const expected = execFileSync('python3', ['-c',
      'from src.core.text_codec import TextEncoder; import sys; sys.stdout.buffer.write(TextEncoder.encode_pokemon(sys.argv[1].replace(r"\\n", "\\n"), strict=True))',
      row.portuguese], { cwd: root });
    expect(rom.subarray(pointer - 0x08000000, pointer - 0x08000000 + expected.length)).toEqual(expected);
    rom.set([0x0f, 0], script + n * 16);
    rom.writeUInt32LE(pointer, script + n * 16 + 2);
    rom.set([0x09, 6, 2], script + n * 16 + 6);
  }
  fs.writeFileSync(path.join(temp, 'game.gba'), rom);
  fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
  fs.writeFileSync(path.join(temp, 'ocr.swift'), `import Foundation
import Vision
let r = VNRecognizeTextRequest()
r.recognitionLevel = .accurate
r.recognitionLanguages = ["pt-BR", "en-US"]
r.usesLanguageCorrection = true
try VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([r])
print((r.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\\n"))
`);
  const ocr = path.join(temp, 'ocr');
  execFileSync('swiftc', [path.join(temp, 'ocr.swift'), '-o', ocr]);
  const pictures: string[] = [];
  // Une sonde Lua privée, sans port réseau ni arrêt d'un autre émulateur.
  for (let n = 0; n < cases.length; n++) {
    const lua = path.join(temp, `scene${n}.lua`);
    const done = path.join(temp, `scene${n}.done`);
    fs.writeFileSync(lua, `
local f=0
callbacks:add('frame', function()
 f=f+1
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 if f==2020 then
  assert(emu:read8(0x03000EA8)==2, 'Script actif avant sonde')
  emu:write8(0x03000EA8,0); emu:write8(0x03000EB1,1)
  emu:write32(0x03000EB8,${0x08000000 + script + n * 16})
 end
 if f==2450 then emu:screenshot(${JSON.stringify(path.join(temp, `scene${n}.png`))}) end
 if f==2500 then local d=io.open(${JSON.stringify(done)},'w'); d:write('ok'); d:close() end
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
        return fs.existsSync(done);
      }, { timeout: 90_000 }).toBe(true);
    } finally {
      child.kill('SIGTERM');
      await new Promise<void>(resolve => {
        if (child.exitCode !== null || child.signalCode !== null || launchError) resolve();
        else child.once('exit', () => resolve());
      });
    }
    const shot = path.join(temp, `scene${n}.png`);
    const src = `data:image/png;base64,${fs.readFileSync(shot).toString('base64')}`;
    const picture = `<figure><figcaption>${cases[n].offset} — sonde native (lignes 1 et 2)</figcaption><img alt="${cases[n].offset}" src="${src}"></figure>`;
    await page.setContent(`<style>img{width:960px;height:640px;image-rendering:pixelated}</style>${picture}`);
    await page.getByRole('img').evaluate(img => (img as HTMLImageElement).decode());
    const large = path.join(temp, 'large.png');
    await page.getByRole('img').screenshot({ path: large });
    const text = normalize(execFileSync(ocr, [large], { encoding: 'utf8' }));
    pictures.push(picture);
    console.log(cases[n].offset, text);
    for (const line of cases[n].portuguese.split('<0xFB>')[0].split('\\n').slice(0, 2)) {
      expect(text, line).toContain(normalize(line));
    }
    expect(text).not.toMatch(/you can't|right now|trash can|empty|Desole/i);
  }
  await page.setContent(`<style>body{margin:0;background:#222;color:white;font:18px sans-serif}main{display:grid;grid-template-columns:repeat(2,720px);gap:8px;padding:8px;width:max-content}figure{margin:0}img{width:720px;height:480px;image-rendering:pixelated}</style><main>${pictures.join('')}</main>`);
  await expect(page.getByRole('img')).toHaveCount(2);
  await page.getByRole('img').evaluateAll(images => Promise.all(images.map(img => (img as HTMLImageElement).decode())));
  const proof = path.join(os.tmpdir(), 'f784-pt25-proof.png');
  await page.locator('main').screenshot({ path: proof });
  console.log(`Preuve : ${proof}`);
});
