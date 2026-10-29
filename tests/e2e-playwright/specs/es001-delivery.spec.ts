/** Imprimante native sur les textes finaux ES-001 ; aucune sauvegarde en jeu. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

test('les 349 textes de script ES-001 atteignent le rendu natif', async ({ page }) => {
  const root = process.cwd();
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'f851-native-'));
  const romPath = path.join(temp, 'game.gba');
  const report = JSON.parse(fs.readFileSync(path.join(root, 'docs/analysis/es/0851_ES001_TRAITEMENT.json'), 'utf8'));
  // 028780 belongs to the battle-string engine, verified separately in ROM.
  const entries = report.entries.filter((e: {decision: string; offset: string}) =>
    e.decision === 'traduit_depuis_en' && Number(e.offset) !== 0x28780);
  expect(entries).toHaveLength(349);
  const rom = fs.readFileSync(process.env.F851_ROM ?? path.join(root, 'output/roms/GenedRom-es-maint.gba'));
  const scriptBase = rom.lastIndexOf(Buffer.alloc(4096, 255));
  expect(scriptBase).toBeGreaterThan(0x1000000);
  for (let n = 0; n < entries.length; n++) {
    const target = rom.readUInt32LE(Number(entries[n].pointers[0])) - 0x08000000;
    const expected = Buffer.from(entries[n].encoded_hex, 'hex');
    expect(rom.subarray(target, target + expected.length)).toEqual(expected);
    rom.set([0x0f, 0], scriptBase + n * 9);
    rom.writeUInt32LE(target + 0x08000000, scriptBase + n * 9 + 2);
    rom.set([0x09, 6, 2], scriptBase + n * 9 + 6);
  }
  fs.writeFileSync(romPath, rom);
  fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
  const lua = path.join(temp, 'probe.lua');
  fs.writeFileSync(lua, `
local f=0
callbacks:add('frame', function()
 f=f+1
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 local n=math.floor((f-2020)/1200)
 local t=(f-2020)%1200
 if n>=0 and n<349 then
  if t==0 then
   assert(emu:read8(0x03000EA8)==2, 'Script actif avant scene '..n)
   for _,address in ipairs({0x02021CD0,0x02021CF0,0x02021D04}) do emu:write8(address,0xFF) end
   emu:write8(0x03000EA8,0); emu:write8(0x03000EB1,1)
   emu:write32(0x03000EB8,${scriptBase + 0x08000000}+n*9)
  end
  if t==300 then emu:screenshot(${JSON.stringify(temp)}..'/page'..n..'.png') end
  if t==430 then emu:screenshot(${JSON.stringify(temp)}..'/next'..n..'.png') end
  if t>=380 and t<=1160 and (t-380)%60==0 then emu:addKey(0) end
  if t>=384 and t<=1164 and (t-384)%60==0 then emu:clearKey(0) end
 end
 if f==2020+349*1200 then
  assert(emu:read8(0x03000EA8)==2, 'Dernier script encore actif')
  local out=assert(io.open(${JSON.stringify(path.join(temp, 'done'))},'w')); out:write('349'); out:close()
 end
end)
`);
  const log = fs.openSync(path.join(temp, 'mgba.log'), 'w');
  const child = spawn(process.env.MGBA_PATH ?? '/opt/homebrew/opt/mgba/bin/mGBA', [
    '-C', 'mute=1', '-C', 'videoDriver=1', '-C', 'fpsTarget=1000',
    '-C', 'audioSync=0', '-C', 'videoSync=0',
    ...['savegamePath', 'savestatePath', 'screenshotPath', 'cheatsPath'].flatMap(key => ['-C', `${key}=${temp}`]),
    '--script', lua, romPath,
  ], { env: { ...process.env, QT_QPA_PLATFORM: 'offscreen' }, stdio: ['ignore', log, log] });
  let launchError: Error | undefined;
  child.on('error', error => { launchError = error; });
  console.log(`Sonde et captures : ${temp}`);
  try {
    await expect.poll(() => {
      if (launchError) throw launchError;
      if (child.exitCode !== null) throw new Error(`mGBA terminé : ${child.exitCode}`);
      return fs.existsSync(path.join(temp, 'done'));
    }, { timeout: 1_080_000, intervals: [1000] }).toBe(true);
  } finally {
    child.kill('SIGTERM');
    await new Promise<void>(resolve => {
      if (child.exitCode !== null || child.signalCode !== null || launchError) resolve();
      else child.once('exit', () => resolve());
    });
    fs.closeSync(log);
  }
  for (let n = 0; n < entries.length; n++) {
    const capture = fs.readFileSync(path.join(temp, `page${n}.png`));
    expect(capture.subarray(-12)).toEqual(Buffer.from('0000000049454e44ae426082', 'hex'));
    expect(capture.length).toBeGreaterThan(1000);
  }
  const samples: [number, RegExp][] = [
    [0x172482, /peque.a/i], [0x172FC3, /Solo pueden pasar/i],
    [0x17D866, /Labora?torio Pok.mon Log/i], [0x17FF49, /de\s*jar de comprar/i],
    [0x188119, /perlas estaban ah/i], [0x18D43E, /pel.cula en la tele/i],
    [0x18D492, /pel.cula en la tele/i], [0x18D53B, /aviso colgado/i],
    [0x190687, /No s. qu. hacer/i], [0x196A82, /No se lo digas/i],
    [0x196D87, /Me faltan fichas/i], [0x19A5BD, /bajar del monte/i],
    [0x1A2B88, /Recordador de Movimientos/i], [0x1A508A, /qu. PC quieres acceder/i],
  ];
  const swift = path.join(temp, 'ocr.swift');
  fs.writeFileSync(swift, `import Foundation\nimport Vision\nlet request = VNRecognizeTextRequest()\nrequest.recognitionLevel = .accurate\nrequest.recognitionLanguages = ["es-ES", "en-US"]\nrequest.usesLanguageCorrection = false\ntry VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([request])\nprint((request.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\\n"))\n`);
  const ocr = path.join(temp, 'ocr');
  execFileSync('swiftc', [swift, '-o', ocr], { timeout: 60_000 });
  const pictures = samples.map(([offset]) => {
    const n = entries.findIndex((e: {offset: string}) => Number(e.offset) === offset);
    return `<img alt="${offset.toString(16)}" src="data:image/png;base64,${fs.readFileSync(path.join(temp, `page${n}.png`)).toString('base64')}">`;
  });
  await page.setContent(`<style>body{margin:0;background:#222}main{display:grid;grid-template-columns:repeat(2,720px);gap:8px;padding:8px;width:max-content}img{width:720px;height:480px;image-rendering:pixelated}</style><main>${pictures.join('')}</main>`);
  await expect(page.getByRole('img')).toHaveCount(samples.length);
  await page.getByRole('img').evaluateAll(images => Promise.all(images.map(image => (image as HTMLImageElement).decode())));
  for (let n = 0; n < samples.length; n++) {
    const enlarged = path.join(temp, `ocr${n}.png`);
    await page.getByRole('img').nth(n).screenshot({ path: enlarged });
    const text = execFileSync(ocr, [enlarged], { encoding: 'utf8', timeout: 60_000 }).replace(/\s+/g, ' ');
    console.log(samples[n][0].toString(16), text);
    expect(text).toMatch(samples[n][1]);
  }
  // FA and FB must advance beyond their initial page.
  for (const [offset, expectedNext] of [[0x172FC3, /en combate/i], [0x18D43E, /del tren/i], [0x18D53B, /Si tienes dudas/i]] as const) {
    const n = entries.findIndex((e: {offset: string}) => Number(e.offset) === offset);
    expect(fs.readFileSync(path.join(temp, `next${n}.png`))).not.toEqual(fs.readFileSync(path.join(temp, `page${n}.png`)));
    const data = fs.readFileSync(path.join(temp, `next${n}.png`));
    await page.locator('main').evaluate((main, src) => {
      const image = document.createElement('img'); image.src = src; image.alt = 'Page suivante'; main.appendChild(image);
    }, `data:image/png;base64,${data.toString('base64')}`);
    const image = page.getByRole('img').last();
    await image.evaluate(img => (img as HTMLImageElement).decode());
    const enlarged = path.join(temp, `next-ocr-${offset}.png`);
    await image.screenshot({ path: enlarged });
    const text = execFileSync(ocr, [enlarged], { encoding: 'utf8', timeout: 60_000 }).replace(/\s+/g, ' ');
    expect(text).toMatch(expectedNext);
  }
  await page.locator('main').screenshot({ path: path.join(os.tmpdir(), 'f851-native-proof.png') });
});
