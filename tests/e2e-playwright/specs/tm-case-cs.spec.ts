/** #189 : rendu réel de la Boîte CT par mGBA Qt hors écran.
 * La sauvegarde de référence possède CT56 et CT86, mais aucune CS. Dans une
 * copie temporaire de la ROM seulement, CT56 reçoit la fiche CS01 existante.
 * Le moteur dessine donc lui-même Coupe et son sigle, sans sauvegarde en jeu.
 */
import { test, expect } from '@playwright/test';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PNG } from 'pngjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const letters = ['.##....###', '#..#..#...', '#......##.', '#........#', '#..#.....#', '.##...###.'];

function badge(file: string): string[] {
  const png = PNG.sync.read(fs.readFileSync(file));
  expect([png.width, png.height]).toEqual([240, 160]);
  return Array.from({ length: 6 }, (_, y) =>
    Array.from({ length: 10 }, (_, x) => {
      const i = ((y + 13) * png.width + x + 123) * 4;
      return png.data[i] > png.data[i + 1] && png.data[i + 1] > png.data[i + 2] ? '#' : '.';
    }).join(''));
}

for (const original of [false, true]) {
  test(original ? 'le bitmap HM original échoue à l’oracle CS' : 'CS reste lisible après navigation dans la Boîte CT', async ({ page }) => {
    const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'tm-case-cs-'));
    const rom = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-fr.gba'));
    // La fiche entière conserve les propriétés cohérentes d’une vraie CS.
    rom.copy(rom, 0x879D20, 0x87AD1C, 0x87AD1C + 44);
    if (original) fs.readFileSync(path.join(root, 'tests/unit/fixtures/tm_case/hm.4bpp')).copy(rom, 0xE99118);
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
      if (original) {
        expect(badge(first)).not.toEqual(letters);
        expect(badge(final)).not.toEqual(letters);
      } else {
        expect(badge(first)).toEqual(letters);
        expect(badge(final)).toEqual(letters);
        // Le panneau inférieur est statique : les animations des Pokémon ne
        // peuvent pas faire passer la vérification de navigation à tort.
        const info = (file: string): Buffer => PNG.sync.read(fs.readFileSync(file)).data.subarray(104 * 240 * 4);
        expect(info(path.join(temp, 'next.png')).equals(info(first))).toBe(false);
        expect(info(final).equals(info(first))).toBe(true);
        // Capture après assertions, agrandie sans interpolation pour la preuve.
        const data = fs.readFileSync(final).toString('base64');
        await page.setContent(`<style>body{margin:0;background:#222}img{width:960px;height:640px;image-rendering:pixelated}</style><img alt="Boîte CT : CS No1 Coupe" src="data:image/png;base64,${data}">`);
        await expect(page.getByRole('img')).toBeVisible();
        const proof = process.env.TM_CASE_PROOF ?? path.join(os.tmpdir(), 'tm-case-cs-proof.png');
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
