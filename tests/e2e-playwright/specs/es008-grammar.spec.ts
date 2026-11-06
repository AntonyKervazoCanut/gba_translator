/** B-1038 : vrais consommateurs et police mGBA, phrases temporaires hors combined. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { PNG } from 'pngjs';

test('les cinq groupes ignorent le buffer grammatical et rendent la phrase entière', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'b1038-mgba-'));
  execFileSync('python3', ['tests/e2e-playwright/fixtures/prepare_es008_grammar_probe.py', temp]);
  const expected: string[] = JSON.parse(fs.readFileSync(path.join(temp, 'expected.json'), 'utf8'));
  const rom = fs.readFileSync(path.join(temp, 'game.gba'));
  const log = fs.openSync(path.join(temp, 'mgba.log'), 'w');
  const child = spawn(process.env.MGBA_PATH ?? '/opt/homebrew/opt/mgba/bin/mGBA', [
    '-C', 'mute=1', '-C', 'videoDriver=1', '-C', 'fpsTarget=240', '-C', 'audioSync=0', '-C', 'videoSync=0',
    ...['savegamePath', 'savestatePath', 'screenshotPath', 'cheatsPath'].flatMap(key => ['-C', `${key}=${temp}`]),
    '--script', path.join(temp, 'probe.lua'), path.join(temp, 'game.gba'),
  ], { env: { ...process.env, QT_QPA_PLATFORM: 'offscreen' }, stdio: ['ignore', log, log] });
  let error: Error | undefined;
  child.on('error', value => { error = value; });
  try {
    await expect.poll(() => {
      if (error) throw error;
      if (child.exitCode !== null) throw new Error(fs.readFileSync(path.join(temp, 'mgba.log'), 'utf8'));
      return fs.existsSync(path.join(temp, 'result.json'));
    }, { timeout: 60_000 }).toBe(true);
    const result = JSON.parse(fs.readFileSync(path.join(temp, 'result.json'), 'utf8'));
    expect(result.marker).toBe(0x1038);
    expect(result.buffers).toHaveLength(7);
    for (let n = 0; n < 7; n++) {
      expect(result.buffers[n].slice(0, expected[n].length)).toBe(expected[n]);
      expect(result.buffers[n].slice(expected[n].length)).toBe('a5'.repeat(256 - expected[n].length / 2));
    }
    const pngBytes = fs.readFileSync(path.join(temp, 'render.png'));
    const png = PNG.sync.read(pngBytes);
    expect([png.width, png.height]).toEqual([240, 160]);
    const glyphBase = rom.readUInt32LE(0x658c) - 0x08000000;
    const widths = rom.readUInt32LE(0x6594) - 0x08000000;
    const mask = new Set<number>();
    for (let n = 0; n < 5; n++) {
      let x = 4, y = n * 32;
      for (const cp of Buffer.from(expected[n], 'hex').subarray(0, -1)) {
        if (cp === 0xfe) { x = 4; y += 16; continue; }
        const width = rom[widths + cp];
        expect(x + width).toBeLessThanOrEqual(240);
        for (let dy = 0; dy < 16; dy++) for (let dx = 0; dx < 8; dx++) {
          const at = glyphBase + cp * 64 + (dy >> 3) * 32 + (dy % 8) * 2;
          if ((rom.readUInt16LE(at) >> (14 - 2 * dx) & 3) === 1) mask.add((y + dy) * 240 + x + dx);
        }
        x += width;
      }
    }
    expect(mask.size).toBeGreaterThan(1000);
    for (let p = 0; p < 240 * 160; p++) {
      expect(png.data[p * 4] < 100, `pixel ${p % 240},${Math.floor(p / 240)}`).toBe(mask.has(p));
    }
    await page.setContent(`<style>body{font:18px monospace;background:#17202b;color:white}img{width:960px;image-rendering:pixelated}</style>
      <p>B-1038 — 5 groupes du moteur ; phrases temporaires, noms longs, terminaison vérifiée</p>
      <img alt="Phrases complètes des cinq groupes dans mGBA" src="data:image/png;base64,${pngBytes.toString('base64')}">`);
    await page.getByRole('img').evaluate(async (img: HTMLImageElement) => img.decode());
    await expect(page.getByRole('img')).toBeVisible();
    await page.screenshot({ path: path.join(os.tmpdir(), 'b1038-grammaire-es.png') });
    console.log(`Sonde et buffers : ${temp}`);
  } finally {
    if (child.exitCode === null) child.kill('SIGTERM');
    fs.closeSync(log);
  }
});
