/** Socle PT-BR : boot réel sans sauvegarde, mGBA et Chromium hors écran. */
import { test, expect } from '@playwright/test';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

test('la ROM PT-BR démarre et poursuit son exécution', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'pt-seed-'));
  fs.copyFileSync(process.env.ROM_PATH ?? 'output/roms/GenedRom-pt.gba', path.join(temp, 'game.gba'));
  fs.writeFileSync(path.join(temp, 'probe.lua'), `
local f=0
callbacks:add('frame', function()
 f=f+1
 if f==300 then emu:screenshot('${temp}/boot.png') end
 if f==600 then
  emu:screenshot('${temp}/running.png')
  local out=io.open('${temp}/frames.txt','w'); out:write(tostring(f)); out:close()
 end
end)
`);
  const child = spawn(process.env.MGBA_PATH ?? '/opt/homebrew/opt/mgba/bin/mGBA', [
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
      return fs.existsSync(path.join(temp, 'frames.txt'));
    }, { timeout: 60_000 }).toBe(true);
    expect(fs.readFileSync(path.join(temp, 'frames.txt'), 'utf8')).toBe('600');
    const png = fs.readFileSync(path.join(temp, 'running.png'));
    expect(png.length).toBeGreaterThan(1000);
    await page.setContent(`<img alt="Boot PT-BR" style="width:720px;image-rendering:pixelated" src="data:image/png;base64,${png.toString('base64')}">`);
    await expect(page.getByRole('img', { name: 'Boot PT-BR' })).toBeVisible();
    await page.getByRole('img').screenshot({ path: path.join(os.tmpdir(), 'a664-pt-boot.png') });
  } finally {
    if (child.exitCode === null) child.kill('SIGTERM');
  }
});
