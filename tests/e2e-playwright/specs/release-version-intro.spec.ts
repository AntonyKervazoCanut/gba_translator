/** #193 : l'écran NOT FOR SALE affiche le numéro de la publication téléchargée.
 * La ROM est matérialisée depuis les patchs réécrits par le workflow de release
 * (`scripts/materialize_release_rom.py`). mGBA réel, hors écran : un script Lua
 * lit la bande de version dans la VRAM et capture l'écran pendant l'intro.
 */
import { test, expect } from '@playwright/test';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const expected = process.env.EXPECTED_VERSION ?? 'FR.2.1.156';
const LAST_FRAME = 1800;
const BAND_ADDRESS = 0x06000000 + 0xe1 * 32; // BG0 charblock 0, tuiles 0xE1-0xEC.

// Glyphes 4x5 de languages/fr/patches/version.py, recopiés pour un décodage indépendant.
const GLYPH_ROWS: Record<string, string> = {
  '0': '0110 1001 1001 1001 0110', '1': '0010 0110 0010 0010 0111',
  '2': '0110 1001 0010 0100 1111', '3': '1110 0001 0110 0001 1110',
  '4': '0011 0101 1111 0001 0001', '5': '1111 1000 1110 0001 1110',
  '6': '0110 1000 1110 1001 0110', '7': '1111 0001 0010 0100 0100',
  '8': '0110 1001 0110 1001 0110', '9': '0110 1001 0111 0001 0110',
  F: '1111 1000 1110 1000 1000', R: '1110 1001 1110 1010 1001',
  I: '1111 0110 0110 0110 1111', T: '1111 0110 0110 0110 0110',
  D: '1110 1001 1001 1001 1110', E: '1111 1000 1110 1000 1111',
  N: '1001 1101 1011 1001 1001', '.': '0000 0000 0000 0000 0110',
};
const GLYPHS = Object.fromEntries(
  Object.entries(GLYPH_ROWS).map(([char, rows]) => [rows.replaceAll(' ', ''), char]),
);

/** Décode la bande 48x16 px (6x2 tuiles 4bpp) comme scripts/verify_version_display.py. */
function decodeBand(bytes: Buffer): string {
  const pixel = (x: number, y: number) => {
    const tile = Math.floor(y / 8) * 6 + Math.floor(x / 8);
    const byte = bytes[tile * 32 + (y % 8) * 4 + ((x % 8) >> 1)];
    return (x & 1) === 0 ? byte & 0xf : byte >> 4;
  };
  const y0 = 5;
  const columns = Array.from({ length: 48 }, (_, x) => x)
    .filter(x => [0, 1, 2, 3, 4].some(dy => pixel(x, y0 + dy) === 4));
  if (!columns.length) return '';
  let text = '';
  for (let x = columns[0]; x + 4 <= 48; x += 4) {
    let key = '';
    for (let dy = 0; dy < 5; dy++) for (let dx = 0; dx < 4; dx++) key += pixel(x + dx, y0 + dy) === 4 ? '1' : '0';
    if (!key.includes('1')) break;
    text += GLYPHS[key] ?? '?';
  }
  return text;
}

test(`l'écran NOT FOR SALE affiche ${expected}`, async ({ page }) => {
  const rom = process.env.ROM_PATH;
  expect(rom, 'ROM_PATH doit désigner une ROM matérialisée depuis une publication').toBeTruthy();
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'release-version-'));
  fs.copyFileSync(rom!, path.join(temp, 'game.gba'));
  const lua = path.join(temp, 'probe.lua');
  fs.writeFileSync(lua, `
local f=0
local dump=io.open(${JSON.stringify(temp)}..'/bands.txt','w')
callbacks:add('frame', function()
 f=f+1
 if f%30==0 and f<=${LAST_FRAME} then
  local hex={}
  for i=0,383 do hex[#hex+1]=string.format('%02x', emu:read8(${BAND_ADDRESS}+i)) end
  dump:write(f, ' ', string.format('%02x', emu:read8(0x080000BC)), ' ', table.concat(hex), '\\n')
  dump:flush()
  emu:screenshot(${JSON.stringify(temp)}..'/frame'..f..'.png')
 end
 if f==${LAST_FRAME} then dump:close() end
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
      return fs.existsSync(path.join(temp, `frame${LAST_FRAME}.png`));
    }, { timeout: 90_000 }).toBe(true);
  } finally {
    child.kill('SIGTERM');
    await new Promise<void>(resolve => {
      if (child.exitCode !== null || child.signalCode !== null || launchError) resolve();
      else child.once('exit', () => resolve());
    });
  }

  const samples = fs.readFileSync(path.join(temp, 'bands.txt'), 'utf8').trim().split('\n')
    .map(line => line.split(' '))
    .map(([frame, header, band]) => ({ frame: Number(frame), header: parseInt(header, 16), text: decodeBand(Buffer.from(band, 'hex')) }));
  const shown = samples.filter(sample => sample.text === expected);
  expect(shown.length, `bandes lues : ${[...new Set(samples.map(s => s.text))].join(', ')}`).toBeGreaterThan(0);
  expect(samples.map(sample => sample.text)).not.toContain('FR.2.1.44');
  expect(shown[0].header).toBe(Number(expected.split('.').pop()) & 0xff);

  // Capture prise une seconde après le chargement de la bande (fondu terminé).
  const frame = Math.min(shown[0].frame + 60, shown[shown.length - 1].frame);
  const picture = fs.readFileSync(path.join(temp, `frame${frame}.png`)).toString('base64');
  await page.setContent(`<style>body{margin:0;background:#222}img{width:720px;height:480px;image-rendering:pixelated}</style><img alt="NOT FOR SALE" src="data:image/png;base64,${picture}">`);
  await expect(page.getByRole('img')).toBeVisible();
  const proof = process.env.RELEASE_VERSION_PROOF ?? path.join(os.tmpdir(), 'release-version-intro-proof.png');
  await page.getByRole('img').screenshot({ path: proof });
  console.log(`Preuve : ${proof} (frame ${frame})`);
});
