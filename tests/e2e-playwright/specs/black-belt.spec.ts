import { test, expect } from '@playwright/test';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PNG } from 'pngjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
// #196 : le moteur réel dessine la fiche Ceinture Noire dans une copie
// temporaire. La Boîte Costume du save sert de support, sans sauvegarde en jeu.
function namePixels(file: string): Buffer {
  const png = PNG.sync.read(fs.readFileSync(file));
  expect([png.width, png.height]).toEqual([240, 160]);
  return Buffer.concat(Array.from({ length: 16 }, (_, y) =>
    png.data.subarray(((y + 10) * 240 + 96) * 4, ((y + 10) * 240 + 228) * 4)));
}
test('Ceint.Noire est rendu dans le Cube et distingue l’ancien libellé', async ({ page }) => {
  const captures: string[] = [];
  for (const variant of ['actual', 'reference', 'old']) {
    const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'black-belt-'));
    const rom = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-fr.gba'));
    const base = 0x876074, stride = 44, belt = 216, fixture = 357;
    const expected = Buffer.from([189, 217, 221, 226, 232, 173, 200, 227, 221, 230, 217, 255]);
    const old = Buffer.from([189, 217, 221, 226, 232, 233, 230, 226, 227, 221, 230, 217, 255]);
    if (variant === 'actual') {
      expect(rom.subarray(base + belt * stride, base + belt * stride + expected.length)).toEqual(expected);
    }
    rom.copy(rom, base + fixture * stride, base + belt * stride, base + (belt + 1) * stride);
    if (variant !== 'actual') {
      rom.fill(0, base + fixture * stride, base + fixture * stride + 14);
      (variant === 'old' ? old : expected).copy(rom, base + fixture * stride);
    }
    fs.writeFileSync(path.join(temp, 'game.gba'), rom);
    fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
    const luaPath = path.join(temp, 'probe.lua');
    fs.writeFileSync(luaPath, `
local f=0
local keys={[2020]=3,[2070]=4,[2100]=4,[2130]=0,[2220]=4}
callbacks:add('frame', function()
 f=f+1
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 if keys[f] then emu:addKey(keys[f]) end
 if keys[f-4] then emu:clearKey(keys[f-4]) end
 if f==2320 then emu:screenshot(${JSON.stringify(path.join(temp, 'final.png'))}) end
end)
`);
    const binary = process.env.MGBA_PATH ?? '/opt/homebrew/opt/mgba/bin/mGBA';
    const child = spawn(binary, [
      '-C', 'mute=1', '-C', 'videoDriver=1', '-C', 'fpsTarget=240',
      '-C', 'audioSync=0', '-C', 'videoSync=0',
      ...['savegamePath', 'savestatePath', 'screenshotPath', 'cheatsPath'].flatMap(key => ['-C', `${key}=${temp}`]),
      '--script', luaPath, path.join(temp, 'game.gba'),
    ], { env: { ...process.env, QT_QPA_PLATFORM: 'offscreen' }, stdio: 'ignore' });
    let launchError: Error | undefined;
    child.on('error', error => { launchError = error; });
    const final = path.join(temp, 'final.png');
    try {
      await expect.poll(() => {
        if (launchError) throw launchError;
        if (child.exitCode !== null) throw new Error(`mGBA terminé : ${child.exitCode}`);
        return fs.existsSync(final);
      }, { timeout: 90_000 }).toBe(true);
      captures.push(final);
    } finally {
      child.kill('SIGTERM');
      await new Promise<void>(resolve => {
        if (child.exitCode !== null || launchError) resolve();
        else child.once('exit', () => resolve());
      });
    }
  }
  const actual = namePixels(captures[0]);
  expect(actual.equals(namePixels(captures[1]))).toBe(true);
  expect(actual.equals(namePixels(captures[2]))).toBe(false);
  const data = fs.readFileSync(captures[0]).toString('base64');
  await page.setContent(`<style>body{margin:0;background:#222}img{width:960px;height:640px;image-rendering:pixelated}</style><img alt="Cube : Ceint.Noire" src="data:image/png;base64,${data}">`);
  await expect(page.getByRole('img')).toBeVisible();
  const proof = process.env.BLACK_BELT_PROOF ?? path.join(os.tmpdir(), 'black-belt-proof.png');
  await page.getByRole('img').screenshot({ path: proof });
  console.log(`Preuve : ${proof}`);
});
