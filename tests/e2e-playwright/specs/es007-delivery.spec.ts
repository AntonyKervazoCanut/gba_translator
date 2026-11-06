/** F-857 : octets finaux et impression native ; sonde hors combat, sans sauvegarde. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

type Entry = { decision: string; offset: string; pointer_sites: string[];
  expected_hex: string; final_text: string };
const hash = (bytes: Buffer) => createHash('sha256').update(bytes).digest('hex');
const fcArgs: Record<number, number> = {
  1: 1, 2: 1, 3: 1, 4: 3, 5: 1, 6: 1, 8: 1, 11: 2, 12: 1,
  13: 1, 14: 1, 16: 2, 17: 1, 18: 1, 19: 1, 20: 1, 25: 1,
};

/** Développe les buffers combat dans la seule copie temporaire de la sonde.
 * FA/FB, les commandes FC et leurs arguments sont recopiés intégralement.
 * L'imprimante de scripts ne développe pas les FD du moteur de combat.
 */
function expandBattleBuffers(raw: Buffer): Buffer {
  const output: number[] = [];
  for (let i = 0; i < raw.length;) {
    const code = raw[i];
    if (code === 0xfd) {
      expect(i + 1).toBeLessThan(raw.length);
      output.push(...Array(10).fill(0xd1)); // Dix W, aucun buffer global modifié.
      i += 2;
    } else {
      const size = code === 0xfc ? 2 + (fcArgs[raw[i + 1]] ?? 0)
        : [0xf7, 0xf8, 0xf9].includes(code) ? 2 : 1;
      output.push(...raw.subarray(i, i + size));
      i += size;
    }
  }
  return Buffer.from(output);
}

test('chaque traduction ES-007 est injectée et imprimable par le moteur natif', async ({ page }) => {
  const root = process.cwd();
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'f857-native-'));
  const romPath = path.join(temp, 'game.gba');
  const report = JSON.parse(fs.readFileSync(path.join(root, 'docs/analysis/es/007_TRAITEMENT.json'), 'utf8'));
  const entries: Entry[] = report.entries.filter((e: Entry) => e.decision === 'traduit');
  expect(entries.length).toBeGreaterThan(0);
  const fixture = path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav');
  const fixtureHash = hash(fs.readFileSync(fixture));
  const savePath = path.join(temp, 'game.sav');
  fs.copyFileSync(fixture, savePath);
  const rom = fs.readFileSync(process.env.F857_ROM ?? path.join(root, 'output/roms/GenedRom-es-maint.gba'));
  // Les assertions portent d'abord sur tous les pointeurs de la ROM finale,
  // avant toute modification de la copie temporaire.
  const texts = entries.map(entry => {
    const expected = Buffer.from(entry.expected_hex, 'hex');
    expect(expected[expected.length - 1], entry.offset).toBe(0xff);
    expect(expected.length, entry.offset).toBeLessThanOrEqual(512);
    const targets = entry.pointer_sites.length
      ? entry.pointer_sites.map(site => rom.readUInt32LE(Number(site)) - 0x08000000)
      : [Number(entry.offset)];
    for (const target of targets) {
      expect(target, entry.offset).toBeGreaterThanOrEqual(0);
      expect(target + expected.length, entry.offset).toBeLessThanOrEqual(rom.length);
      expect(rom.subarray(target, target + expected.length), entry.offset).toEqual(expected);
    }
    return expandBattleBuffers(expected);
  });
  // Composition conforme au constructeur prouvé : intensité puis suffixe.
  // Les octets des neuf composants ont été vérifiés ci-dessus dans la ROM.
  const component = (offset: number) => Buffer.from(entries.find(e => Number(e.offset) === offset)!.expected_hex, 'hex');
  for (const [template, strong] of [[0x3fcb5f, false], [0x3fcb5f, true], [0x3fcb8f, false], [0x3fcb8f, true]] as const) {
    const up = template === 0x3fcb5f;
    const modifier = strong ? component(up ? 0x3fcb41 : 0x3fcb50).subarray(0, -1).toString('hex') : '';
    const suffix = component(up ? 0x3fcb4a : 0x3fcb59).subarray(0, -1).toString('hex');
    texts.push(Buffer.from(component(template).toString('hex')
      .replace('fd0f', 'cadddfd5d7dce9').replace('fd00', 'bbe8d5e5e9d9')
      .replace('fd01', modifier + suffix), 'hex'));
  }
  const scriptBase = rom.lastIndexOf(Buffer.alloc(131072, 255));
  expect(scriptBase).toBeGreaterThan(0x1000000);
  let textCursor = scriptBase + texts.length * 9;
  texts.forEach((raw, n) => {
    rom.set([0x0f, 0], scriptBase + n * 9);
    rom.writeUInt32LE(textCursor + 0x08000000, scriptBase + n * 9 + 2);
    rom.set([0x09, 6, 2], scriptBase + n * 9 + 6);
    rom.set(raw, textCursor);
    textCursor += raw.length;
  });
  expect(textCursor).toBeLessThanOrEqual(scriptBase + 131072);
  fs.writeFileSync(romPath, rom);
  const lua = path.join(temp, 'probe.lua');
  fs.writeFileSync(lua, `
local f=0
callbacks:add('frame', function()
 f=f+1
 if f>=300 and f<=1800 and f%120==0 then emu:addKey(0) end
 if f>=304 and f<=1804 and f%120==4 then emu:clearKey(0) end
 local n=math.floor((f-2020)/1200)
 local t=(f-2020)%1200
 if n>=0 and n<${texts.length} then
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
 if f==2020+${texts.length}*1200 then
  assert(emu:read8(0x03000EA8)==2, 'Dernier script encore actif')
  local out=assert(io.open(${JSON.stringify(path.join(temp, 'done'))},'w'))
  out:write('${texts.length}'); out:close()
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
  console.log(`Sonde native ES-007 : ${temp} ; ${texts.length} textes`);
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
  expect(fs.readFileSync(path.join(temp, 'done'), 'utf8')).toBe(String(texts.length));
  for (let n = 0; n < entries.length; n++) {
    const capture = fs.readFileSync(path.join(temp, `page${n}.png`));
    expect(capture.subarray(-12), entries[n].offset).toEqual(Buffer.from('0000000049454e44ae426082', 'hex'));
    expect(capture.length, entries[n].offset).toBeGreaterThan(1000);
  }
  expect(hash(fs.readFileSync(fixture))).toBe(fixtureHash);
  expect(hash(fs.readFileSync(savePath))).toBe(fixtureHash);
  const samples: [number, RegExp][] = [
    [0x3ecaa4, /DESTINO/i], [0x3eed08, /Pueblo Bellin/i],
    [0x3eef12, /Liga Pok.mon/i], [0x3fb70f, /par.lisis/i],
    [0x3fcc74, /supereficaz/i], [0x3fcdb3, /huir/i],
    [-1, /subi[oó]!/i], [-2, /subi[oó] mucho!/i],
    [-3, /baj[oó]!/i], [-4, /baj[oó] mucho!/i],
  ];
  const swift = path.join(temp, 'ocr.swift');
  fs.writeFileSync(swift, `import Foundation\nimport Vision\nlet request = VNRecognizeTextRequest()\nrequest.recognitionLevel = .accurate\nrequest.recognitionLanguages = ["es-ES", "en-US"]\nrequest.usesLanguageCorrection = false\ntry VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([request])\nprint((request.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\\n"))\n`);
  const ocr = path.join(temp, 'ocr');
  execFileSync('swiftc', [swift, '-o', ocr], { timeout: 60_000 });
  const pictures = samples.map(([offset]) => {
    const n = offset < 0 ? entries.length + (-offset - 1) : entries.findIndex(e => Number(e.offset) === offset);
    expect(n).toBeGreaterThanOrEqual(0);
    return `<figure><figcaption>${offset.toString(16)}</figcaption><img alt="${offset.toString(16)}" src="data:image/png;base64,${fs.readFileSync(path.join(temp, `page${n}.png`)).toString('base64')}"></figure>`;
  });
  await page.setContent(`<style>body{margin:0;background:#222;color:white;font:20px sans-serif}main{display:grid;grid-template-columns:repeat(2,720px);gap:8px;padding:8px;width:max-content}figure{margin:0}img{width:720px;height:480px;image-rendering:pixelated}</style><main>${pictures.join('')}</main>`);
  await expect(page.getByRole('img')).toHaveCount(samples.length);
  await page.getByRole('img').evaluateAll(images => Promise.all(images.map(image => (image as HTMLImageElement).decode())));
  for (let n = 0; n < samples.length; n++) {
    const enlarged = path.join(temp, `ocr${n}.png`);
    await page.getByRole('img').nth(n).screenshot({ path: enlarged });
    const text = execFileSync(ocr, [enlarged], { encoding: 'utf8', timeout: 60_000 }).replace(/\s+/g, ' ');
    console.log(samples[n][0].toString(16), text);
    expect(text).toMatch(samples[n][1]);
  }
  const proof = path.join(os.tmpdir(), 'f857-native-proof.png');
  await page.locator('main').screenshot({ path: proof });
  console.log(`Preuve Playwright ES-007 : ${proof}`);
});
