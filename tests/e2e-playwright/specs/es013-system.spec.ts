/** ES-013 : expansion F7 native et rendu des fenêtres FC13/F8/pages. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

test('ES-013 : commandes livrées, expansion F7 et cinq fenêtres natives', async ({ page }) => {
  const reportPath = path.join(root, 'output/reports/es013-probe.json');
  const report = JSON.parse(fs.readFileSync(reportPath, 'utf8')) as {
    rom: string; records: { key: number; pointers: number[]; expected_hex: string; target: number }[];
  };
  const keys = [0x457d44, 0x459378, 0x458fc6];
  const selected = keys.map(key => report.records.find(entry => entry.key === key)!);
  expect(selected.every(Boolean)).toBe(true);
  const rom = fs.readFileSync(path.resolve(root, report.rom));
  for (const entry of selected) for (const ref of entry.pointers) {
    const target = rom.readUInt32LE(ref) - 0x08000000;
    expect(target).toBe(entry.target);
    expect(rom.subarray(target, target + entry.expected_hex.length / 2).toString('hex')).toBe(entry.expected_hex);
  }
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'f1044-system-'));
  fs.writeFileSync(path.join(temp, 'game.gba'), rom);
  execFileSync('python3', ['tests/e2e-playwright/fixtures/prepare_es013_system_probe.py', temp, reportPath], { cwd: root });
  const log = fs.openSync(path.join(temp, 'mgba.log'), 'w');
  const child = spawn(process.env.MGBA_PATH ?? '/opt/homebrew/opt/mgba/bin/mGBA', [
    '-C', 'mute=1', '-C', 'videoDriver=1', '-C', 'fpsTarget=240', '-C', 'audioSync=0', '-C', 'videoSync=0',
    ...['savegamePath', 'savestatePath', 'screenshotPath', 'cheatsPath'].flatMap(key => ['-C', `${key}=${temp}`]),
    '--script', path.join(temp, 'probe.lua'), path.join(temp, 'game.gba'),
  ], { env: { ...process.env, QT_QPA_PLATFORM: 'offscreen' }, stdio: ['ignore', log, log] });
  try {
    await expect.poll(() => fs.existsSync(path.join(temp, 'result.json')), { timeout: 90_000 }).toBe(true);
  } finally {
    child.kill('SIGTERM');
    await new Promise<void>(resolve => child.exitCode !== null || child.signalCode !== null ? resolve() : child.once('exit', () => resolve()));
    fs.closeSync(log);
  }
  const result = JSON.parse(fs.readFileSync(path.join(temp, 'result.json'), 'utf8')) as {
    marker: number; guards: number; expanded: string; tiles: string; widths: number[];
  };
  expect(result.marker).toBe(0x1044);
  expect(result.guards).toBe(1);
  const source = Buffer.from(selected[0].expected_hex, 'hex');
  const buffers = [Buffer.from('a2a1a1', 'hex'), Buffer.alloc(10, 0xd1), Buffer.from('a2a1a1', 'hex'), Buffer.alloc(10, 0xd1)];
  const expected: number[] = [];
  const order: number[] = [];
  for (let i = 0; i < source.length; i++) {
    if (source[i] === 0xf7) { const index = source[++i]; order.push(index); expected.push(...buffers[index]); }
    else expected.push(source[i]);
  }
  expect(order).toEqual([0, 1, 2, 3]);
  expect(Buffer.from(result.expanded, 'hex')).toEqual(Buffer.from(expected));
  expect(expected.filter(value => value === 0xfb)).toHaveLength(2);
  expect(expected.length).toBeLessThanOrEqual(512);
  expect(result.widths).toHaveLength(5);
  for (let i = 0; i < 5; i++) {
    expect(result.widths[i]).toBeGreaterThan(0);
    expect(result.widths[i]).toBeLessThanOrEqual([216, 232, 208, 208, 208][i]);
  }
  const tiles = Buffer.from(result.tiles, 'hex');
  for (let section = 0; section < 5; section++) {
    const width = section === 1 ? 240 : section === 0 ? 224 : 208;
    const bitmap = tiles.subarray(section * 4096, section * 4096 + width * 32 / 2);
    expect(bitmap.some(value => value !== 0), `fenêtre native ${section}`).toBe(true);
    expect(tiles.subarray(section * 4096 + width * 32 / 2, (section + 1) * 4096).every(value => value === 0)).toBe(true);
  }
  // Les trois colonnes FC13 viennent des arguments entiers 3C/6E/C6.
  for (const column of [60, 110, 198]) {
    const x = 8 + column;
    const columnBytes: number[] = [];
    for (let y = 0; y < 16; y++) for (let dx = 0; dx < 4; dx++) {
      const px = x + dx;
      const byte = tiles[(y >> 3) * 28 * 32 + (px >> 3) * 32 + (y & 7) * 4 + ((px & 7) >> 1)];
      columnBytes.push((byte >> ((px & 1) * 4)) & 15);
    }
    expect(columnBytes.some(value => value !== 0), `colonne ${column}`).toBe(true);
  }
  const aliases = JSON.parse(fs.readFileSync(path.join(root, 'languages/es-maint/text_aliases.json'), 'utf8'));
  const small = Buffer.from(aliases.fonts.small.hex, 'hex');
  const icons = Buffer.from(aliases.keypad_icons.hex, 'hex');
  const help = Buffer.from(selected[2].expected_hex, 'hex');
  let helpX = 8;
  const iconOrder: number[] = [];
  for (let i = 0; i < help.length && help[i] !== 255; i++) {
    if (help[i] === 0xf8) {
      const index = help[++i], width = icons[index * 4 + 2];
      iconOrder.push(index);
      const pixels: number[] = [];
      for (let y = 0; y < 16; y++) for (let x = helpX; x < helpX + width; x++) {
        const value = tiles[4096 + (y >> 3) * 30 * 32 + (x >> 3) * 32 + (y & 7) * 4 + ((x & 7) >> 1)];
        pixels.push((value >> ((x & 1) * 4)) & 15);
      }
      expect(pixels.some(value => value !== 0), `icône F8 ${index}`).toBe(true);
      helpX += width;
    } else helpX += small[help[i]];
  }
  expect(iconOrder).toEqual([10, 0, 1]);
  const png = fs.readFileSync(path.join(temp, 'native.png')).toString('base64');
  await page.setContent(`<html lang="fr"><body style="margin:24px;background:#e9edf1;font:18px sans-serif"><h1>ES-013 — fenêtres natives</h1><p>En-tête FC13 · aide F8 · trois pages F7 expansées</p><img alt="Rendu natif vérifié" style="width:720px;image-rendering:pixelated" src="data:image/png;base64,${png}"><p>Quatre tampons longs, ordre 0/1/2/3, deux FB et canaris vérifiés.</p></body></html>`);
  await expect(page.getByRole('img', { name: 'Rendu natif vérifié' })).toBeVisible();
  await page.screenshot({ path: path.join(temp, 'proof.png'), fullPage: true });
  console.log(`ES013_SYSTEM_PROOF=${path.join(temp, 'proof.png')}`);
});
