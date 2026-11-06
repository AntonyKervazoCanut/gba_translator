/** F-1041 : quinze routes actives, lectures finales et sept rendus natifs.
 * Les 42 crédits legacy exclus ne sont pas présentés comme des écrans vivants.
 * Sonde RAM sans sauvegarde. Le mode ES011_PRODUCTION vérifie les textes F-861. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PNG } from 'pngjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
interface RecordEntry {
  key: number; live: number; pointers: number[]; expected_hex: string; target: number;
  layout?: { font: string; font_id?: number; max_width: number; max_lines: number };
}
interface Expectations {
  records: {key: number; commands: number[][]; widths?: number[]}[];
  selected: {index: number; key: number; font: number; pointer: number; widths: number[];
             max_width: number; x: number; y: number}[];
}
interface Result {
  observations: {index: number; pointer: number; target: number; raw: string}[];
  widths: {target: number; width: number; marker: number}[];
}

test('ES-011 : quinze routes actives et sept labels lus par le moteur natif', async ({ page }) => {
  const production = process.env.ES011_PRODUCTION === '1';
  const reportPath = path.join(root, production ? 'output/reports/es011-production-aliases.json' : 'output/reports/es011-alias-probe.json');
  const report = JSON.parse(fs.readFileSync(reportPath, 'utf8')) as {records: RecordEntry[]; rom: string};
  expect(report.records).toHaveLength(15);
  const candidates = JSON.parse(fs.readFileSync(path.join(root, 'docs/analysis/es/011_ROUTES.json'), 'utf8'))
    .aliases_candidates as {contract_offset: string; live_offset: string}[];
  const activeKeys = candidates.slice(0, 15).map(r => parseInt(r.contract_offset, 16));
  expect(report.records.map(r => r.key).sort((a,b) => a-b)).toEqual(activeKeys.sort((a,b) => a-b));
  const rom = fs.readFileSync(path.resolve(root, report.rom));
  const source = fs.readFileSync(path.join(root, 'input/roms/englishrom.gba'));
  for (const entry of report.records) {
    const raw = Buffer.from(entry.expected_hex, 'hex');
    expect(rom.subarray(entry.key, entry.live)).toEqual(source.subarray(entry.key, entry.live));
    expect(source.subarray(entry.key, entry.live)).toEqual(Buffer.alloc(entry.live-entry.key));
    for (const pointer of entry.pointers) {
      const target = rom.readUInt32LE(pointer) - 0x08000000;
      if (!production) expect(target).not.toBe(entry.live);
      expect(rom.subarray(target, target+raw.length)).toEqual(raw);
    }
  }
  // Ces deux LDR racines des crédits lisent la table Unbound, pas la table FRLG.
  for (const pointer of [0xf3f18, 0xf3f78]) {
    expect(source.readUInt32LE(pointer)).toBe(0x09fb0db0);
    expect(rom.readUInt32LE(pointer)).toBe(0x09fb0db0);
  }
  const creditsTable = source.subarray(0x1fb0db0, 0x1fb12d8);
  for (const legacy of candidates.slice(15)) {
    const target = Buffer.alloc(4);
    target.writeUInt32LE(0x08000000 + parseInt(legacy.live_offset,16));
    expect(creditsTable.indexOf(target)).toBe(-1);
  }
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'f1041-es011-'));
  fs.writeFileSync(path.join(temp, 'game.gba'), rom);
  execFileSync('python3', ['tests/e2e-playwright/fixtures/prepare_es011_probe.py', temp, reportPath], {cwd: root});
  const expected = JSON.parse(fs.readFileSync(path.join(temp,'expectations.json'),'utf8')) as Expectations;
  expect(expected.records).toHaveLength(15);
  expect(expected.selected).toHaveLength(7);
  // Le préparateur consomme les commandes avec leurs arguments et les compare
  // aux préimages ROM, puis mesure chaque surface déclarée avec ses métriques.
  expect(expected.records.find(r=>r.key===0x41cea7)?.commands).toContainEqual([0xfc,0x0b,1,1]);
  expect(expected.records.find(r=>r.key===0x41d042)?.commands).toContainEqual([0xfd,2]);
  const log = fs.openSync(path.join(temp,'mgba.log'),'w');
  const child = spawn(process.env.MGBA_PATH ?? '/opt/homebrew/opt/mgba/bin/mGBA', [
    '-C','mute=1','-C','videoDriver=1','-C','fpsTarget=240','-C','audioSync=0','-C','videoSync=0',
    ...['savegamePath','savestatePath','screenshotPath','cheatsPath'].flatMap(key=>['-C',`${key}=${temp}`]),
    '--script',path.join(temp,'probe.lua'),path.join(temp,'game.gba'),
  ], {env:{...process.env,QT_QPA_PLATFORM:'offscreen'},stdio:['ignore',log,log]});
  let launchError: Error | undefined;
  child.on('error',error=>{launchError=error;});
  try {
    await expect.poll(()=>{
      if(launchError)throw launchError;
      if(child.exitCode!==null)throw new Error(fs.readFileSync(path.join(temp,'mgba.log'),'utf8'));
      return fs.existsSync(path.join(temp,'result.json'));
    },{timeout:60_000}).toBe(true);
    const result = JSON.parse(fs.readFileSync(path.join(temp,'result.json'),'utf8')) as Result;
    expect(result.observations).toHaveLength(report.records.reduce((n,r)=>n+r.pointers.length,0));
    for(const observation of result.observations) {
      const entry=report.records[observation.index];
      expect(entry.pointers).toContain(observation.pointer);
      expect(observation.raw).toBe(entry.expected_hex);
      expect(observation.target).toBe(rom.readUInt32LE(observation.pointer));
    }
    expect(result.widths).toHaveLength(7);
    const images: string[]=[];
    for(const [index,entry] of expected.selected.entries()) {
      const measured=result.widths[index];
      expect(measured.marker).toBe(0x1041);
      expect(measured.target).toBe(rom.readUInt32LE(entry.pointer));
      expect(measured.width).toBe(Math.max(...entry.widths));
      expect(measured.width).toBeLessThanOrEqual(entry.max_width);
      const pngBytes=fs.readFileSync(path.join(temp,`render-${index}.png`));
      const png=PNG.sync.read(pngBytes);
      expect([png.width,png.height]).toEqual([240,160]);
      let ink=0;
      for(let y=0;y<160;y++)for(let x=0;x<240;x++) {
        if(png.data[(y*240+x)*4]>=200)continue;
        ink++;
        expect(x).toBeGreaterThanOrEqual(entry.x);
        expect(x).toBeLessThanOrEqual(entry.x+measured.width);
        expect(y).toBeGreaterThanOrEqual(entry.y);
        expect(y).toBeLessThan(entry.y+16);
      }
      expect(ink,`texte non rendu à ${entry.key.toString(16)}`).toBeGreaterThan(15);
      images.push(`<figure><figcaption>0x${entry.key.toString(16).toUpperCase()} · police ${entry.font} · ${measured.width}/${entry.max_width} px</figcaption><img alt="Rendu moteur ${entry.key.toString(16)}" src="data:image/png;base64,${pngBytes.toString('base64')}"></figure>`);
    }
    await page.setContent(`<style>body{margin:16px;background:#152334;color:white;font:16px monospace}main{display:grid;grid-template-columns:repeat(2,480px);gap:12px}figure{margin:0}img{width:480px;height:320px;image-rendering:pixelated}figcaption{padding:8px}</style><h1>ES-011 · ${production ? 'traductions finales' : 'routage temporaire'} vérifié</h1><p>15 routes actives · ${result.observations.length} lecteurs exacts · sept rendus moteur</p><p>42 crédits legacy exclus : les crédits actuels utilisent la table 0x1FB0DB0.</p><main>${images.join('')}</main><p>Mire native RAM ; aucune sauvegarde. ${production ? 'Textes de production F-861 ; parcours naturels non certifiés.' : 'Traductions finales réservées à F-861.'}</p>`);
    await expect(page.getByRole('img')).toHaveCount(7);
    for(const image of await page.getByRole('img').all()) {
      await image.evaluate(async (element: HTMLImageElement)=>element.decode());
      await expect(image).toBeVisible();
    }
    const proof=path.join(os.tmpdir(),production ? 'f861-es011-alias-proof.png' : 'f1041-es011-proof.png');
    await page.screenshot({path:proof,fullPage:true});
    console.log(`Preuve après assertions : ${proof}`);
  } finally {
    if(child.exitCode===null)child.kill('SIGTERM');
    await new Promise<void>(resolve=>{
      if(child.exitCode!==null||child.signalCode!==null||launchError)resolve();
      else child.once('exit',()=>resolve());
    });
    fs.closeSync(log);
  }
});
