import { test, expect } from '@playwright/test';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PNG } from 'pngjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

function pixels(png: PNG, x: number, y: number, width: number, height: number): number[] {
  const result: number[] = [];
  for (let row = y; row < y + height; row++) {
    for (let column = x; column < x + width; column++) {
      const offset = (row * png.width + column) * 4;
      result.push(...png.data.subarray(offset, offset + 3));
    }
  }
  return result;
}

test('la carte conserve Dépl. et ne montre aucun deuxième point', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'world-map-194-'));
  const rom = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-fr.gba'));
  // Open the ordinary map through its existing initializer, without navigating
  // the Cube or saving. The wrapper normally supplies fly mode (2); use mode 1.
  expect(rom.readUInt16LE(0xC4EFE)).toBe(0x2002);
  rom.writeUInt16LE(0x2001, 0xC4EFE);
  fs.writeFileSync(path.join(temp, 'game.gba'), rom);
  fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
  fs.writeFileSync(path.join(temp, 'probe.lua'), `
local f=0
callbacks:add('frame', function()
 f=f+1
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 if f==2020 then
  emu:write32(0x030030F4,0x080C4EF9)
  emu:write8(0x03003528,0)
 end
 if f==2300 then emu:screenshot(${JSON.stringify(path.join(temp, 'map.png'))}) end
end)
`);
  async function capture(regress: boolean): Promise<PNG> {
    const input = Buffer.from(rom);
    if (regress) input[0x418E8B] = 0xAD;
    fs.writeFileSync(path.join(temp, 'game.gba'), input);
    fs.rmSync(path.join(temp, 'map.png'), { force: true });
    const child = spawn(process.env.MGBA_PATH ?? '/opt/homebrew/bin/mgba', [
      '-C', 'mute=1', '-C', 'videoDriver=1', '-C', 'fpsTarget=240',
      '-C', 'audioSync=0', '-C', 'videoSync=0',
      ...['savegamePath', 'savestatePath', 'screenshotPath', 'cheatsPath'].flatMap(key => ['-C', `${key}=${temp}`]),
      '--script', path.join(temp, 'probe.lua'), path.join(temp, 'game.gba'),
    ], { env: { ...process.env, QT_QPA_PLATFORM: 'offscreen' }, stdio: 'ignore' });
    let launchError: Error | undefined;
    child.on('error', error => { launchError = error; });
    try {
      await expect.poll(() => {
        if (launchError) throw launchError;
        if (child.exitCode !== null) throw new Error(`mGBA terminé : ${child.exitCode}`);
        return fs.existsSync(path.join(temp, 'map.png'));
      }, { timeout: 90_000 }).toBe(true);
      return PNG.sync.read(fs.readFileSync(path.join(temp, 'map.png')));
    } finally {
      child.kill('SIGTERM');
      await new Promise<void>(resolve => {
        if (child.exitCode !== null || child.signalCode !== null || launchError) resolve();
        else child.once('exit', () => resolve());
      });
    }
  }
  const regressed = await capture(true);
  const final = await capture(false);
  expect([final.width, final.height]).toEqual([240, 160]);
  // The second 40px action window must be completely blank blue.
  const background = pixels(final, 192, 0, 1, 1);
  expect(pixels(final, 192, 0, 40, 16)).toEqual(Array(40 * 16).fill(background).flat());
  expect(pixels(regressed, 192, 0, 40, 16)).not.toEqual(pixels(final, 192, 0, 40, 16));
  // Preserve the whole D-pad + Dépl. label, including its legitimate period.
  expect(pixels(final, 144, 0, 40, 16)).toEqual(pixels(regressed, 144, 0, 40, 16));
  expect(pixels(final, 172, 8, 3, 3)).toContain(255);
  const picture = fs.readFileSync(path.join(temp, 'map.png')).toString('base64');
  await page.setContent(`<style>body{margin:0}img{width:960px;height:640px;image-rendering:pixelated}</style><img alt="Carte corrigée" src="data:image/png;base64,${picture}">`);
  await expect(page.getByRole('img', { name: 'Carte corrigée' })).toBeVisible();
  await page.getByRole('img').screenshot({ path: process.env.WORLD_MAP_PROOF ?? path.join(os.tmpdir(), 'world-map-194-proof.png') });
});
