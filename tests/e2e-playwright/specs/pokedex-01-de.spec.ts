/** B-686 : lecture des pointeurs finaux et impression native hors écran. */
import { test, expect } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { MgbaBridgeClient } from '../../../emulator-web/src/mgba-bridge.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

test('les espèces et motifs corrigés sont imprimés par mGBA', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'b686-render-'));
  const rom = fs.readFileSync(path.join(root, 'output/roms/GenedRom-de.gba'));
  const cases = [
    { ref: 0x4561f0, text: 'Smoochum-Puppe' },
    { ref: 0x456270, text: 'Duskull-Puppe' },
    { ref: 0x4562b0, text: 'Baltoy-Puppe' },
    { ref: 0x456450, text: 'Sableye-Kissen' },
    { ref: 0x4564d0, text: 'Wasser-Kissen' },
    { ref: 0x455e90, text: 'Donner-Matte' },
  ];
  const script = rom.lastIndexOf(Buffer.alloc(128, 255));
  expect(script).toBeGreaterThan(0x1000000);
  cases.forEach(({ ref }, n) => {
    const pointer = rom.readUInt32LE(ref);
    expect(pointer).toBeGreaterThanOrEqual(0x08000000);
    expect(pointer).toBeLessThan(0x0a000000);
    rom.set([0x0f, 0], script + n * 16);
    rom.writeUInt32LE(pointer, script + n * 16 + 2);
    rom.set([0x09, 6, 2], script + n * 16 + 6);
  });
  const game = path.join(temp, 'game.gba');
  fs.writeFileSync(game, rom);
  fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
  const swift = path.join(temp, 'ocr.swift');
  fs.writeFileSync(swift, `import Foundation
import Vision
let r = VNRecognizeTextRequest()
r.recognitionLevel = .accurate
r.recognitionLanguages = ["de-DE", "en-US"]
r.usesLanguageCorrection = false
try VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([r])
print((r.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\\n"))
`);
  const ocr = path.join(temp, 'ocr');
  execFileSync('swiftc', [swift, '-o', ocr]);
  process.env.QT_QPA_PLATFORM = 'offscreen';
  process.env.MGBA_PATH = '/opt/homebrew/opt/mgba/bin/mGBA';
  const client = new MgbaBridgeClient();
  const pictures: string[] = [];
  try {
    await client.startMgba(game);
    await client.advanceFrames(300);
    for (let n = 0; n < 13; n++) {
      await client.pressKey('A', 4);
      await client.advanceFrames(116);
    }
    expect((await client.readMemory(0x03000ea8, 1))[0]).toBe(2);
    await client.saveState(1);
    for (let n = 0; n < cases.length; n++) {
      await client.loadState(1);
      await client.advanceFrames(10);
      await client.writeMemory(0x03000ea8, Buffer.from([0]));
      await client.writeMemory(0x03000eb1, Buffer.from([1]));
      const pointer = Buffer.alloc(4);
      pointer.writeUInt32LE(0x08000000 + script + n * 16);
      await client.writeMemory(0x03000eb8, pointer);
      await client.advanceFrames(300);
      const shot = path.join(temp, `scene${n}.png`);
      await client.screenshot(shot);
      const src = `data:image/png;base64,${fs.readFileSync(shot).toString('base64')}`;
      pictures.push(`<img alt="Cas ${n + 1}" src="${src}">`);
      await page.setContent(`<style>img{width:720px;height:480px;image-rendering:pixelated}</style>${pictures[n]}`);
      const large = path.join(temp, `large${n}.png`);
      await page.getByRole('img').screenshot({ path: large });
      const text = execFileSync(ocr, [large], { encoding: 'utf8' });
      console.log(cases[n].text, text);
      expect(text).toContain(cases[n].text);
      expect(text).not.toMatch(/LIEBISKUS|TRAUNFUGIL|WAILMER|BANETTE|Filigranmuster|THUNDER/);
    }
  } finally {
    await client.stop();
  }
  await page.setContent(`<style>body{margin:0}main{display:grid;grid-template-columns:repeat(3,720px);width:max-content}img{width:720px;height:480px;image-rendering:pixelated}</style><main>${pictures.join('')}</main>`);
  await expect(page.getByRole('img')).toHaveCount(6);
  await page.getByRole('img').evaluateAll(images => Promise.all(images.map(img => (img as HTMLImageElement).decode())));
  await page.locator('main').screenshot({ path: path.join(os.tmpdir(), 'b686-pokedex-01.png') });
});
