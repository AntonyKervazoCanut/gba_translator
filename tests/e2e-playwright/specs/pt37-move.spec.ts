/** PT-37 : vraie Boîte CT, description livrée au pointeur objet ; copie temporaire de fiche uniquement. */
import { test, expect } from '@playwright/test';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PNG } from 'pngjs';
import { decodePokemonText } from '../../../emulator-web/src/charmap.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const combined = fs.readFileSync(path.join(root, 'languages/pt/combined_pt.txt'), 'utf8');
const line = combined.split('\n').find(line => line.startsWith('0xa37cb9: '))!;
const cases = [['Ice Beam PT-37', (0x8795bc - 0x876074) / 44,
  line.slice('0xa37cb9: '.length).replaceAll('\\n', '\n')]] as const;
for (const [label, item, description] of cases) {
  test(`${label} affiche sa description complète dans la Boîte CT`, async ({ page }) => {
    const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'pt37-move-'));
    const rom = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-pt.gba'));
    // La sauvegarde possède CT56 : remplacer sa fiche dans une copie
    // temporaire permet de vérifier chaque capacité sans sauvegarder en jeu.
    const itemOffset = 0x876074 + item * 44;
    const pointer = rom.readUInt32LE(itemOffset + 0x14) - 0x08000000;
    expect(decodePokemonText(rom.subarray(pointer, rom.indexOf(0xff, pointer)))).toBe(description);
    rom.copy(rom, 0x879D20, itemOffset, itemOffset + 44);

    fs.writeFileSync(path.join(temp, 'game.gba'), rom);
    fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
    const luaPath = path.join(temp, 'probe.lua');
    fs.writeFileSync(luaPath, `
local f=0
local keys={[2020]=3,[2070]=4,[2100]=4,[2130]=0,[2220]=4,
 [2340]=7,[2370]=7,[2400]=7,[2430]=7,[2470]=0,[2510]=0,[2700]=7,[2800]=6}
callbacks:add('frame', function()
 f=f+1
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 if keys[f] then emu:addKey(keys[f]) end
 if keys[f-4] then emu:clearKey(keys[f-4]) end
 if f==2650 then emu:screenshot(${JSON.stringify(path.join(temp, 'first.png'))}) end
 if f==2760 then emu:screenshot(${JSON.stringify(path.join(temp, 'next.png'))}) end
 if f==2860 then emu:screenshot(${JSON.stringify(path.join(temp, 'final.png'))}) end
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
      const first = path.join(temp, 'first.png');
      {
        const png = PNG.sync.read(fs.readFileSync(first));
        expect([png.width, png.height]).toEqual([240, 160]);
        // Aucun glyphe blanc ne doit toucher le bord droit du panneau.
        const white = (x: number, y: number) => {
          const i = (y * png.width + x) * 4;
          return png.data[i] > 235 && png.data[i + 1] > 235 && png.data[i + 2] > 235;
        };
        for (let y = 102; y < 154; y++) {
          expect(white(238, y), `texte rogné à droite en y=${y}`).toBe(false);
          expect(white(239, y), `texte rogné à droite en y=${y}`).toBe(false);
        }
        // La dernière ligne attendue est effectivement dessinée dans le cadre.
        const lastY = 102 + (description.split('\n').length - 1) * 14;
        let lastLinePixels = 0;
        for (let y = lastY; y < lastY + 10; y++) {
          for (let x = 96; x < 238; x++) if (white(x, y)) lastLinePixels++;
        }
        expect(lastLinePixels).toBeGreaterThan(20);
        // La navigation change bien la description puis restitue le panneau.
        const info = (file: string): Buffer => PNG.sync.read(fs.readFileSync(file)).data.subarray(104 * 240 * 4);
        expect(info(path.join(temp, 'next.png')).equals(info(first))).toBe(false);
        expect(info(final).equals(info(first))).toBe(true);
        // Capture après assertions, agrandie sans interpolation pour la preuve.
        const data = fs.readFileSync(final).toString('base64');
        await page.setContent(`<style>body{margin:0;background:#222}img{width:960px;height:640px;image-rendering:pixelated}</style><img alt="Boîte CT : ${label}" src="data:image/png;base64,${data}">`);
        await expect(page.getByRole('img')).toBeVisible();
        const proof = path.join(os.tmpdir(), `f796-pt37-move.png`);
        await page.getByRole('img').screenshot({ path: proof });
        console.log(`Preuve : ${proof}`);
      }
    } finally {
      child.kill('SIGTERM');
      await new Promise<void>(resolve => {
        if (child.exitCode !== null || launchError) resolve();
        else child.once('exit', () => resolve());
      });
    }
  });
}
