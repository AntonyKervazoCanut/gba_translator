/** Vérification des véritables décompresseurs GBA, sans serveur ni sauvegarde. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

test('es-maint : cinq polices moteur et quatre jeux de badges', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'f850-emulator-'));
  const rom = fs.readFileSync('output/roms/GenedRom-es-maint.gba');
  fs.writeFileSync(path.join(temp, 'game.gba'), rom);
  execFileSync('python3', ['scripts/prepare_es_font_probe.py', temp]);
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
    expect(JSON.parse(fs.readFileSync(path.join(temp, 'result.json'), 'utf8')).marker).toBe(0x850);
    const png = fs.readFileSync(path.join(temp, 'render.png'));
    await page.setContent(`<style>body{font:18px monospace;background:#17202b;color:white}img{width:960px;image-rendering:pixelated}p{margin:12px}</style>
      <p>ES maintenu — áéíóúüñ ÁÉÍÓÚÜÑ ¡¿</p>
      <p>5 polices moteur GBA ; 4 blocs de badges ENV PAR DOR CON QUE · DEB — version ES.2.1.0</p>
      <img alt="Rendu mGBA ES" src="data:image/png;base64,${png.toString('base64')}">
      <canvas hidden width="240" height="160"></canvas>`);
    await page.getByRole('img').evaluate(async (img: HTMLImageElement) => { await img.decode(); });
    const pixels = await page.evaluate(() => {
      const c = document.querySelector('canvas')!;
      const ctx = c.getContext('2d')!;
      ctx.drawImage(document.querySelector('img')!, 0, 0);
      return Array.from(ctx.getImageData(0, 0, 240, 160).data);
    });
    const ink = (x: number, y: number) => pixels[(y * 240 + x) * 4] < 200;
    const cps = [0x17,0x1b,0x6f,0x23,0x27,0xf6,0x29,0x02,0x06,0x5a,0x0e,0x12,0xf3,0x14,0x52,0x51];
    // Adresses/strides tirés des cinq fonctions 08006448…080067EC, pas de l'encodeur.
    const fonts = [[0x1eaf00,32],[0x1f3100,64],[0x1ff300,64],[0x20f618,64],[0x21f930,64]];
    for (const [font, [base, stride]] of fonts.entries()) {
      for (const [n, cp] of cps.entries()) {
        let count = 0;
        for (let y=0;y<16;y++) for(let x=0;x<8;x++) {
          const offset = base + cp*stride + (stride===32 ? y*2 : (y>>3)*32+(y%8)*2);
          const raw = rom.readUInt16LE(offset);
          const value = raw >> (14-2*x) & 3;
          const expected = value===1 || value===2;
          expect(ink(4+n*14+x,4+font*18+y), `police ${font}, octet ${cp.toString(16)}, pixel ${x},${y}`).toBe(expected);
          if(expected)count++;
        }
        expect(count).toBeGreaterThan(2);
      }
    }
    // Motifs indépendants : première ligne de chacun des six libellés officiels.
    const tops: Record<number,string> = {0:'111110011001',1:'111001101110',2:'111001101110',3:'011101101001',4:'011010011111',6:'111011111110'};
    for(let block=0;block<4;block++)for(const [slot, top] of Object.entries(tops)) {
      for(let letter=0;letter<3;letter++)for(let x=0;x<4;x++) {
        expect(ink(4+Number(slot)*33+8+1+letter*5+x,96+block*10+1)).toBe(top[letter*4+x]==='1');
      }
    }
    const sGlyph = ['0111','1000','0110','0001','1110'];
    for(let y=0;y<5;y++)for(let x=0;x<4;x++) {
      expect(ink(108+x,145+y), `préfixe ES : pixel S ${x},${y}`).toBe(sGlyph[y][x]==='1');
    }
    await expect(page.getByRole('img', { name: 'Rendu mGBA ES' })).toBeVisible();
    await page.screenshot({ path: path.join(os.tmpdir(), 'f850-es-maint-polices-statuts.png') });
  } finally {
    if(child.exitCode===null)child.kill('SIGTERM');
    fs.closeSync(log);
  }
});
