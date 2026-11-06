/** F-694 : rendu moteur du lot HI-02, via pointeurs vivants et cellule fixe. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const samples = [
  { id: 'centre', offset: '0x1a5483', pointer: 0x1a6588 },
  { id: 'cube', offset: '0x236632', pointer: 0x87b6d0 },
  { id: 'classe', offset: '0x23e58c', pointer: null },
] as const;

test('HI-02 rend le Centre, la description du Cube et la classe Sevak', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'hi02-surfaces-'));
  const source = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-indie.gba'));
  const audit: { entries: { offset: string; translation?: string; status: string }[] } =
    JSON.parse(fs.readFileSync(path.join(root, 'languages/indie/data/hi02_audit.json'), 'utf8'));

  for (const sample of samples) {
    const entry = audit.entries.find(candidate => candidate.offset === sample.offset);
    expect(entry?.status).toBe('translated');
    expect(entry?.translation).toBeTruthy();
    const target = sample.pointer === null ? Number(sample.offset) : source.readUInt32LE(sample.pointer) - 0x08000000;
    expect(target).toBeGreaterThan(0);
    expect(target).toBeLessThan(source.length);
    const expected = Buffer.from(execFileSync('python3', ['-c',
      'from src.core.text_codec import TextEncoder; import sys; sys.stdout.buffer.write(TextEncoder.encode_pokemon(sys.argv[1].replace("\\\\n", "\\n"), strict=True))',
      entry!.translation!], { cwd: root }));
    expect(source.subarray(target, target + expected.length)).toEqual(expected);

    // Seule cette copie temporaire reçoit des déclencheurs et changements de fixture.
    const rom = Buffer.from(source);
    const romPath = path.join(temp, `${sample.id}.gba`);
    fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, `${sample.id}.sav`));
    const scriptBase = rom.lastIndexOf(Buffer.alloc(128, 255));
    expect(scriptBase).toBeGreaterThan(0x1000000);
    let trigger = '';
    let screenshotFrame = 2320;
    if (sample.id === 'centre') {
      rom.set([0x0f, 0], scriptBase);
      rom.writeUInt32LE(target + 0x08000000, scriptBase + 2);
      rom.set([0x09, 6, 2], scriptBase + 6);
    } else if (sample.id === 'cube') {
      // La Repousse déjà dans le Cube affiche les champs réels de Safety Goggles.
      rom.copy(rom, 0x876074 + 95 * 44, sample.pointer - 20, sample.pointer - 6);
      rom.copy(rom, 0x876074 + 95 * 44 + 20, sample.pointer, sample.pointer + 4);
      trigger = `
 local keys={[2020]=3,[2070]=4,[2100]=4,[2130]=0}
 if keys[f] then emu:addKey(keys[f]) end
 if keys[f-4] then emu:clearKey(keys[f-4]) end`;
      screenshotFrame = 2450;
    } else {
      expect(expected.length).toBeLessThanOrEqual(13);
      expect(entry!.translation).toBe('Sevak');
      // Trainer 527, combat type 3 : seul son indice de classe change dans la copie.
      rom[0x23eac8 + 527 * 40 + 1] = (0x23e58c - 0x23e558) / 13;
      expect(rom[0x23eac8 + 527 * 40 + 1]).toBe(4);
      rom.set([0x5c, 3, 0x0f, 2, 0, 0], scriptBase);
      rom.writeUInt32LE(target + 0x08000000, scriptBase + 6);
      rom[scriptBase + 10] = 2;
      screenshotFrame = 2700;
    }
    if (sample.id !== 'cube') {
      trigger = `
 if f==2020 then
  assert(emu:read8(0x03000EA8)==2, 'Un script est déjà actif')
  emu:write8(0x03000EA8,0); emu:write8(0x03000EB1,1)
  emu:write32(0x03000EB8,${scriptBase + 0x08000000})
 end`;
    }
    fs.writeFileSync(romPath, rom);
    const capture = path.join(temp, `${sample.id}.png`);
    const lua = path.join(temp, `${sample.id}.lua`);
    fs.writeFileSync(lua, `
local f=0
callbacks:add('frame', function()
 f=f+1
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 ${trigger}
 if f==${screenshotFrame} then emu:screenshot(${JSON.stringify(capture)}) end
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
        return fs.existsSync(capture) && fs.readFileSync(capture).subarray(-12)
          .equals(Buffer.from('0000000049454e44ae426082', 'hex'));
      }, { timeout: 120_000 }).toBe(true);
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
request.recognitionLanguages = ["en-US"]
request.usesLanguageCorrection = false
try VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([request])
print((request.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\\n"))
`);
  const ocr = path.join(temp, 'ocr');
  execFileSync('swiftc', [swift, '-o', ocr], { timeout: 60_000 });
  const images = samples.map(sample => `<img alt="HI-02 ${sample.id}" src="data:image/png;base64,${fs.readFileSync(path.join(temp, `${sample.id}.png`)).toString('base64')}">`);
  await page.setContent(`<style>body{margin:0;background:#222}main{display:grid;grid-template-columns:repeat(2,720px);gap:8px;padding:8px;width:max-content}img{width:720px;height:480px;image-rendering:pixelated}</style><main>${images.join('')}</main>`);
  await expect(page.getByRole('img')).toHaveCount(3);
  await page.getByRole('img').evaluateAll(elements => Promise.all(elements.map(element => (element as HTMLImageElement).decode())));
  const texts: string[] = [];
  for (let index = 0; index < samples.length; index++) {
    const readable = path.join(temp, `${samples[index].id}-readable.png`);
    await page.getByRole('img').nth(index).screenshot({ path: readable });
    texts.push(execFileSync(ocr, [readable], { encoding: 'utf8', timeout: 60_000 }));
  }
  console.log(texts);
  expect(texts[0]).toMatch(/svaagat hai/i);
  expect(texts[0]).not.toMatch(/Welcome/i);
  expect(texts[1]).toMatch(/chashme mausam/i);
  expect(texts[1]).toMatch(/rakshaa karte hain/i);
  expect(texts[1]).not.toMatch(/weather-related|These goggles/i);
  expect(texts[2]).toMatch(/Sevak/);
  expect(texts[2]).not.toMatch(/Waiter/);
  const proof = path.join(os.tmpdir(), 'f694-hi02-surfaces.png');
  await page.locator('main').screenshot({ path: proof });
  console.log(`Preuve : ${proof}`);
});
