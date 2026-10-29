/** B-1026 : lookup réel de 122 objets, rendu mGBA et OCR sans fenêtre visible. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

test('122 noms accessibles par bufferitemname et exemples rendus en allemand', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'b1026-items-'));
  const rom = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-de.gba'));
  const manifest = JSON.parse(fs.readFileSync(path.join(root, 'languages/de/data/item_names_objets_01.json'), 'utf8')) as { entries: { offset: string }[] };
  const offsets = manifest.entries.map(e => Number(e.offset));
  expect(offsets).toHaveLength(122);
  expect(rom.readUInt32LE(0x9A8D8)).toBe(0x08876200);
  const base = rom.lastIndexOf(Buffer.alloc(4096, 255));
  expect(base).toBeGreaterThan(0x1000000);
  // Opcode natif bufferitemname : chaque ID est résolu par le moteur.
  offsets.forEach((offset, n) => {
    const id = (offset - 0x876200) / 44;
    rom.set([0x80, 0, id & 255, id >> 8, 2], base + n * 8);
  });
  const pairs = [
    [0x876258, 0x878510], [0x876938, 0x876F10],
    [0x878904, 0x8792FC], [0x879170, 0x87919C],
    [0x8791C8, 0x879278], [0x87714C, 0x8771A4],
  ];
  const names = [
    ['Hyperball', 'Granitstein'], ['Schwarz.Flöte', 'X-Abwehr'],
    ['Schwächensch.', 'Lager-Schl.'], ['Roter Edlst.', 'Blauer Edlst.'],
    ['Werte-Scanner', 'Codekarte: 2'], ['Traumnebel', 'Tauschstein'],
  ];
  const template = base + 3000;
  rom.set([0xFD, 2, 0xFE, 0xFD, 3, 0xFF], template);
  pairs.forEach((pair, n) => {
    const at = base + 1100 + n * 24;
    pair.forEach((offset, buffer) => {
      const id = (offset - 0x876200) / 44;
      rom.set([0x80, buffer, id & 255, id >> 8], at + buffer * 4);
    });
    rom.set([0x0F, 0], at + 8);
    rom.writeUInt32LE(template + 0x08000000, at + 10);
    rom.set([0x09, 6, 2], at + 14);
  });
  fs.writeFileSync(path.join(temp, 'game.gba'), rom);
  fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
  const lua = path.join(temp, 'probe.lua');
  fs.writeFileSync(lua, `
local f=0
local function start(script)
 assert(emu:read8(0x03000EA8)==2, 'Script actif')
 emu:write8(0x03000EA8,0); emu:write8(0x03000EB1,1)
 emu:write32(0x03000EB8,script)
end
callbacks:add('frame', function()
 f=f+1
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 for n=0,121 do
  if f==2020+n*15 then start(${base + 0x08000000}+n*8) end
  if f==2030+n*15 then
   local out=assert(io.open(${JSON.stringify(temp)}..'/lookup'..n..'.bin','wb'))
   for i=0,13 do out:write(string.char(emu:read8(0x02021CD0+i))) end
   out:close()
  end
 end
 if f==3900 then emu:saveStateFile(${JSON.stringify(path.join(temp, 'ready.ss'))}) end
 for n=0,5 do
  if f==4000+n*600 then emu:loadStateFile(${JSON.stringify(path.join(temp, 'ready.ss'))}) end
  if f==4010+n*600 then start(${base + 0x08000000 + 1100}+n*24) end
  if f==4400+n*600 then emu:screenshot(${JSON.stringify(temp)}..'/page'..n..'.png') end
 end
end)
`);
  const child = spawn(process.env.MGBA_PATH ?? '/opt/homebrew/opt/mgba/bin/mGBA', [
    '-C', 'mute=1', '-C', 'videoDriver=1', '-C', 'fpsTarget=240',
    '-C', 'audioSync=0', '-C', 'videoSync=0',
    ...['savegamePath', 'savestatePath', 'screenshotPath', 'cheatsPath'].flatMap(key => ['-C', `${key}=${temp}`]),
    '--script', lua, path.join(temp, 'game.gba'),
  ], { env: { ...process.env, QT_QPA_PLATFORM: 'offscreen' }, stdio: ['ignore', fs.openSync(path.join(temp, 'mgba.log'), 'w'), 'ignore'] });
  let launchError: Error | undefined;
  child.on('error', error => { launchError = error; });
  try {
    await expect.poll(() => {
      if (launchError) throw launchError;
      if (child.exitCode !== null) throw new Error(`mGBA terminé : ${child.exitCode}`);
      return fs.existsSync(path.join(temp, 'page5.png'));
    }, { timeout: 120_000 }).toBe(true);
    child.kill('SIGTERM');
    await new Promise<void>(resolve => child.once('exit', () => resolve()));
    offsets.forEach((offset, n) => {
      const actual = fs.readFileSync(path.join(temp, `lookup${n}.bin`));
      const length = rom.indexOf(255, offset) - offset + 1;
      expect(actual.subarray(0, length), `lookup ${offset.toString(16)}`).toEqual(rom.subarray(offset, offset + length));
    });
    const swift = path.join(temp, 'ocr.swift');
    fs.writeFileSync(swift, `
import Foundation
import Vision
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.recognitionLanguages = ["de-DE", "en-US"]
request.usesLanguageCorrection = false
try VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([request])
print((request.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\\n"))
`);
    const ocr = path.join(temp, 'ocr');
    execFileSync('swiftc', [swift, '-o', ocr], { timeout: 60_000 });
    const pictures = pairs.map((_, n) => `<img alt="Objets ${n + 1}" src="data:image/png;base64,${fs.readFileSync(path.join(temp, `page${n}.png`)).toString('base64')}">`);
    await page.setContent(`<style>body{margin:0;background:#222}main{display:grid;grid-template-columns:repeat(3,720px);gap:8px;padding:8px;width:max-content}img{width:720px;height:480px;image-rendering:pixelated}</style><main>${pictures.join('')}</main>`);
    await expect(page.getByRole('img')).toHaveCount(6);
    for (let n = 0; n < pairs.length; n++) {
      const readable = path.join(temp, `readable${n}.png`);
      await page.getByRole('img').nth(n).screenshot({ path: readable });
      const text = execFileSync(ocr, [readable], { encoding: 'utf8', timeout: 60_000 });
      console.log(n, text);
      for (const name of names[n]) expect(text).toContain(name);
      expect(text).not.toMatch(/Hard Stone|Harter Stein|Ultra Ball|Dream Mist/);
    }
    const proof = path.join(os.tmpdir(), 'b1026-item-names-proof.png');
    await page.locator('main').screenshot({ path: proof });
    console.log(`Preuve : ${proof}`);
  } finally {
    child.kill('SIGTERM');
    await new Promise<void>(resolve => {
      if (child.exitCode !== null || child.signalCode !== null || launchError) resolve();
      else child.once('exit', () => resolve());
    });
  }
});
