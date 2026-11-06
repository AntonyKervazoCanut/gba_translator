/** F-1049 : lectures finales et mire RAM native, sans sauvegarde ni parcours simulé.
 * Les sept premières lignes de chaque route sont rendues séparément. Toutes les
 * lignes et commandes sont vérifiées ; les traductions finales restent à F-869. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PNG } from 'pngjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
interface Entry {
  key: number; live: number; pointers: number[]; expected_hex: string; target: number;
  layout?: { glyph_widths_hex: string; max_width: number; max_lines: number; max_bytes?: number };
}

function decodeContract(raw: Buffer, widths: Buffer, playerWidth: number, maxLines = 2) {
  const lines = [0];
  const commands: string[] = [];
  let visibleLines = 1;
  for (let i=0;i<raw.length;i++) {
    const value=raw[i];
    if(value===0xff) { expect(i).toBe(raw.length-1); return {lines,commands}; }
    if(value===0xfc) {
      expect(raw[i+1]).toBe(1);
      commands.push(raw.subarray(i,i+3).toString('hex')); i+=2;
    } else if(value===0xfd) {
      expect(raw[i+1]).toBe(1);
      commands.push(raw.subarray(i,i+2).toString('hex')); i++;
      lines[lines.length-1]+=playerWidth;
    } else if(value===0xfe || value===0xfa || value===0xfb) {
      lines.push(0);
      if(value===0xfe) { visibleLines++; expect(visibleLines).toBeLessThanOrEqual(maxLines); }
      if(value===0xfa) commands.push('fa');
      if(value===0xfb) {commands.push('fb');visibleLines=1;}
    } else {
      expect(value).toBeLessThan(0xf7);
      lines[lines.length-1]+=widths[value];
    }
  }
  throw new Error('Terminateur absent');
}

test('ES-019 : 6 routes, quatre alias et métriques moteur après patches', async ({ page }) => {
  const reportPath=path.join(root,'output/reports/es019-routing-probe.json');
  const report=JSON.parse(fs.readFileSync(reportPath,'utf8')) as {rom: string;records: Entry[]};
  expect(report.records).toHaveLength(6);
  const rom=fs.readFileSync(path.resolve(root,report.rom));
  const source=fs.readFileSync(path.join(root,'input/roms/englishrom.gba'));
  const routes=JSON.parse(fs.readFileSync(path.join(root,'docs/analysis/es/019_ROUTES.json'),'utf8')).routes;
  const aliases=report.records;
  for(const row of report.records) {
    const expected=Buffer.from(row.expected_hex,'hex');
    expect(row.pointers.length).toBeGreaterThan(0);
    for(const pointer of row.pointers) {
      const target=rom.readUInt32LE(pointer)-0x8000000;
      expect(target).toBe(row.target);
      expect(target).not.toBe(row.live);
      expect(rom.subarray(target,target+expected.length)).toEqual(expected);
    }
  }
  for(const row of aliases) {
    const route=routes.find((r: {contract_offset:string;offset:string})=>parseInt(r.contract_offset,16)===row.key || parseInt(r.offset,16)===row.key);
    expect(row.layout).toBeDefined();
    const widths=Buffer.from(row.layout!.glyph_widths_hex,'hex');
    expect(widths).toHaveLength(512);
    const actual=Buffer.from(row.expected_hex,'hex');
    const original=Buffer.from(route.snapshot.raw_hex,'hex');
    const checked=decodeContract(actual,widths,84,row.layout!.max_lines);
    expect(checked.commands).toEqual(decodeContract(original,widths,84,row.layout!.max_lines).commands);
    expect(Math.max(...checked.lines)).toBeLessThanOrEqual(row.layout!.max_width);
    expect(actual.length).toBeLessThanOrEqual(row.layout!.max_bytes ?? 512);
    expect(rom.subarray(row.key,row.live)).toEqual(source.subarray(row.key,row.live));
  }
  const temp=fs.mkdtempSync(path.join(os.tmpdir(),'f1049-mgba-'));
  fs.writeFileSync(path.join(temp,'game.gba'),rom);
  execFileSync('python3',['tests/e2e-playwright/fixtures/prepare_es015_routing_probe.py',temp,reportPath,'--all-records'],{cwd:root});
  const log=fs.openSync(path.join(temp,'mgba.log'),'w');
  const child=spawn(process.env.MGBA_PATH ?? '/opt/homebrew/opt/mgba/bin/mGBA',[
    '-C','mute=1','-C','videoDriver=1','-C','fpsTarget=240','-C','audioSync=0','-C','videoSync=0',
    ...['savegamePath','savestatePath','screenshotPath','cheatsPath'].flatMap(key=>['-C',`${key}=${temp}`]),
    '--script',path.join(temp,'probe.lua'),path.join(temp,'game.gba'),
  ],{env:{...process.env,QT_QPA_PLATFORM:'offscreen'},stdio:['ignore',log,log]});
  let launchError: Error | undefined;
  child.on('error',error=>{launchError=error;});
  try {
    await expect.poll(()=>{
      if(launchError)throw launchError;
      if(child.exitCode!==null)throw new Error(fs.readFileSync(path.join(temp,'mgba.log'),'utf8'));
      return fs.existsSync(path.join(temp,'result.json'));
    },{timeout:60_000}).toBe(true);
    const result=JSON.parse(fs.readFileSync(path.join(temp,'result.json'),'utf8')) as {
      observations: {index:number;pointer:number;target:number;raw:string}[];
      renders: {key:number;marker:number;target:number;widths:number[]}[];
    };
    expect(result.observations).toHaveLength(report.records.reduce((n,row)=>n+row.pointers.length,0));
    for(const observation of result.observations) {
      const row=report.records[observation.index];
      expect(row.pointers).toContain(observation.pointer);
      expect(observation.target).toBe(0x8000000+row.target);
      expect(observation.raw).toBe(row.expected_hex);
    }
    expect(result.renders).toHaveLength(6);
    const panels: string[]=[];
    for(const [index,row] of aliases.entries()) {
      const render=result.renders[index];
      expect(render.key).toBe(row.key);
      expect(render.marker).toBe(0x1043);
      expect(render.target).toBe(0x8000000+row.target);
      const metrics=Buffer.from(row.layout!.glyph_widths_hex,'hex');
      // Le vrai StringExpandPlaceholders développe le nom RAM MMMMMMM.
      const checked=decodeContract(Buffer.from(row.expected_hex,'hex'),metrics,7*metrics[0xc7],row.layout!.max_lines);
      expect(render.widths).toEqual(checked.lines);
      const bytes=fs.readFileSync(path.join(temp,`render-${index}.png`));
      const png=PNG.sync.read(bytes);
      expect([png.width,png.height]).toEqual([240,160]);
      let ink=0;
      for(let y=0;y<160;y++)for(let x=0;x<240;x++)if(png.data[(y*240+x)*4]<200)ink++;
      expect(ink,`Rendu natif absent ${row.key.toString(16)}`).toBeGreaterThan(20);
      panels.push(`<figure><figcaption>0x${row.key.toString(16).toUpperCase()} · ${render.widths.length} lignes mesurées</figcaption><img alt="Alias ${row.key.toString(16)} rendu moteur" src="data:image/png;base64,${bytes.toString('base64')}"></figure>`);
    }
    await page.setContent(`<style>body{background:#152334;color:white;font:16px monospace;margin:20px}main{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}figure{margin:0}img{width:100%;image-rendering:pixelated}figcaption{padding:6px 0}</style><h1>ES-019 · acheminement mécanique</h1><p>6 routes vérifiées · 4 alias · 2 clés canoniques · commandes et largeurs natives contrôlées</p><main>${panels.join('')}</main><p>Mire RAM de sentinelles temporaires : sept premières lignes séparées par alias.<br>Qualification linguistique et parcours de jeu réservés à F-869.</p>`);
    await expect(page.getByRole('img')).toHaveCount(6);
    for(const img of await page.getByRole('img').all()) {
      await img.evaluate(async(node:HTMLImageElement)=>node.decode());
      await expect(img).toBeVisible();
    }
    const proof=path.join(os.tmpdir(),'f1049-es019-proof.png');
    expect(fs.readFileSync(path.join(temp,'game.gba'))).toEqual(rom);
    // mGBA crée automatiquement la flash vide ; aucune sauvegarde en jeu.
    for(const name of fs.readdirSync(temp).filter(name=>name.endsWith('.sav'))) {
      const flash=fs.readFileSync(path.join(temp,name));
      expect(flash).toEqual(Buffer.alloc(131072,0xff));
    }
    await page.screenshot({path:proof,fullPage:true});
    console.log(`Preuve après assertions : ${proof}`);
  } finally {
    if(child.exitCode===null)child.kill('SIGTERM');
    await new Promise<void>(resolve=>{
      if(child.exitCode!==null || child.signalCode!==null || launchError)resolve();
      else child.once('exit',()=>resolve());
    });
    fs.closeSync(log);
  }
});
