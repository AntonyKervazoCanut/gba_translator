/** PT-04 : la chaîne injectée est lue via son pointeur vivant puis rendue par mGBA. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PNG } from 'pngjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

function ink(png: PNG, x: number, y: number): boolean {
  const at = (y * png.width + x) * 4;
  return Math.max(...png.data.subarray(at, at + 3)) < 100;
}

test('le dialogue PT-04 affiche Valeu por batalhar comigo sans débordement', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'pt04-dialogue-'));
  const rom = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-pt.gba'));
  const target = rom.readUInt32LE(0x26d3d9) - 0x08000000; // 0x26d5bf, Dresseur
  const expected = Buffer.from(execFileSync('python3', ['-c',
    'from src.core.text_codec import TextEncoder; import sys; sys.stdout.buffer.write(TextEncoder.encode_pokemon("Valeu por batalhar comigo!"))'], { cwd: root }));
  expect(rom.subarray(target, target + expected.length)).toEqual(expected);
  // Seul le script de déclenchement est ajouté à la copie ; le texte testé est livré par le build.
  const script = rom.lastIndexOf(Buffer.alloc(256, 255));
  expect(script).toBeGreaterThan(0x1000000);
  rom.set([0x0f, 0], script);
  rom.writeUInt32LE(0x08000000 + target, script + 2);
  rom.set([0x09, 6, 2], script + 6);
  const romPath = path.join(temp, 'game.gba');
  fs.writeFileSync(romPath, rom);
  const lua = path.join(temp, 'probe.lua');
  fs.writeFileSync(lua, `
local f=0
callbacks:add('frame', function()
 f=f+1
 if f==2 then emu:loadStateFile(${JSON.stringify(path.join(root, 'output/roms/GenedRom-fr.ss2'))}) end
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 if f==2020 then
  assert(emu:read8(0x03000EA8)==2, 'Un script est déjà actif')
  emu:write8(0x03000EA8,0); emu:write8(0x03000EB1,1)
  emu:write32(0x03000EB8,${script + 0x08000000})
 end
 if f==2320 then emu:screenshot(${JSON.stringify(path.join(temp, 'dialogue.png'))}) end
end)
`);
  const child = spawn(process.env.MGBA_PATH ?? '/opt/homebrew/opt/mgba/bin/mGBA', [
    '-C', 'mute=1', '-C', 'videoDriver=1', '-C', 'fpsTarget=1000',
    '-C', 'audioSync=0', '-C', 'videoSync=0',
    ...['savegamePath', 'savestatePath', 'screenshotPath', 'cheatsPath'].flatMap(key => ['-C', `${key}=${temp}`]),
    '--script', lua, romPath,
  ], { env: { ...process.env, QT_QPA_PLATFORM: 'offscreen' }, stdio: 'ignore' });
  let launchError: Error | undefined;
  child.on('error', error => { launchError = error; });
  try {
    await expect.poll(() => {
      if (launchError) throw launchError;
      if (child.exitCode !== null) throw new Error(`mGBA terminé : ${child.exitCode}`);
      return fs.existsSync(path.join(temp, 'dialogue.png'));
    }, { timeout: 90_000 }).toBe(true);
  } finally {
    child.kill('SIGTERM');
    await new Promise<void>(resolve => {
      if (child.exitCode !== null || child.signalCode !== null || launchError) resolve();
      else child.once('exit', () => resolve());
    });
  }
  const png = PNG.sync.read(fs.readFileSync(path.join(temp, 'dialogue.png')));
  expect([png.width, png.height]).toEqual([240, 160]);
  const widthBase = rom.readUInt32LE(0x6594) - 0x08000000;
  const advance = [...expected.subarray(0, -1)].reduce((sum, code) => sum + rom[widthBase + code], 0);
  // Comparaison du texte réellement rendu aux glyphes natifs 2bpp,
  // indépendamment de la présence de la traduction dans la source.
  const glyphBase = rom.readUInt32LE(0x658c) - 0x08000000;
  // Origine du moteur dans la zone intérieure de la msgbox (marge + décalage vertical).
  let cursor = 16;
  let checkedPixels = 0;
  for (const code of expected.subarray(0, -1)) {
    const width = rom[widthBase + code];
    for (let y = 0; y < 16; y++) for (let x = 0; x < Math.min(width, 8); x++) {
      const offset = glyphBase + code * 64 + (y >> 3) * 32 + (y % 8) * 2;
      const value = rom.readUInt16LE(offset) >> (14 - 2 * x) & 3;
      // 1 = encre de premier plan ; 2 = ombre, 0/3 = transparent.
      if (value === 1) {
        expect(ink(png, cursor + x, 121 + y), `glyphe ${code} pixel ${x},${y}`).toBe(true);
        checkedPixels++;
      }
    }
    cursor += width;
  }
  expect(checkedPixels).toBeGreaterThan(100);
  expect(advance).toBeLessThanOrEqual(192);
  // Pas de texte parasite sur la deuxième ligne ni après la fin du message.
  for (let y = 117; y < 148; y++) for (let x = 15; x < 207; x++) {
    if (y >= 140 || x >= 15 + advance + 2) expect(ink(png, x, y)).toBe(false);
  }
  await page.setContent(`<style>body{margin:0;background:#222;color:white;font:18px sans-serif}figure{margin:12px;width:max-content}img{width:960px;height:640px;image-rendering:pixelated}figcaption{padding:8px}</style><figure><figcaption>PT-04 — 0x26d5bf : Valeu por batalhar comigo! — ROM construite, pointeur vivant</figcaption><img alt="Dialogue PT-04 vérifié dans mGBA" src="data:image/png;base64,${fs.readFileSync(path.join(temp, 'dialogue.png')).toString('base64')}"></figure>`);
  await expect(page.getByRole('img')).toBeVisible();
  const proof = process.env.PT04_PROOF ?? path.join(os.tmpdir(), 'pt04-dialogue-proof.png');
  await page.locator('figure').screenshot({ path: proof });
  console.log(`Preuve : ${proof} ; sondes : ${temp}`);
});
