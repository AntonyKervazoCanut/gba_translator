/** HI-01 : sondes du moteur natif, textes livrés lus par leurs pointeurs vivants. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const normalize = (text: string): string => text.normalize('NFD').replace(/\p{M}/gu, '')
  .replace(/[.,!?]/g, '').replace(/\s+/g, ' ').trim().toLowerCase();

function lastWins(): Map<number, string> {
  const result = new Map<number, string>();
  for (const line of fs.readFileSync(path.join(root, 'languages/indie/combined_indie.txt'), 'utf8').split(/\r?\n/)) {
    const match = /^(0x[0-9a-f]+):\s*(.*)$/i.exec(line);
    if (match) result.set(Number(match[1]), match[2]);
  }
  return result;
}

test('HI-01 : les répliques et la question PC sont lisibles, sans fallback ni débordement', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'hi01-native-'));
  const original = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-indie.gba'));
  const translations = lastWins();
  // trainerbattle défaite/introduction et loadpointer de la question PC.
  // Ces sondes valident le moteur de boîte de dialogue, pas un parcours de quête.
  const scenes = [
    { offset: 0x1835a0, site: 0x1a93d3, label: 'Réplique de défaite' },
    { offset: 0x183560, site: 0x1a93cf, label: 'Dialogue, première page' },
    { offset: 0x1a508a, site: 0x1a6999, label: 'Question PC' },
  ];
  const save = fs.readFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'));
  fs.writeFileSync(path.join(temp, 'ocr.swift'), `import Foundation
import Vision
let r = VNRecognizeTextRequest()
r.recognitionLevel = .accurate
r.recognitionLanguages = ["en-US"]
r.usesLanguageCorrection = false
r.regionOfInterest = CGRect(x: 0.05, y: 0.025, width: 0.90, height: 0.26)
try VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([r])
print((r.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\\n"))
`);
  const ocr = path.join(temp, 'ocr');
  execFileSync('swiftc', [path.join(temp, 'ocr.swift'), '-o', ocr], { timeout: 60_000 });
  const pictures: string[] = [];
  for (const [n, scene] of scenes.entries()) {
    const translation = translations.get(scene.offset);
    expect(translation, `Traduction requise à ${scene.offset.toString(16)}`).toBeTruthy();
    const expected = execFileSync('python3', ['-c',
      'from src.core.text_codec import TextEncoder; import sys; sys.stdout.buffer.write(TextEncoder.encode_pokemon(sys.argv[1].replace(chr(92)+"n", chr(10)), strict=True))',
      translation!], { cwd: root });
    const rom = Buffer.from(original);
    const target = rom.readUInt32LE(scene.site) - 0x08000000;
    expect(target).toBeGreaterThan(0);
    expect(target).toBeLessThan(rom.length);
    expect(rom.subarray(target, target + expected.length), 'Texte réellement livré au pointeur').toEqual(expected);
    const lines = translation!.split('<0xFB>')[0].split('\\n');
    expect(lines.length).toBeLessThanOrEqual(2);
    const widths = rom.readUInt32LE(0x6594) - 0x08000000;
    for (const line of lines) {
      const encoded = execFileSync('python3', ['-c',
        'from src.core.text_codec import TextEncoder; import sys; sys.stdout.buffer.write(TextEncoder.encode_pokemon(sys.argv[1], strict=True))', line], { cwd: root });
      const advance = [...encoded.subarray(0, -1)].reduce((total, byte) => total + rom[widths + byte], 0);
      expect(advance, line).toBeLessThanOrEqual(192);
    }
    const script = rom.lastIndexOf(Buffer.alloc(128, 255));
    expect(script).toBeGreaterThan(0x1000000);
    // Seul un déclencheur privé est ajouté ; aucune réécriture du texte testé.
    rom.set([0x0f, 0], script);
    rom.writeUInt32LE(target + 0x08000000, script + 2);
    rom.set([0x09, 6, 2], script + 6);
    fs.writeFileSync(path.join(temp, 'game.gba'), rom);
    fs.writeFileSync(path.join(temp, 'game.sav'), save);
    const lua = path.join(temp, `scene${n}.lua`);
    const done = path.join(temp, `scene${n}.done`);
    const status = path.join(temp, `scene${n}.status`);
    const shot = path.join(temp, `scene${n}.png`);
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
  emu:write32(0x03000EB8,${0x08000000 + script})
 end
 if f==2450 then emu:screenshot(${JSON.stringify(shot)}) end
 if f==2500 then local d=io.open(${JSON.stringify(done)},'w'); d:write('ok'); d:close() end
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
    child.stdout?.on('data', data => { diagnostics += data.toString(); });
    child.stderr?.on('data', data => { diagnostics += data.toString(); });
    child.on('error', error => { launchError = error; });
    try {
      await expect.poll(() => {
        if (launchError) throw launchError;
        if (child.exitCode !== null) throw new Error(`mGBA terminé : ${child.exitCode}; ${diagnostics}`);
        if (fs.existsSync(status) && fs.readFileSync(status, 'utf8') !== '2') {
          throw new Error(`Script actif avant sonde : ${fs.readFileSync(status, 'utf8')}; ${temp}`);
        }
        return fs.existsSync(done);
      }, { timeout: 90_000 }).toBe(true);
    } finally {
      child.kill('SIGTERM');
      await new Promise<void>(resolve => {
        if (child.exitCode !== null || child.signalCode !== null || launchError) resolve();
        else child.once('exit', () => resolve());
      });
    }
    expect(fs.readFileSync(path.join(temp, 'game.sav')), 'La sauvegarde ne doit pas être modifiée').toEqual(save);
    const picture = `<figure><figcaption>HI-01 — 0x${scene.offset.toString(16)} — ${scene.label}</figcaption><img alt="${scene.label}" src="data:image/png;base64,${fs.readFileSync(shot).toString('base64')}"></figure>`;
    await page.setContent(`<style>img{width:1440px;height:960px;image-rendering:pixelated}</style>${picture}`);
    await page.getByRole('img').evaluate(img => (img as HTMLImageElement).decode());
    const large = path.join(temp, `large${n}.png`);
    await page.getByRole('img').screenshot({ path: large });
    const text = normalize(execFileSync(ocr, [large], { encoding: 'utf8', timeout: 60_000 }));
    console.log(`0x${scene.offset.toString(16)} : ${text}`);
    for (const line of lines) expect(text, `Ligne entière attendue : ${line}`).toContain(normalize(line));
    pictures.push(picture);
  }
  await page.setContent(`<style>body{margin:0;background:#222;color:white;font:18px sans-serif}main{display:grid;grid-template-columns:repeat(2,720px);gap:8px;padding:8px;width:max-content}figure{margin:0}img{width:720px;height:480px;image-rendering:pixelated}</style><main>${pictures.join('')}</main>`);
  await expect(page.getByRole('img')).toHaveCount(scenes.length);
  await page.getByRole('img').evaluateAll(images => Promise.all(images.map(img => (img as HTMLImageElement).decode())));
  const proof = process.env.HI01_PROOF ?? path.join(os.tmpdir(), 'f693-hi01-proof.png');
  await page.locator('main').screenshot({ path: proof });
  console.log(`Preuve : ${proof} ; sondes : ${temp}`);
});
