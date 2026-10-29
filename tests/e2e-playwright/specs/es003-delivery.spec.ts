/** B-1016 : vrais pointeurs DE et imprimante native mGBA, sans fenêtre visible. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';


const root = process.cwd();

test('huit textes ES-003 sont imprimés par le moteur natif', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'b1016-dialogues-'));
  const romPath = path.join(temp, 'game.gba');
  fs.copyFileSync(path.join(root, 'output/roms/GenedRom-es-maint.gba'), romPath);
  fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
  const rom = fs.readFileSync(romPath);
  const offsets = [0x23e6d1, ...[0x456eb4, 0x96de68, 0x26d3a8, 0x271c30, 0x876634, 0x3074b2, 0x307535].map(site => {
    const target = rom.readUInt32LE(site) - 0x08000000;
    expect(target).toBeGreaterThan(0);
    expect(target).toBeLessThan(rom.length);
    return target;
  })];
  expect(rom.subarray(offsets[0], offsets[0]+9).equals(Buffer.from('ccd5e2d7dcd9e6e3ff','hex'))).toBe(true);
  expect(rom.subarray(offsets[3], offsets[3]+100).includes(Buffer.from('bbe9e8e3ea6fd500cdbfcd','hex'))).toBe(true);
  const scriptBase = rom.lastIndexOf(Buffer.alloc(128, 255));
  expect(scriptBase).toBeGreaterThan(0x1000000);
  rom.set([0x0f, 0], scriptBase);
  rom.set([0x09, 6, 2], scriptBase + 6);
  // Seule la copie temporaire reçoit les scripts de déclenchement.
  fs.writeFileSync(romPath, rom);
  for (let scene = 0; scene < 8; scene++) {
    fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
    let displayOffset = offsets[scene];
    if (scene >= 6) {
      // FD00 appartient au moteur combat. Pour la seule sonde d'imprimante
      // hors combat, substituer dix glyphes larges dans la copie temporaire.
      // Les octets de production et le FD00 sont contrôlés par le test ROM.
      const raw = rom.subarray(offsets[scene], rom.indexOf(255, offsets[scene]) + 1);
      expect(raw.includes(Buffer.from([0xFD, 0]))).toBe(true);
      const expanded = Buffer.from(raw.toString('hex').replace('fd00', 'd1'.repeat(10)), 'hex');
      displayOffset = scriptBase + 16;
      expect(expanded.length).toBeLessThanOrEqual(112);
      rom.set(expanded, displayOffset);
    }
    rom.writeUInt32LE(displayOffset + 0x08000000, scriptBase + 2);
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
   -- Buffers de la sonde vidés : aucune sauvegarde en jeu.
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
request.recognitionLanguages = ["es-ES", "en-US"]
request.usesLanguageCorrection = false
try VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([request])
print((request.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\\n"))
`);
  const ocr = path.join(temp, 'ocr');
  execFileSync('swiftc', [swift, '-o', ocr], { timeout: 60_000 });
  const pictures = Array.from({ length: 8 }, (_, n) =>
    `<img alt="Texte ES-003 ${n + 1}" src="data:image/png;base64,${fs.readFileSync(path.join(temp, `page${n}.png`)).toString('base64')}">`);
  await page.setContent(`<style>body{margin:0;background:#222}main{display:grid;grid-template-columns:repeat(2,720px);gap:8px;padding:8px;width:max-content}img{width:720px;height:480px;image-rendering:pixelated}</style><main>${pictures.join('')}</main>`);
  await expect(page.getByRole('img')).toHaveCount(8);
  await page.getByRole('img').evaluateAll(images => Promise.all(images.map(image => (image as HTMLImageElement).decode())));
  const texts: string[] = [];
  for (let n = 0; n < 8; n++) {
    const enlarged = path.join(temp, `readable${n}.png`);
    await page.getByRole('img').nth(n).screenshot({ path: enlarged });
    texts.push(execFileSync(ocr, [enlarged], { encoding: 'utf8', timeout: 60_000 }).replace(/\s+/g, ' '));
  }
  console.log(texts);
  expect(texts[0]).toMatch(/Ranchero/i);
  expect(texts[1]).toMatch(/VOLADOR/i);
  expect(texts[2]).toMatch(/supereficaz/i);
  expect(texts[3]).toMatch(/entrada de la/i);
  expect(texts[3]).toContain('SES');
  expect(texts[4]).toMatch(/piedras puntiagudas/i);
  expect(texts[5]).toMatch(/mitad/i);
  expect(texts[6]).toMatch(/piedras puntiagudas/i);
  expect(texts[7]).toMatch(/ha quedado atrapado/i);
  const proof = path.join(os.tmpdir(), 'f853-huit-textes.png');
  await page.locator('main').screenshot({ path: proof });
  console.log(`Preuve : ${proof}`);
});
