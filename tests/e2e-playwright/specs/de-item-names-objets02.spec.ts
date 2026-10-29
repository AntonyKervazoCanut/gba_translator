/** B-1027 : cellules finales dans le Cube réel et résolution des 104 IDs par bufferitemname. */
import { test, expect } from '@playwright/test';
import { decodePokemonText } from '../helpers/charmap.js';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

const samples = [
  [0x87A0BC, 'Beerentüte'], [0x87AE7C, 'Ultranecr. Z'],
  [0x87B0B8, 'Aerodactylnit'], [0x87BADC, 'Illum.Galette'],
  [0x87C660, 'Feldbesch.'], [0x87CBE0, 'Silberkorken'],
  [0x87CCBC, 'Purpur-Nektar'],
] as const;
for (const [offset, expected] of samples) {
for (const mode of ['cube', 'ramassage'] as const) {
test(`B-1027 : ${mode} rend ${expected}`, async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'b1027-'));
  const rom = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-de.gba'));
  const name = rom.subarray(offset, offset + 14);
  expect(name.indexOf(255)).toBeGreaterThan(0);
  expect(name.indexOf(255)).toBeLessThan(14);
  // La Repousse de la sauvegarde permet d'exercer le rendu du même champ fixe.
  name.copy(rom, 0x876074 + 95 * 44);
  // Le descriptif associé à l'objet garde la capture cohérente.
  rom.copy(rom, 0x876074 + 95 * 44 + 20, offset + 20, offset + 24);
  const entries = JSON.parse(fs.readFileSync(path.join(root, 'docs/analysis/1027_OBJETS_02_RACCORDEMENT_DE.json'), 'utf8')).entries as {offset: string, target: string}[];
  expect(entries).toHaveLength(104);
  const scriptBase = rom.lastIndexOf(Buffer.alloc(104 * 8 + 32, 255));
  expect(scriptBase).toBeGreaterThan(0x1000000);
  const checks = entries.map((entry, n) => {
    const at = Number(entry.offset);
    const id = (at - rom.readUInt32LE(0x9A8D8) + 0x08000000) / 44;
    expect(Number.isInteger(id)).toBe(true);
    rom.set([0x80, 1, id & 255, id >> 8, 2], scriptBase + n * 8);
    const raw = rom.subarray(at, rom.indexOf(255, at) + 1);
    expect(decodePokemonText(raw)).toBe(entry.target);
    return `{${Array.from(raw).join(',')}}`;
  });
  const pickupScript = scriptBase + 104 * 8;
  const itemId = (offset - 0x876200) / 44;
  // Le vrai template de réception, suivi via le pointeur du script de ramassage.
  const template = rom.readUInt32LE(0x1A674A);
  expect(template).toBeGreaterThan(0x08000000);
  expect(template).toBeLessThan(0x08000000 + rom.length);
  rom.set([0x80, 1, itemId & 255, itemId >> 8, 0x0F, 0], pickupScript);
  rom.writeUInt32LE(template, pickupScript + 6);
  rom.set([0x09, 6, 2], pickupScript + 10);
  fs.writeFileSync(path.join(temp, 'game.gba'), rom);
  fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
  const lua = path.join(temp, 'probe.lua');
  fs.writeFileSync(lua, `
local f=0
local checks={${checks.join(',')}}
callbacks:add('frame', function()
 f=f+1
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 if f>=2020 and f<2436 then
  local n=math.floor((f-2020)/4)
  if (f-2020)%4==0 then
   assert(emu:read8(0x03000EA8)==2, 'Script actif')
   emu:write8(0x03000EA8,0); emu:write8(0x03000EB1,1)
   emu:write32(0x03000EB8,${scriptBase + 0x08000000}+n*8)
  elseif (f-2020)%4==3 then
   for i,b in ipairs(checks[n+1]) do
    assert(emu:read8(0x02021CF0+i-1)==b, 'Nom runtime incorrect '..n..' octet '..i)
   end
   if n==103 then local out=io.open(${JSON.stringify(path.join(temp, 'resolved.txt'))},'w'); out:write('104'); out:close() end
  end
 end
 if f==2500 and ${mode === 'ramassage'} then
  emu:write8(0x03000EA8,0); emu:write8(0x03000EB1,1)
  emu:write32(0x03000EB8,${pickupScript + 0x08000000})
 end
 local keys={}
 if ${mode === 'cube'} then keys={[2500]=3,[2550]=4,[2580]=4,[2610]=0} end
 if keys[f] then emu:addKey(keys[f]) end
 if keys[f-4] then emu:clearKey(keys[f-4]) end
 if f==2930 then emu:screenshot(${JSON.stringify(temp)}..'/page0.png') end
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
    expect(fs.readFileSync(path.join(temp, 'resolved.txt'), 'utf8')).toBe('104');
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
    await page.setContent(`<style>body{margin:0}img{width:960px;height:640px;image-rendering:pixelated}</style><img alt="Cube : ${expected}" src="data:image/png;base64,${fs.readFileSync(path.join(temp, 'page0.png')).toString('base64')}">`);
    const readable = path.join(temp, 'readable.png');
    await page.getByRole('img').screenshot({ path: readable });
    const text = execFileSync(ocr, [readable], { encoding: 'utf8', timeout: 60_000 });
    console.log(text);
    // L'OCR varie sur les accents de la police pixel ; les octets sont
    // vérifiés exactement avant le lancement de l'émulateur.
    const normalize = (value: string) => value.normalize('NFD').replace(/\p{M}/gu, '').replace(/ı/g, 'i').replace(/[^a-z0-9]/gi, '').toLowerCase();
    // Confusions OCR constatées sur les captures inspectées : A/R et Z/2.
    // Les octets ROM ET les buffers produits par le moteur restent strictement exacts.
    const visualVariants: Record<string, string[]> = {
      'Aerodactylnit': ['Aerodactylnit', 'Rerodactylnit'],
      'Ultranecr. Z': ['Ultranecr. Z', 'Ultranecr. 2'],
    };
    expect((visualVariants[expected] ?? [expected]).some(value => normalize(text).includes(normalize(value)))).toBe(true);
    if (mode === 'ramassage') expect(text).toContain('erhalten!');
    await page.getByRole('img').screenshot({ path: path.join(os.tmpdir(), `b1027-${mode}-${offset.toString(16)}-proof.png`) });
  } finally {
    child.kill('SIGTERM');
    await new Promise<void>(resolve => {
      if (child.exitCode !== null || child.signalCode !== null || launchError) resolve();
      else child.once('exit', () => resolve());
    });
  }
});

}

}
