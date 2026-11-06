/** ES-013 : deux tables de natures, StringCopy et impression natives, sans sauvegarde. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PNG } from 'pngjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
interface Entry { key: number; pointers: number[]; expected_hex: string; target: number }
interface Observation { id: number; table: number; marker: number; target: number; width0: number; width2: number; buffer: string }

test('ES-013 : 25 ID aux deux tables et copies natives sans débordement', async ({ page }) => {
  const report = JSON.parse(fs.readFileSync(path.join(root, 'output/reports/es013-probe.json'), 'utf8')) as { records: Entry[]; rom: string };
  const contract = JSON.parse(fs.readFileSync(path.join(root, 'tests/unit/fixtures/es013_surfaces_contract.json'), 'utf8')) as { entries: { offset: string }[] };
  const keys = contract.entries.map(entry => Number(entry.offset));
  const records = keys.map(key => report.records.find(entry => entry.key === key)!);
  expect(records).toHaveLength(25);
  const rom = fs.readFileSync(path.resolve(root, report.rom));
  records.forEach((entry, id) => {
    expect(entry).toBeDefined();
    expect(entry.pointers).toEqual([0x463e60 + id * 4, 0x1fe65f4 + id * 4]);
    for (const ref of entry.pointers) {
      const target = rom.readUInt32LE(ref) - 0x08000000;
      expect(target).toBe(entry.target);
      expect(rom.subarray(target, target + entry.expected_hex.length / 2).toString('hex')).toBe(entry.expected_hex);
    }
  });
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'f1044-natures-'));
  fs.writeFileSync(path.join(temp, 'game.gba'), rom);
  execFileSync(process.env.PYTHON ?? 'python3', ['tests/e2e-playwright/fixtures/prepare_es013_natures_probe.py', temp], { cwd: root });
  const log = fs.openSync(path.join(temp, 'mgba.log'), 'w');
  const child = spawn(process.env.MGBA_PATH ?? '/opt/homebrew/opt/mgba/bin/mGBA', [
    '-C', 'mute=1', '-C', 'videoDriver=1', '-C', 'fpsTarget=240', '-C', 'audioSync=0', '-C', 'videoSync=0',
    ...['savegamePath', 'savestatePath', 'screenshotPath', 'cheatsPath'].flatMap(key => ['-C', `${key}=${temp}`]),
    '--script', path.join(temp, 'probe.lua'), path.join(temp, 'game.gba'),
  ], { env: { ...process.env, QT_QPA_PLATFORM: 'offscreen' }, stdio: ['ignore', log, log] });
  let launchError: Error | undefined;
  child.on('error', error => { launchError = error; });
  const done = path.join(temp, 'result.json');
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
  const observations = JSON.parse(fs.readFileSync(done, 'utf8')) as Observation[];
  expect(observations).toHaveLength(50);
  for (const actual of observations) {
    const entry = records[actual.id];
    const raw = Buffer.from(entry.expected_hex, 'hex');
    expect(actual.marker).toBe(0x1044);
    expect(actual.target).toBe(rom.readUInt32LE(entry.pointers[actual.table]));
    expect(actual.width0).toBeGreaterThan(0);
    expect(actual.width0).toBeLessThanOrEqual(42);
    expect(actual.width2).toBeGreaterThan(0);
    expect(actual.width2).toBeLessThanOrEqual(42);
    expect(raw.length).toBeLessThanOrEqual(8);
    const buffer = Buffer.from(actual.buffer, 'hex');
    expect(buffer.subarray(0, 4)).toEqual(Buffer.alloc(4, 0xa5));
    expect(buffer.subarray(4, 4 + raw.length)).toEqual(raw);
    expect(buffer.subarray(4 + raw.length)).toEqual(Buffer.alloc(28 - raw.length, 0xa5));
  }
  const figures: string[] = [];
  for (let id = 0; id < 25; id++) {
    const bytes = fs.readFileSync(path.join(temp, `case${id}.png`));
    const png = PNG.sync.read(bytes);
    expect([png.width, png.height]).toEqual([240, 160]);
    expect(png.data.subarray(0, 16 * 240 * 4)).toEqual(png.data.subarray(32 * 240 * 4, 48 * 240 * 4));
    let ink = 0, maxX = -1;
    for (let y = 0; y < 16; y++) for (let x = 0; x < 240; x++) {
      if (png.data[(y * 240 + x) * 4] < 200) { ink++; maxX = Math.max(maxX, x); }
    }
    expect(ink).toBeGreaterThan(30);
    expect(maxX).toBeLessThan(42);
    figures.push(`<figure><figcaption>ID ${id} · tables 463E60 / 1FE65F4</figcaption><div><img alt="Nature ID ${id}, deux impressions natives" src="data:image/png;base64,${bytes.toString('base64')}"></div></figure>`);
  }
  await page.setContent(`<style>body{margin:0;background:#152334;color:white;font:16px monospace}main{display:grid;grid-template-columns:repeat(3,480px);gap:12px;padding:16px;width:max-content}figure{margin:0}figure div{height:96px;overflow:hidden}img{width:480px;height:320px;image-rendering:pixelated}</style><p>ES-013 · 25 ID × deux tables · copies et métriques natives · sentinelles temporaires</p><main>${figures.join('')}</main>`);
  await expect(page.getByRole('img')).toHaveCount(25);
  await page.getByRole('img').evaluateAll(images => Promise.all(images.map(image => (image as HTMLImageElement).decode())));
  const proof = path.join(os.tmpdir(), 'f1044-natures-proof.png');
  await page.screenshot({ path: proof, fullPage: true });
  console.log(`Preuve après assertions : ${proof}`);
});
