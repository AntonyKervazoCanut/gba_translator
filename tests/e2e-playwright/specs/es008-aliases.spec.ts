/** F-1037 : consommateurs finaux, métriques et impression natives des sept alias.
 * La mire RAM réutilise AddTextPrinterParameterized3, GetStringWidth et les
 * commandes F8 du moteur. Ce n'est pas une certification des parcours ni des
 * traductions finales de F-858. Aucun fichier de sauvegarde n'est chargé/écrit. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PNG } from 'pngjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
interface RecordEntry {
  key: number; live: number; pointers: number[]; expected_hex: string; target: number;
  layout: { font: 'small' | 'normal'; max_width: number; glyph_widths_hex: string; keypad_widths: number[] };
}
interface Result {
  marker: number;
  observations: { index: number; pointer: number; target: number; raw: string }[];
  widths: { target: number; width: number; x: number }[];
}

function engineTableWidth(raw: Buffer, entry: RecordEntry): number {
  const table = Buffer.from(entry.layout.glyph_widths_hex, 'hex');
  let width = 0;
  for (let i = 0; i < raw.length; i++) {
    const byte = raw[i];
    if (byte === 0xff) { expect(i).toBe(raw.length - 1); break; }
    if (byte === 0xf8) width += entry.layout.keypad_widths[raw[++i]];
    else if (byte === 0xf9) width += table[0x100 + raw[++i]];
    else { expect(byte).toBeLessThan(0xf7); width += table[byte]; }
  }
  return width;
}

test('ES-008 : les sept alias atteignent les lecteurs finaux et le moteur de menus', async ({ page }) => {
  const reportPath = path.join(root, 'output/reports/es008-alias-probe.json');
  const report = JSON.parse(fs.readFileSync(reportPath, 'utf8')) as { records: RecordEntry[]; rom: string };
  expect(report.records).toHaveLength(7);
  expect(report.records.map(r => r.key)).toEqual([0x415d45, 0x415d4f, 0x415d5e, 0x415d77, 0x415d8a, 0x4160f9, 0x416101]);
  const rom = fs.readFileSync(path.resolve(root, report.rom));
  const source = fs.readFileSync(path.join(root, 'input/roms/englishrom.gba'));
  const expectedCommands = [[0,], [0,1], [10,0,1], [10,0,1], [0], [], []];
  for (const [index, entry] of report.records.entries()) {
    const raw = Buffer.from(entry.expected_hex, 'hex');
    const controls: number[] = [];
    for (let i=0;i<raw.length;i++) if(raw[i]===0xf8) controls.push(raw[++i]);
    expect(controls).toEqual(expectedCommands[index]);
    expect(source.subarray(entry.key, entry.live)).toEqual(Buffer.alloc(entry.live-entry.key));
    expect(rom.subarray(entry.key, entry.live)).toEqual(source.subarray(entry.key, entry.live));
    for (const pointer of entry.pointers) {
      const target = rom.readUInt32LE(pointer) - 0x08000000;
      expect(target).not.toBe(entry.live);
      expect(rom.subarray(target, target+raw.length)).toEqual(raw);
    }
  }
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'f1037-menus-'));
  fs.writeFileSync(path.join(temp, 'game.gba'), rom);
  execFileSync('python3', ['tests/e2e-playwright/fixtures/prepare_es008_probe.py', temp, reportPath], { cwd: root });
  const log = fs.openSync(path.join(temp, 'mgba.log'), 'w');
  const child = spawn(process.env.MGBA_PATH ?? '/opt/homebrew/opt/mgba/bin/mGBA', [
    '-C', 'mute=1', '-C', 'videoDriver=1', '-C', 'fpsTarget=240',
    '-C', 'audioSync=0', '-C', 'videoSync=0',
    ...['savegamePath', 'savestatePath', 'screenshotPath', 'cheatsPath'].flatMap(key => ['-C', `${key}=${temp}`]),
    '--script', path.join(temp, 'probe.lua'), path.join(temp, 'game.gba'),
  ], { env: { ...process.env, QT_QPA_PLATFORM: 'offscreen' }, stdio: ['ignore', log, log] });
  let launchError: Error | undefined;
  child.on('error', error => { launchError = error; });
  try {
    await expect.poll(() => {
      if (launchError) throw launchError;
      if (child.exitCode !== null) throw new Error(fs.readFileSync(path.join(temp, 'mgba.log'), 'utf8'));
      return fs.existsSync(path.join(temp, 'result.json'));
    }, { timeout: 60_000 }).toBe(true);
    const result = JSON.parse(fs.readFileSync(path.join(temp, 'result.json'), 'utf8')) as Result;
    expect(result.marker).toBe(0x1037);
    expect(result.observations).toHaveLength(14);
    for (const observation of result.observations) {
      const entry = report.records[observation.index];
      expect(entry.pointers).toContain(observation.pointer);
      expect(observation.raw).toBe(entry.expected_hex);
      expect(observation.target).toBe(rom.readUInt32LE(observation.pointer));
    }
    const pngBytes = fs.readFileSync(path.join(temp, 'render.png'));
    const png = PNG.sync.read(pngBytes);
    expect([png.width,png.height]).toEqual([240,160]);
    for (const [n, entry] of report.records.entries()) {
      const measured = result.widths[n];
      const width = engineTableWidth(Buffer.from(entry.expected_hex,'hex'),entry);
      expect(measured.width).toBe(width);
      expect(width).toBeLessThanOrEqual(entry.layout.max_width);
      expect(measured.target).toBe(rom.readUInt32LE(entry.pointers[0]));
      expect(measured.x).toBe(entry.layout.font==='small' ? 236-width : 4);
      let ink=0;
      for(let y=4+n*20;y<20+n*20;y++)for(let x=0;x<240;x++) {
        if(png.data[(y*240+x)*4]>=200)continue;
        ink++;
        expect(x).toBeGreaterThanOrEqual(measured.x);
        expect(x).toBeLessThanOrEqual(measured.x+width);
      }
      expect(ink, `rendu moteur absent pour ${entry.key.toString(16)}`).toBeGreaterThan(15);
    }
    await page.setContent(`<style>body{margin:0;background:#152334;color:white;font:18px monospace}p{padding:8px 16px}img{width:960px;height:640px;image-rendering:pixelated}</style><p>ES-008 · sept alias · 14 lecteurs · largeur et commandes moteur vérifiées</p><img alt="Mire moteur ES-008 : sept sentinelles temporaires" src="data:image/png;base64,${pngBytes.toString('base64')}"><p>Sonde RAM du moteur de menus · valeurs finales réservées à F-858</p>`);
    await page.getByRole('img').evaluate(async (image: HTMLImageElement) => image.decode());
    await expect(page.getByRole('img')).toBeVisible();
    const proof = path.join(os.tmpdir(),'f1037-es008-proof.png');
    await page.screenshot({path:proof,fullPage:true});
    console.log(`Preuve après assertions : ${proof}`);
  } finally {
    if(child.exitCode===null)child.kill('SIGTERM');
    await new Promise<void>(resolve=> {
      if(child.exitCode!==null || child.signalCode!==null || launchError)resolve();
      else child.once('exit',()=>resolve());
    });
    fs.closeSync(log);
  }
});
