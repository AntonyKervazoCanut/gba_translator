import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

test('B-668 : menus DE encodés, umlauts et affichage réel', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'combat-ui-02-'));
  fs.copyFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-de.gba'), path.join(temp, 'game.gba'));
  fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
  // Les adresses sont les pointeurs EN réellement référents des deux labels.
  // Seul un script de sonde est ajouté à une copie temporaire ; les textes
  // restent ceux de la ROM construite et ne sont jamais réécrits par le test.
  const offsets = JSON.parse(execFileSync('python3', ['-c', `
import json, struct, sys
from pathlib import Path
from src.core.text_codec import TextEncoder
source=Path('input/roms/englishrom.gba').read_bytes()
rom=Path(sys.argv[1]).read_bytes()
positions=[]
for offset, expected in [(0x41DFFC, 'GRÜSSE'), (0x41E023, 'GEFÜHLE')]:
    site=source.index(struct.pack('<I', offset+0x08000000))
    target=struct.unpack_from('<I',rom,site)[0]-0x08000000
    encoded=TextEncoder.encode_pokemon(expected, skip_aliases=frozenset('äöüÄÖÜ'))
    assert rom[target:target+len(encoded)] == encoded, hex(offset)
    positions.append(target)
print(json.dumps(positions))
`, path.join(temp, 'game.gba')], { cwd: root, encoding: 'utf8' })) as number[];
  const testRom = fs.readFileSync(path.join(temp, 'game.gba'));
  const scriptBase = testRom.lastIndexOf(Buffer.alloc(64, 255));
  expect(scriptBase).toBeGreaterThan(0x1000000);
  for (let n = 0; n < 2; n++) {
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
local keys={[4020]=3,[4070]=4,[4100]=4,[4130]=0,[4220]=4,[4350]=0}
callbacks:add('frame', function()
 f=f+1
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 for n=0,1 do
  if f==2020+n*1000 then
   assert(emu:read8(0x03000EA8)==2, 'Un script est déjà actif')
   local script=${scriptBase + 0x08000000}+n*16
   emu:write8(0x03000EA8,0); emu:write8(0x03000EB1,1)
   emu:write32(0x03000EB8,script)
  end
  if f==2320+n*1000 then emu:screenshot(${JSON.stringify(temp)}..'/page'..n..'.png') end

  if f==2370+n*1000 or f==2620+n*1000 then emu:addKey(0) end
  if f==2374+n*1000 or f==2624+n*1000 then emu:clearKey(0) end
 end
 if keys[f] then emu:addKey(keys[f]) end
 if keys[f-4] then emu:clearKey(keys[f-4]) end
 if f==4450 then emu:screenshot(${JSON.stringify(temp)}..'/page2.png') end
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
      return fs.existsSync(path.join(temp, 'page2.png'));
    }, { timeout: 90_000 }).toBe(true);
    child.kill('SIGTERM');
    await new Promise<void>(resolve => child.once('exit', () => resolve()));
    const swift = path.join(temp, 'ocr.swift');
    fs.writeFileSync(swift, `
import Foundation
import Vision
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.recognitionLanguages = ["de-DE", "en-US"]
request.usesLanguageCorrection = false
try VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([request])
print((request.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\\n"))
`);
    const ocr = path.join(temp, 'ocr');
    execFileSync('swiftc', [swift, '-o', ocr], { timeout: 60_000 });
    const pictures = Array.from({ length: 3 }, (_, n) =>
      `<img alt="Étape ${n + 1}" src="data:image/png;base64,${fs.readFileSync(path.join(temp, `page${n}.png`)).toString('base64')}">`);
    await page.setContent(`<style>body{margin:0;background:#222}main{display:grid;grid-template-columns:repeat(2,480px);gap:8px;padding:8px;width:max-content}img{width:480px;height:320px;image-rendering:pixelated}</style><main>${pictures.join('')}</main>`);
    await expect(page.getByRole('img')).toHaveCount(3);
    const texts: string[] = [];
    for (let n = 0; n < 3; n++) {
      const enlarged = path.join(temp, `readable${n}.png`);
      await page.getByRole('img').nth(n).screenshot({ path: enlarged });
      texts.push(execFileSync(ocr, [enlarged], { encoding: 'utf8', timeout: 60_000 }));
    }
    expect(texts[0]).toMatch(/GR[ÜU]SSE/i);
    expect(texts[1]).toMatch(/GEF[ÜU]HLE/i);
    // Le troisième écran est le vrai menu d'action du Cube, ouvert par
    // navigation depuis la sauvegarde, sans substitution du texte affiché.
    expect(texts[2]).toMatch(/\bNutzen\b/i);
    expect(texts.join(' ')).not.toMatch(/GREETINGS|FEELINGS/);
    const proof = path.join(os.tmpdir(), 'combat-ui-02-proof.png');
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
