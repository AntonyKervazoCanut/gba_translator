/** PT-74 : menu Missions natif, catégories et objectif réellement livré. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const normalize = (s: string) => s.normalize('NFD').replace(/\p{M}/gu, '').toLowerCase().replace(/[^a-z0-9 ]/g, ' ').replace(/\s+/g, ' ').trim();
test('PT-74 : filtres Missions et objectif de Cinder Volcano sont lisibles', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'pt74-missions-'));
  const rom = fs.readFileSync(process.env.PT74_ROM ?? path.join(root, 'output/roms/GenedRom-pt.gba'));
  const script = rom.lastIndexOf(Buffer.alloc(64, 255));
  expect(script).toBeGreaterThan(0x1000000);
  // Seul le déclencheur change dans une copie temporaire : callnative ouvre
  // le véritable menu, ses fenêtres, ses catégories et ses textes restent livrés.
  rom[script] = 0x23;
  rom.writeUInt32LE(0x09ec0eb5, script + 1);
  rom[script + 5] = 2;
  fs.writeFileSync(path.join(temp, 'game.gba'), rom);
  const save = fs.readFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'));
  fs.writeFileSync(path.join(temp, 'game.sav'), save);
  const lua = path.join(temp, 'probe.lua');
  const done = path.join(temp, 'done');
  fs.writeFileSync(lua, `local f=0
callbacks:add('frame',function()
 f=f+1
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 if f==2020 then
  assert(emu:read8(0x03000EA8)==2, 'Script actif avant sonde')
  emu:write8(0x03000EA8,0); emu:write8(0x03000EB1,1)
  emu:write32(0x03000EB8,${script + 0x08000000})
 end
 if f==2500 then emu:screenshot(${JSON.stringify(path.join(temp, 'all.png'))}) end
 if f==2520 or f==2820 then emu:addKey(8) end
 if f==2524 or f==2824 then emu:clearKey(8) end
 if f==2800 then emu:screenshot(${JSON.stringify(path.join(temp, 'inactive.png'))}) end
 if f==3100 then emu:screenshot(${JSON.stringify(path.join(temp, 'active.png'))}) end
 if f==3120 then local out=io.open(${JSON.stringify(done)},'w');out:write('ok');out:close() end
end)`);
  const child = spawn(process.env.MGBA_PATH ?? '/opt/homebrew/opt/mgba/bin/mGBA', [
    '-C','mute=1','-C','videoDriver=1','-C','fpsTarget=240','-C','audioSync=0','-C','videoSync=0',
    ...['savegamePath','savestatePath','screenshotPath','cheatsPath'].flatMap(k=>['-C',`${k}=${temp}`]),
    '--script',lua,path.join(temp,'game.gba'),
  ], {env:{...process.env,QT_QPA_PLATFORM:'offscreen'},stdio:'ignore'});
  let launchError: Error | undefined;
  child.on('error', e=>{launchError=e;});
  try {
    await expect.poll(()=>{
      if (launchError) throw launchError;
      if (child.exitCode!==null) throw new Error(`mGBA: ${child.exitCode}`);
      return fs.existsSync(done);
    },{timeout:90_000}).toBe(true);
  } finally {
    child.kill('SIGTERM');
    await new Promise<void>(resolve=>{
      if(child.exitCode!==null||child.signalCode!==null||launchError) resolve();
      else child.once('exit',()=>resolve());
    });
  }
  expect(fs.readFileSync(path.join(temp,'game.sav'))).toEqual(save);
  fs.writeFileSync(path.join(temp,'ocr.swift'), `import Foundation
import Vision
let r=VNRecognizeTextRequest()
r.recognitionLevel = .accurate
r.recognitionLanguages=["pt-BR","en-US"]
r.usesLanguageCorrection=false
try VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([r])
print((r.results ?? []).compactMap {$0.topCandidates(1).first?.string}.joined(separator:"\\n"))
`);
  const ocr=path.join(temp,'ocr');
  execFileSync('swiftc',[path.join(temp,'ocr.swift'),'-o',ocr]);
  const pictures: string[]=[];
  for (const name of ['all','inactive','active']) {
    const shot=path.join(temp,`${name}.png`), large=path.join(temp,`${name}-ocr.png`);
    execFileSync('sips',['-z','640','960',shot,'--out',large]);
    const text=normalize([shot,large].map(p=>execFileSync(ocr,[p],{encoding:'utf8'})).join(' '));
    console.log(name,text);
    expect(text).toContain('tipo');
    if(name==='inactive') {
      expect(text).toContain('inativas'); expect(text).toContain('fechar');
    } else {
      expect(text).toContain(name==='all'?'todas':'ativ');
      expect(text).toContain('local');
      expect(text).toContain('cinder volcano');
      expect(text).toContain('salve moltres');
      expect(text).toContain('ativ');
    }
    expect(text).not.toMatch(/all missions|inactive missions|active missions|location|make a beeline|save moltres/);
    pictures.push(`<figure><figcaption>${name}</figcaption><img alt="Missions ${name}" src="data:image/png;base64,${fs.readFileSync(shot).toString('base64')}"></figure>`);
  }
  await page.setContent(`<style>body{margin:0;background:#222;color:white;font:18px sans-serif}main{display:flex;gap:8px;padding:8px;width:max-content}figure{margin:0}img{width:720px;height:480px;image-rendering:pixelated}</style><main>${pictures.join('')}</main>`);
  await expect(page.getByRole('img')).toHaveCount(3);
  await page.getByRole('img').evaluateAll(imgs=>Promise.all(imgs.map(i=>(i as HTMLImageElement).decode())));
  const proof=path.join(os.tmpdir(),'f833-pt74-missions-proof.png');
  await page.locator('main').screenshot({path:proof});
  console.log(`Preuve : ${proof}`);
});
