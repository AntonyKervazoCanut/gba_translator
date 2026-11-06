/** F-854 : valeurs finales livrées, fenêtre native du Cube.
 * La copie temporaire utilise le Repel de la sauvegarde comme porte d'entrée
 * vers le nom et le pointeur de chaque objet testé. Le texte livré n'est pas réécrit.
 * La copie éphémère expose les consommateurs finaux sans réécrire les textes. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PNG } from 'pngjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

for (const offset of ['0x003D5706', '0x003D5883', '0x003D90D7']) test(`ES-004 ${offset} : description finale dans le Cube`, async ({ page }) => {
  const report = JSON.parse(fs.readFileSync(path.join(root, 'docs/analysis/es/004_TRAITEMENT.json'), 'utf8'));
  const row = report.entries.find((entry: { offset: string }) => entry.offset === offset);
  expect(row).toBeTruthy();
  const sentinel: string = row.value;
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'f854-cube-'));
  const delivered = fs.readFileSync(path.join(root, 'output/roms/GenedRom-es-maint.gba'));
  const expected = execFileSync('python3', ['-c',
    'from src.core.text_codec import TextEncoder, SPANISH_GLYPH_CHARS; import sys; sys.stdout.buffer.write(TextEncoder.encode_pokemon(sys.argv[1], skip_aliases=SPANISH_GLYPH_CHARS))',
    sentinel], { cwd: root });
  const item = 0x876200 + row.item_ids_cfru_base_876200[0] * 44;
  expect(delivered.readUInt32LE(0x9A98C)).toBe(0x08876200);
  const target = delivered.readUInt32LE(item + 20) - 0x08000000;
  expect(delivered.subarray(target, target + expected.length)).toEqual(expected);
  expect([...expected].filter(byte => byte === 0xFE)).toHaveLength(sentinel.split('\n').length - 1);
  expect([...expected]).not.toContain(0xFA);
  expect([...expected]).not.toContain(0xFB);

  // La fixture possède Repel. Seuls son nom et son pointeur description sont
  // adaptés dans la copie éphémère : la vraie chaîne ES-004 reste à sa cible.
  const fixture = 0x876200 + 86 * 44;
  const rom = Buffer.from(delivered);
  delivered.copy(rom, fixture, item, item + 14);
  delivered.copy(rom, fixture + 20, item + 20, item + 24);
  const restored = Buffer.from(rom);
  delivered.copy(restored, fixture, fixture, fixture + 14);
  delivered.copy(restored, fixture + 20, fixture + 20, fixture + 24);
  expect(restored.equals(delivered)).toBe(true);
  fs.writeFileSync(path.join(temp, 'game.gba'), rom);
  const saveFixture = fs.readFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'));
  fs.writeFileSync(path.join(temp, 'game.sav'), saveFixture);
  const lua = path.join(temp, 'probe.lua');
  fs.writeFileSync(lua, `
local f=0
local keys={[2020]=3,[2070]=4,[2100]=4,[2130]=0}
callbacks:add('frame', function()
 f=f+1
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 if keys[f] then emu:addKey(keys[f]) end
 if keys[f-4] then emu:clearKey(keys[f-4]) end
 if f==2450 then emu:screenshot(${JSON.stringify(path.join(temp, 'render.png'))}) end
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
    const capture = path.join(temp, 'render.png');
    await expect.poll(() => {
      if (launchError) throw launchError;
      if (child.exitCode !== null) throw new Error(`mGBA terminé : ${child.exitCode}`);
      return fs.existsSync(capture) && fs.readFileSync(capture).subarray(-12)
        .equals(Buffer.from('0000000049454e44ae426082', 'hex'));
    }, { timeout: 90_000 }).toBe(true);
    const png = fs.readFileSync(capture);
    const dimensions = PNG.sync.read(png);
    expect([dimensions.width, dimensions.height]).toEqual([240, 160]);
    await page.setContent(`<style>body{margin:0}img{width:960px;height:640px;image-rendering:pixelated}</style><img alt="ES-004 : traduction finale du champ description dans le Cube" src="data:image/png;base64,${png.toString('base64')}">`);
    await page.getByRole('img').evaluate(async (image: HTMLImageElement) => image.decode());
    await expect(page.getByRole('img')).toBeVisible();
    const readable = path.join(temp, 'readable.png');
    await page.getByRole('img').screenshot({ path: readable });
    // Origine et interligne de la fenêtre native du Cube. Vérification de
    // chaque pixel d'encre, accents et ponctuation compris, sans OCR.
    const glyphBase = delivered.readUInt32LE(0x658c) - 0x08000000;
    const widthBase = delivered.readUInt32LE(0x6594) - 0x08000000;
    const footprint = new Set<number>();
    let cursor = 40;
    let top = 115;
    let lineCount = 1;
    for (const code of expected.subarray(0, -1)) {
      if (code === 0xFE) {
        expect(cursor - 40).toBeLessThanOrEqual(176);
        cursor = 40; top += 14; lineCount++;
        continue;
      }
      const width = delivered[widthBase + code];
      for (let y = 0; y < 16; y++) for (let x = 0; x < Math.min(width, 8); x++) {
        const at = glyphBase + code * 64 + (y >> 3) * 32 + (y % 8) * 2;
        const value = delivered.readUInt16LE(at) >> (14 - 2 * x) & 3;
        if (value === 1) {
          expect(cursor + x).toBeLessThan(216);
          expect(top + y).toBeLessThan(158);
          footprint.add((top + y) * 240 + cursor + x);
        }
      }
      cursor += width;
    }
    expect(cursor - 40).toBeLessThanOrEqual(176);
    expect(lineCount).toBe(sentinel.split('\n').length);
    expect(lineCount).toBeLessThanOrEqual(3);
    expect(footprint.size).toBeGreaterThan(400);
    // Toute la zone texte est contrôlée : aucun pixel manquant, ajouté ou
    // reporté sur une ligne parasite. L'icône est hors de cette fenêtre.
    for (let y = 115; y < 158; y++) for (let x = 40; x < 216; x++) {
      const at = (y * 240 + x) * 4;
      const ink = dimensions.data[at] > 220 && dimensions.data[at + 1] > 220 && dimensions.data[at + 2] > 220;
      expect(ink, `pixel natif ${x},${y}`).toBe(footprint.has(y * 240 + x));
    }
    expect(fs.readFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'))).toEqual(saveFixture);
    const proof = path.join(os.tmpdir(), `f854-es004-${offset}-proof.png`);
    await page.getByRole('img').screenshot({ path: proof });
    console.log(`Preuve après assertions : ${proof}`);
  } finally {
    child.kill('SIGTERM');
    await new Promise<void>(resolve => {
      if (child.exitCode !== null || child.signalCode !== null || launchError) resolve();
      else child.once('exit', () => resolve());
    });
  }
});
