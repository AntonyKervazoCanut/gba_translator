/** F-758 : vrai boot PT, puis rendu moteur des tildes en intro et dialogue.
 * Les chaînes de sonde et le script msgbox ne vivent que dans une copie temporaire.
 * Les pixels de chaque tilde doivent différer de la base tout en conservant son corps.
 */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PNG } from 'pngjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const slots = [0x60, 0x61, 0x62, 0x63];
const bases = [0xd5, 0xe3, 0xbb, 0xc9];
const spaced = (values: number[]) => values.flatMap((value, i) => i ? [0, value] : [value]);

function mask(png: PNG, x: number, y: number, width: number, height: number, light: boolean): string {
  let result = '';
  for (let dy = 0; dy < height; dy++) for (let dx = 0; dx < width; dx++) {
    const at = ((y + dy) * png.width + x + dx) * 4;
    const value = Math.max(...png.data.subarray(at, at + 3));
    result += (light ? value > 200 : value < 100) ? '1' : '0';
  }
  return result;
}

test('ã õ Ã Õ gardent leur corps et leur tilde dans les deux polices', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'pt-font-'));
  const romPath = path.join(temp, 'game.gba');
  const rom = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-pt.gba'));
  // Chercher les copies vivantes du texte plutôt que supposer l'offset EN original.
  const prefix = Buffer.from(execFileSync('python3', ['-c',
    'from src.core.text_codec import TextEncoder; import sys; sys.stdout.buffer.write(TextEncoder.encode_pokemon("Welcome to Pokémon Unbound!").rstrip(bytes([255])))'], { cwd: root }));
  const intro = Buffer.from([...spaced(slots), 0xfe, 0xfe, ...spaced(bases)]);
  let count = 0;
  for (let at = rom.indexOf(prefix); at >= 0; at = rom.indexOf(prefix, at + prefix.length)) {
    rom.fill(0, at, at + prefix.length);
    intro.copy(rom, at);
    count++;
  }
  expect(count, 'la ROM PT conserve le texte anglais initial hors lots traduits').toBeGreaterThan(0);
  const script = rom.lastIndexOf(Buffer.alloc(256, 255));
  expect(script).toBeGreaterThan(0x1000000);
  rom.set([0x0f, 0], script); // loadpointer 0, texte
  rom.writeUInt32LE(0x08000000 + script + 32, script + 2);
  rom.set([0x09, 6, 2], script + 6); // callstd MSGBOX_DEFAULT ; end
  rom.set([...spaced(slots), 0xfe, ...spaced(bases), 0xff], script + 32);
  fs.writeFileSync(romPath, rom);
  const lua = path.join(temp, 'probe.lua');
  fs.writeFileSync(lua, `
local f=0
callbacks:add('frame', function()
 f=f+1
 if f<=600 and f%120==0 then emu:addKey(0) end
 if f<=604 and f%120==4 then emu:clearKey(0) end
 if f<=600 and f%480==60 then emu:addKey(3) end
 if f<=604 and f%480==64 then emu:clearKey(3) end
 if f==1000 then emu:screenshot(${JSON.stringify(temp)}..'/intro.png') end
 if f==1100 then emu:loadStateFile(${JSON.stringify(path.join(root, 'output/roms/GenedRom-fr.ss2'))}) end
 local phase=f-1099
 if phase>=300 and phase<=1800 and phase%120==0 then emu:addKey(0) end
 if phase>=304 and phase<=1804 and phase%120==4 then emu:clearKey(0) end
 if phase==2020 then
  assert(emu:read8(0x03000EA8)==2, 'Un script est déjà actif')
  emu:write8(0x03000EA8,0); emu:write8(0x03000EB1,1)
  emu:write32(0x03000EB8,${script + 0x08000000})
 end
 if phase==2320 then emu:screenshot(${JSON.stringify(temp)}..'/dialogue.png') end
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
  const views = [
    { name: 'intro', x: 24, y: 16, secondY: 44, advance: 12, light: true },
    { name: 'dialogue', x: 15, y: 117, secondY: 132, advance: 12, light: false },
  ];
  for (const view of views) {
    const png = PNG.sync.read(fs.readFileSync(path.join(temp, `${view.name}.png`)));
    expect([png.width, png.height]).toEqual([240, 160]);
    const glyphs: string[] = [];
    for (let i = 0; i < 4; i++) {
      const x = view.x + i * view.advance;
      const marked = mask(png, x, view.y, 8, 16, view.light);
      const base = mask(png, x, view.secondY, 8, 16, view.light);
      expect(marked, `${view.name} glyphe ${i} non vide`).toContain('1');
      expect(marked, `${view.name} glyphe ${i} porte son accent`).not.toBe(base);
      // Le tilde natif de Ñ/ñ utilise sept colonnes : inclure son extrémité
      // droite, même si l'avance de la lettre de base est de six pixels.
      const accentRow = i < 2 ? 7 : 4;
      expect(mask(png, x, view.y + accentRow, 8, 2, view.light),
        `${view.name} tilde ${i} complet et identique à Ñ/ñ`).toBe('0011001001001100');
      const bodyRow = i < 2 ? 10 : 7;
      expect(marked.slice(8 * bodyRow), `${view.name} corps ${i} intact`).toBe(base.slice(8 * bodyRow));
      glyphs.push(marked);
    }
    expect(new Set(glyphs).size, `${view.name} quatre glyphes distincts`).toBe(4);
  }
  const pictures = views.map(view => `<figure><figcaption>${view.name} — ã õ Ã Õ / a o A O</figcaption><img alt="${view.name}" src="data:image/png;base64,${fs.readFileSync(path.join(temp, `${view.name}.png`)).toString('base64')}"></figure>`);
  await page.setContent(`<style>body{margin:0;background:#222;color:white;font:18px sans-serif}main{display:flex;gap:12px;padding:12px;width:max-content}figure{margin:0}figcaption{padding-bottom:8px}img{width:720px;height:480px;image-rendering:pixelated}</style><main>${pictures.join('')}</main>`);
  await expect(page.getByRole('img')).toHaveCount(2);
  const proof = process.env.PT_FONT_PROOF ?? path.join(os.tmpdir(), 'pt-font-proof.png');
  await page.locator('main').screenshot({ path: proof });
  console.log(`Preuve : ${proof} ; sondes : ${temp}`);
});
