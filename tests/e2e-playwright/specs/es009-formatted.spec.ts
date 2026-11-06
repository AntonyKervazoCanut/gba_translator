/** F-1040 : colonnes FC13/FC06 et expansion F7, impression native hors écran.
 * Les sondes sont temporaires ; aucune traduction ni sauvegarde n'est produite. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PNG } from 'pngjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
interface Entry {
  key: number; pointers: number[]; expected_hex: string; source_hex?: string; target: number;
  expected_overflow?: boolean;
  layout: { initial_font: number; max_width: number; max_expanded_bytes: number;
    engine_fonts: Record<string, { hex: string }>;
    buffers?: Record<string, { max_bytes: number; max_width: number; probe_hex?: string }> };
}
interface Observation { case: number; negative: boolean; index: number; marker: number; target: number; width: number;
  window: number; x: number; column: number; guards: number; expanded: string; buffer: string }

function measuredWidth(raw: Buffer, entry: Entry): number {
  let width = 0, font = entry.layout.initial_font;
  for (let i = 0; i < raw.length; i++) {
    const value = raw[i];
    if (value === 0xff) { expect(i).toBe(raw.length - 1); return width; }
    if (value === 0xfc) {
      const command = raw[++i], argument = raw[++i];
      if (command === 0x06) font = argument & 15;
      else { expect(command).toBe(0x13); expect(width).toBeLessThanOrEqual(argument); width = argument; }
    } else {
      expect(value).toBeLessThan(0xf7);
      width += Buffer.from(entry.layout.engine_fonts[String(font)].hex, 'hex')[value];
    }
  }
  throw new Error('Terminateur manquant');
}

async function runOffscreen(temp: string, script: string, done: string): Promise<void> {
  const log = fs.openSync(path.join(temp, 'mgba.log'), 'w');
  const child = spawn(process.env.MGBA_PATH ?? '/opt/homebrew/opt/mgba/bin/mGBA', [
    '-C', 'mute=1', '-C', 'videoDriver=1', '-C', 'fpsTarget=240',
    '-C', 'audioSync=0', '-C', 'videoSync=0',
    ...['savegamePath', 'savestatePath', 'screenshotPath', 'cheatsPath'].flatMap(key => ['-C', `${key}=${temp}`]),
    '--script', script, path.join(temp, 'game.gba'),
  ], { env: { ...process.env, QT_QPA_PLATFORM: 'offscreen' }, stdio: ['ignore', log, log] });
  let launchError: Error | undefined;
  child.on('error', error => { launchError = error; });
  try {
    await expect.poll(() => {
      if (launchError) throw launchError;
      if (child.exitCode !== null) throw new Error(fs.readFileSync(path.join(temp, 'mgba.log'), 'utf8'));
      return fs.existsSync(done) && fs.statSync(done).size > 0;
    }, { timeout: 90_000 }).toBe(true);
  } finally {
    if (child.exitCode === null) child.kill('SIGTERM');
    await new Promise<void>(resolve => {
      if (child.exitCode !== null || child.signalCode !== null || launchError) resolve();
      else child.once('exit', () => resolve());
    });
    fs.closeSync(log);
  }
}

test('ES-009 : contenu, colonnes natives et tampons expansés des 26 surfaces vivantes', async ({ page }) => {
  const reportPath = path.join(root, 'output/reports/es009-formatted-probe.json');
  const report = JSON.parse(fs.readFileSync(reportPath, 'utf8')) as { records: Entry[]; rom: string };
  expect(report.records).toHaveLength(26);
  const rom = fs.readFileSync(path.resolve(root, report.rom));
  for (const entry of report.records) for (const ref of entry.pointers) {
    const target = rom.readUInt32LE(ref) - 0x08000000;
    expect(target).toBe(entry.target);
    expect(rom.subarray(target, target + entry.expected_hex.length / 2).toString('hex')).toBe(entry.expected_hex);
  }
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'f1040-formatted-'));
  fs.writeFileSync(path.join(temp, 'game.gba'), rom);
  execFileSync('python3', ['tests/e2e-playwright/fixtures/prepare_es009_probe.py', temp, reportPath], { cwd: root });
  await runOffscreen(temp, path.join(temp, 'probe.lua'), path.join(temp, 'result.json'));
  const result = JSON.parse(fs.readFileSync(path.join(temp, 'result.json'), 'utf8')) as { cases: Observation[]; readers: { index: number; site: number; target: number; raw: string }[] };
  expect(result.cases).toHaveLength(29);
  expect(result.cases.filter(c => c.negative)).toHaveLength(3);
  expect(result.readers).toHaveLength(report.records.reduce((sum, entry) => sum + entry.pointers.length, 0));
  for (const reader of result.readers) {
    const entry = report.records[reader.index];
    expect(entry.pointers).toContain(reader.site);
    expect(reader.raw).toBe(entry.expected_hex);
    expect(reader.target).toBe(0x08000000 + entry.target);
  }
  const figures: string[] = [];
  for (const observation of result.cases) {
    const entry = report.records[observation.index];
    const source = Buffer.from(observation.negative ? entry.source_hex! : entry.expected_hex, 'hex');
    expect(observation.marker, entry.key.toString(16)).toBe(0x1040);
    expect(observation.target).toBe(observation.negative ? 0x202f400 : rom.readUInt32LE(entry.pointers[0]));
    let displayed = source;
    if (entry.layout.buffers) {
      const buffer = Buffer.from(observation.buffer, 'hex');
      expect(entry.layout.buffers['0'].probe_hex).toBeDefined();
      const probe = Buffer.from(entry.layout.buffers['0'].probe_hex!, 'hex');
      const expectedBuffer = probe.at(-1) === 255 ? probe : Buffer.concat([probe, Buffer.from([255])]);
      expect(buffer).toEqual(expectedBuffer);
      expect(buffer.at(-1)).toBe(255);
      expect(buffer.length - 1).toBeLessThanOrEqual(entry.layout.buffers['0'].max_bytes);
      const at = source.indexOf(Buffer.from([0xf7, 0]));
      expect(at).toBeGreaterThanOrEqual(0);
      displayed = Buffer.concat([source.subarray(0, at), buffer.subarray(0, -1), source.subarray(at + 2)]);
      const actual = Buffer.from(observation.expanded, 'hex');
      expect(actual.subarray(0, displayed.length)).toEqual(displayed);
      expect(actual.length).toBe(observation.negative ? 256 : 80);
      expect(actual.subarray(displayed.length)).toEqual(Buffer.alloc(actual.length - displayed.length, 0xa5));
      expect(observation.guards).toBe(observation.negative ? 0 : 3);
      expect(displayed.length).toBeLessThanOrEqual(entry.layout.max_expanded_bytes);
      expect(observation.window).toBe(144);
      expect(observation.x).toBe(0);
    } else {
      const fc13 = source.indexOf(Buffer.from([0xfc, 0x13]));
      expect(fc13).toBeGreaterThanOrEqual(0);
      expect(observation.column).toBe(8 + source[fc13 + 2]);
      expect(observation.x).toBe(8);
    }
    expect(observation.width).toBe(measuredWidth(displayed, entry));
    if (observation.negative) expect(observation.width).toBeGreaterThan(entry.layout.max_width);
    else expect(observation.width).toBeLessThanOrEqual(entry.layout.max_width);
    const pngBytes = fs.readFileSync(path.join(temp, `case${observation.case}.png`));
    const png = PNG.sync.read(pngBytes);
    expect([png.width, png.height]).toEqual([240, 160]);
    let ink = 0, priceInk = 0, minimumX = 240, maximumX = -1;
    for (let y = 0; y < 16; y++) {
      if (!entry.layout.buffers) {
        const begin = (y * 240 + observation.column) * 4;
        const suffixBegin = ((y + 32) * 240 + observation.column) * 4;
        const bytes = (240 - observation.column) * 4;
        expect(png.data.subarray(begin, begin + bytes)).toEqual(png.data.subarray(suffixBegin, suffixBegin + bytes));
      }
      for (let x = 0; x < 240; x++) {
        if (png.data[(y * 240 + x) * 4] >= 200) continue;
        ink++;
        minimumX = Math.min(minimumX, x); maximumX = Math.max(maximumX, x);
        if (!entry.layout.buffers && x >= observation.column) priceInk++;
      }
    }
    expect(minimumX).toBeGreaterThanOrEqual(observation.x);
    expect(maximumX).toBeLessThan(observation.window);
    expect(ink).toBeGreaterThan(20);
    if (!entry.layout.buffers) expect(priceInk).toBeGreaterThan(10);
    figures.push(`<figure><figcaption>0x${entry.key.toString(16)} · ${observation.width}px${observation.negative ? ' · dépassement source détecté' : ''}</figcaption><div><img alt="Rendu moteur ${entry.key.toString(16)}" src="data:image/png;base64,${pngBytes.toString('base64')}"></div></figure>`);
  }
  await page.setContent(`<style>body{margin:0;background:#152334;color:white;font:16px monospace}main{display:grid;grid-template-columns:repeat(2,720px);gap:12px;padding:16px;width:max-content}figure{margin:0}figure div{height:60px;overflow:hidden}img{width:720px;height:480px;image-rendering:pixelated}</style><p>ES-009 · colonnes et expansions natives · sondes de source temporaires</p><main>${figures.join('')}</main>`);
  await expect(page.getByRole('img')).toHaveCount(29);
  await page.getByRole('img').evaluateAll(images => Promise.all(images.map(image => (image as HTMLImageElement).decode())));
  await page.screenshot({ path: path.join(os.tmpdir(), 'f1040-es009-engine-proof.png'), fullPage: true });
  console.log('Preuve après assertions : ' + path.join(os.tmpdir(), 'f1040-es009-engine-proof.png'));
});

test('ES-009 : six menus à prix réellement ouverts par les scripts multichoice', async ({ page }) => {
  const report = JSON.parse(fs.readFileSync(path.join(root, 'output/reports/es009-formatted-probe.json'), 'utf8')) as { rom: string };
  const original = fs.readFileSync(path.resolve(root, report.rom));
  // L’OCR confond c/o dans Bicycle sur la police pixel. Les octets exacts
  // et les bitmaps des colonnes sont contrôlés séparément par la sonde native.
  const groups = [
    { menu: 13, table: 0x3e01b8, width: 136, words: [/Bicy[co]le/i, /1.?000.?000/] },
    { menu: 14, table: 0x3e01c8, width: 144, words: [/ABRA/i, /CLEFAIRY/i, /DRATINI/i, /SCYTHER/i, /PORYGON/i] },
    { menu: 26, table: 0x3dff30, width: 120, words: [/FRESH WATER/i, /200/] },
    { menu: 27, table: 0x3dffb0, width: 112, words: [/50 COINS/i, /500 COINS/i] },
    { menu: 30, table: 0x3dff50, width: 136, words: [/TM13/i, /TM23/i, /TM24/i, /TM30/i, /TM35/i] },
    { menu: 41, table: 0x3dff80, width: 144, words: [/SMOKE BALL/i, /MIRACLE SEED/i, /CHARCOAL/i, /MYSTIC WATER/i, /YELLOW FLUTE/i] },
  ];
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'f1040-native-menus-'));
  const images: Buffer[] = [];
  for (const [index, group] of groups.entries()) {
    const scene = path.join(temp, String(index)); fs.mkdirSync(scene);
    const rom = Buffer.from(original);
    expect(rom.readUInt32LE(0x3e04b0 + group.menu * 8)).toBe(group.table + 0x08000000);
    const script = rom.lastIndexOf(Buffer.alloc(128, 255));
    expect(script).toBeGreaterThan(0x1000000);
    rom.set([0x6f, 0, 0, group.menu, 0, 2], script);
    fs.writeFileSync(path.join(scene, 'game.gba'), rom);
    fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(scene, 'game.sav'));
    const done = path.join(scene, 'result.json');
    const lua = path.join(scene, 'probe.lua');
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
 if f==2450 then
  emu:screenshot(${JSON.stringify(path.join(scene, 'render.png'))})
  local windows={}
  for n=0,31 do
   local p=0x20204b4+n*12
   if emu:read8(p)~=255 then
    table.insert(windows,'{"id":'..n..',"width":'..emu:read8(p+3)..',"height":'..emu:read8(p+4)..'}')
   end
  end
  local out=io.open(${JSON.stringify(done)},'w')
  out:write('['..table.concat(windows,',')..']');out:close()
 end
end)
`);
    await runOffscreen(scene, lua, done);
    const windows = JSON.parse(fs.readFileSync(done, 'utf8')) as { id: number; width: number; height: number }[];
    expect(windows.some(window => window.width * 8 === group.width && window.height >= 4)).toBe(true);
    images.push(fs.readFileSync(path.join(scene, 'render.png')));
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
  const figures = images.map((image, index) => `<figure><figcaption>Menu moteur ${groups[index].menu} · ${groups[index].width}px</figcaption><img alt="Menu à prix ${groups[index].menu}" src="data:image/png;base64,${image.toString('base64')}"></figure>`);
  await page.setContent(`<style>body{margin:0;background:#152334;color:white;font:18px monospace}main{display:grid;grid-template-columns:repeat(2,720px);gap:12px;padding:12px;width:max-content}figure{margin:0}img{width:720px;height:480px;image-rendering:pixelated}</style><main>${figures.join('')}</main>`);
  await expect(page.getByRole('img')).toHaveCount(6);
  await page.getByRole('img').evaluateAll(imgs => Promise.all(imgs.map(img => (img as HTMLImageElement).decode())));
  for (const [index, group] of groups.entries()) {
    const readable = path.join(temp, `readable${index}.png`);
    await page.getByRole('img').nth(index).screenshot({ path: readable });
    const text = [readable, path.join(temp, String(index), 'render.png')]
      .map(file => execFileSync(ocr, [file], { encoding: 'utf8', timeout: 60_000 }))
      .join(' ').replace(/\s+/g, ' ');
    console.log(`Menu ${group.menu}: ${text}`);
    for (const word of group.words) expect(text).toMatch(word);
  }
  const proof = path.join(os.tmpdir(), 'f1040-es009-native-menus.png');
  await page.locator('main').screenshot({ path: proof });
  console.log(`Preuve après assertions : ${proof}`);
});
