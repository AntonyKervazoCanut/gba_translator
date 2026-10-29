/** B-679 : vrais pointeurs DE et imprimante native mGBA, sans fenêtre visible. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

test('les commandes et noms corrigés sont lisibles dans les dialogues GBA', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'b679-dialogues-'));
  const romPath = path.join(temp, 'game.gba');
  fs.copyFileSync(path.join(root, 'output/roms/GenedRom-de.gba'), romPath);
  fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
  const rom = fs.readFileSync(romPath);
  const offsets = [0x1e56e12, 0x1e69767, 0x1e6bba0, 0x1e77179].map(site => {
    const target = rom.readUInt32LE(site) - 0x08000000;
    expect(target).toBeGreaterThan(0);
    expect(target).toBeLessThan(rom.length);
    return target;
  });
  // Pages Eishieb et Maronbeeren, aux pointeurs réellement injectés.
  offsets[0] = rom.indexOf(0xfb, offsets[0]) + 1;
  for (let page = 0; page < 5; page++) offsets[3] = rom.indexOf(0xfb, offsets[3]) + 1;
  const scriptBase = rom.lastIndexOf(Buffer.alloc(128, 255));
  expect(scriptBase).toBeGreaterThan(0x1000000);
  rom.set([0x0f, 0], scriptBase);
  rom.set([0x09, 6, 2], scriptBase + 6);
  // Seule la copie temporaire reçoit les scripts de déclenchement.
  fs.writeFileSync(romPath, rom);
  for (let scene = 0; scene < 4; scene++) {
    fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
    rom.writeUInt32LE(offsets[scene] + 0x08000000, scriptBase + 2);
    fs.writeFileSync(romPath, rom);
    const lua = path.join(temp, `probe${scene}.lua`);
    fs.writeFileSync(lua, `
local f=0
callbacks:add('frame', function()
 f=f+1
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 for n=${scene},${scene} do
  local start=2020
  if f==start then
   assert(emu:read8(0x03000EA8)==2, 'Un script est déjà actif')
   -- Le maître des capacités prépare normalement ces buffers avant le msgbox.
   for _,address in ipairs({0x02021CD0,0x02021CF0,0x02021D04}) do emu:write8(address,0xFF) end
   emu:write8(0x03000EA8,0); emu:write8(0x03000EB1,1)
   emu:write32(0x03000EB8,${scriptBase + 0x08000000})
  end
  if f==start+300 then emu:screenshot(${JSON.stringify(temp)}..'/page'..n..'.png') end
  for k=0,6 do
   if f==start+380+k*170 then emu:addKey(0) end
   if f==start+384+k*170 then emu:clearKey(0) end
  end

 end
end)
  `);
    const child = spawn(process.env.MGBA_PATH ?? '/opt/homebrew/opt/mgba/bin/mGBA', [
      '-C', 'mute=1', '-C', 'videoDriver=1', '-C', 'fpsTarget=240',
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
        const capture = path.join(temp, `page${scene}.png`);
        if (!fs.existsSync(capture)) return false;
        return fs.readFileSync(capture).subarray(-12).equals(Buffer.from('0000000049454e44ae426082', 'hex'));
      }, { timeout: 120_000 }).toBe(true);
      child.kill('SIGTERM');
      await new Promise<void>(resolve => child.once('exit', () => resolve()));

    } finally {
      child.kill('SIGTERM');
      await new Promise<void>(resolve => {
        if (child.exitCode !== null || child.signalCode !== null || launchError) resolve();
        else child.once('exit', () => resolve());
      });
    }
  }
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
  const pictures = Array.from({ length: 4 }, (_, n) =>
    `<img alt="Dialogue DE ${n + 1}" src="data:image/png;base64,${fs.readFileSync(path.join(temp, `page${n}.png`)).toString('base64')}">`);
  await page.setContent(`<style>body{margin:0;background:#222}main{display:grid;grid-template-columns:repeat(2,720px);gap:8px;padding:8px;width:max-content}img{width:720px;height:480px;image-rendering:pixelated}</style><main>${pictures.join('')}</main>`);
  await expect(page.getByRole('img')).toHaveCount(4);
  await page.getByRole('img').evaluateAll(images => Promise.all(images.map(image => (image as HTMLImageElement).decode())));
  const texts: string[] = [];
  for (let n = 0; n < 4; n++) {
    const enlarged = path.join(temp, `readable${n}.png`);
    await page.getByRole('img').nth(n).screenshot({ path: enlarged });
    texts.push(execFileSync(ocr, [enlarged], { encoding: 'utf8', timeout: 60_000 }));
  }
  console.log(texts);
  expect(texts[0]).toContain('Eishieb');
  expect(texts[1]).toContain('Beulenhelm');
  expect(texts[2]).toMatch(/Glücks.Eier/);
  expect(texts[3]).toContain('Maronbeeren');
  expect(texts.join('\n')).not.toMatch(/Eishand|Furchthelm|Wunder.Eier|Maranga/);
  const proof = path.join(os.tmpdir(), 'b679-dialogues-07.png');
  await page.locator('main').screenshot({ path: proof });
  console.log(`Preuve : ${proof}`);
});
