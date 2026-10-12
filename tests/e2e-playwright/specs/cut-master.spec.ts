/** #198 : les textes de la ROM construite passent par la vraie imprimante mGBA.
 * Un script de test dans une copie temporaire ouvre le dialogue sans déplacer
 * le joueur ni sauvegarder. Playwright vérifie les pixels par OCR, hors écran.
 */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

test('Cimistral affiche Maître Coupe dans le dialogue de son ami', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'cut-master-'));
  fs.copyFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-fr.gba'), path.join(temp, 'game.gba'));
  fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
  const offsets = JSON.parse(execFileSync('python3', ['-c', `
import json, sys, struct
from pathlib import Path
from src.core.text_codec import TextEncoder
rom=Path(sys.argv[1]).read_bytes()
expected=TextEncoder.encode_pokemon("Ne t'en fais pas, mon ami, le\\nMaître Coupe m'a dit que tu").removesuffix(b'\\xff')
position=rom.find(expected)
assert position >= 0, 'Le dialogue corrigé est absent de la ROM construite'
source=Path('input/roms/englishrom.gba').read_bytes()
needle=struct.pack('<I',0x08000000+0x1eea4ed)
sites=[]
site=source.find(needle)
while site>=0:
    sites.append(site)
    site=source.find(needle,site+1)
assert sites, 'Le dialogue anglais doit être référencé par un script'
for site in sites:
    at=struct.unpack_from('<I',rom,site)[0]-0x08000000
    if 0<=at<len(rom) and expected in rom[at:rom.index(b'\\xff',at)+1]:
        break
else:
    raise AssertionError('Aucun pointeur vivant ne mène au dialogue corrigé')
print(json.dumps([position]))
`, path.join(temp, 'game.gba')], { cwd: root, encoding: 'utf8' })) as number[];
  const testRom = fs.readFileSync(path.join(temp, 'game.gba'));
  const scriptBase = testRom.lastIndexOf(Buffer.alloc(64, 255));
  expect(scriptBase).toBeGreaterThan(0x1000000);
  for (let n = 0; n < 1; n++) {
    const at = scriptBase + n * 16;
    expect([...testRom.subarray(at, at + 9)]).toEqual(Array(9).fill(255));
    testRom[at] = 0x0F; testRom[at + 1] = 0;
    testRom.writeUInt32LE(offsets[n] + 0x08000000, at + 2);
    testRom.set([0x09, 6, 2], at + 6);
  }
  fs.writeFileSync(path.join(temp, 'game.gba'), testRom);
  const lua = path.join(temp, 'probe.lua');
  fs.writeFileSync(lua, `
local f=0
callbacks:add('frame', function()
 f=f+1
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 for n=0,0 do
  if f==2020+n*1000 then
   assert(emu:read8(0x03000EA8)==2, 'Un script est déjà actif')
   local script=${scriptBase + 0x08000000}+n*16
   emu:write8(0x03000EA8,0); emu:write8(0x03000EB1,1)
   emu:write32(0x03000EB8,script)
  end
  if f==2600+n*1000 then emu:screenshot(${JSON.stringify(temp)}..'/page'..n..'.png') end
  if f==2370+n*1000 or f==2620+n*1000 then emu:addKey(0) end
  if f==2374+n*1000 or f==2624+n*1000 then emu:clearKey(0) end
 end
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
    await expect.poll(() => {
      if (launchError) throw launchError;
      if (child.exitCode !== null) throw new Error(`mGBA terminé : ${child.exitCode}`);
      return fs.existsSync(path.join(temp, 'page0.png'));
    }, { timeout: 90_000 }).toBe(true);
    child.kill('SIGTERM');
    await new Promise<void>(resolve => child.once('exit', () => resolve()));
    const swift = path.join(temp, 'ocr.swift');
    fs.writeFileSync(swift, `
import Foundation
import Vision
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.recognitionLanguages = ["fr-FR", "en-US"]
request.usesLanguageCorrection = false
try VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([request])
print((request.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\\n"))
`);
    const ocr = path.join(temp, 'ocr');
    execFileSync('swiftc', [swift, '-o', ocr], { timeout: 60_000 });
    const pictures = Array.from({ length: 1 }, (_, n) =>
      `<img alt="Étape ${n + 1}" src="data:image/png;base64,${fs.readFileSync(path.join(temp, `page${n}.png`)).toString('base64')}">`);
    await page.setContent(`<style>body{margin:0;background:#222}main{display:grid;grid-template-columns:480px;gap:8px;padding:8px;width:max-content}img{width:480px;height:320px;image-rendering:pixelated}</style><main>${pictures.join('')}</main>`);
    await expect(page.getByRole('img')).toHaveCount(1);
    const texts: string[] = [];
    for (let n = 0; n < 1; n++) {
      const enlarged = path.join(temp, `readable${n}.png`);
      await page.getByRole('img').nth(n).screenshot({ path: enlarged });
      texts.push(execFileSync(ocr, [enlarged], { encoding: 'utf8', timeout: 60_000 }));
    }
    expect(texts[0]).toContain('Maître Coupe');
    expect(texts[0]).toMatch(/m.a dit que tu\s+venais/);
    expect(texts[0]).not.toMatch(/Cut|Master/);
    const proof = path.join(os.tmpdir(), 'cut-master-proof.png');
    await page.locator('main').screenshot({ path: proof });
    console.log(`Preuve : ${proof}`);
  } finally {
    child.kill('SIGTERM');
    await new Promise<void>(resolve => {
      if (child.exitCode !== null || child.signalCode !== null || launchError) resolve();
      else child.once('exit', () => resolve());
    });
  }
});
