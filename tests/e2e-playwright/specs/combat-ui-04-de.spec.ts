/** B-670: actual summary move window, offscreen mGBA and OCR assertions. */
import { test, expect } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import { MgbaBridgeClient } from '../../../emulator-web/src/mgba-bridge.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

test('les descriptions corrigées tiennent dans la fenêtre réelle des attaques', async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'b670-'));
  const romPath = path.join(temp, 'game.gba');
  fs.copyFileSync(path.join(root, 'output/roms/GenedRom-de.gba'), romPath);
  fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
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
  process.env.QT_QPA_PLATFORM = 'offscreen';
  process.env.MGBA_PATH = '/opt/homebrew/opt/mgba/bin/mGBA';
  const client = new MgbaBridgeClient();
  async function key(name: string, frames = 90) {
    await client.pressKey(name, 4);
    await client.advanceFrames(frames);
  }
  async function capture(label: string): Promise<string> {
    const shot = path.join(temp, `${label}.png`);
    await client.screenshot(shot);
    await page.setContent(`<style>body{margin:0}img{width:720px;height:480px;image-rendering:pixelated}</style><img alt="Descriptions DE dans le résumé Pokémon" src="data:image/png;base64,${fs.readFileSync(shot).toString('base64')}">`);
    const readable = path.join(temp, `${label}-large.png`);
    await page.getByRole('img').screenshot({ path: readable });
    return execFileSync(ocr, [readable], { encoding: 'utf8', timeout: 60_000 });
  }
  try {
    await client.startMgba(romPath);
    await client.advanceFrames(300);
    for (const frames of [60, 60, 120, 120]) await key('A', frames);
    await client.advanceFrames(180);
    const state = await client.getState();
    expect(Number(state.playerX)).toBeGreaterThan(0);
    // CFRU keeps the party substructures decrypted in RAM; only the isolated
    // runtime party is changed, never the battery-save fixture or the ROM.
    const party = Buffer.from(await client.readMemory(0x02024284, 100));
    expect(party.readUInt16LE(0x20)).toBeGreaterThan(0);
    expect(party.readUInt16LE(0x2c)).toBeLessThan(894);
    [603, 726, 746, 857].forEach((move, i) => {
      party.writeUInt16LE(move, 0x2c + 2 * i);
      party[0x34 + i] = 5;
    });
    let checksum = 0;
    for (let i = 0x20; i < 0x50; i += 2) checksum = (checksum + party.readUInt16LE(i)) & 0xffff;
    party.writeUInt16LE(checksum, 0x1c);
    await client.writeMemory(0x02024284, party);
    await key('START');
    await client.saveState(1);
    let found = false;
    for (let candidate = 0; candidate < 4; candidate++) {
      if (candidate) { await client.loadState(1); await client.advanceFrames(20); }
      for (let i = 0; i < candidate; i++) await key('DOWN', 20);
      await key('A', 120); await key('A'); await key('A', 150);
      await key('RIGHT', 120); await key('RIGHT', 120); await key('A', 120);
      const text = await capture(`candidate-${candidate}`);
      console.log(`Candidat ${candidate}: ${text}`);
      if (/Laser/i.test(text)) { found = true; break; }
    }
    expect(found, 'la fenêtre réelle doit afficher la description de Laser Prisme').toBe(true);
    const laser = await capture('laser');
    expect(laser).toMatch(/Prismen/i);
    expect(laser).toMatch(/Runde aus/i); // Last line must remain visible.
    await key('DOWN', 120);
    const gas = await capture('gas');
    expect(gas).toMatch(/Gas/i);
    expect(gas).toMatch(/Ziels auf/i);
    await key('DOWN', 120);
    const axe = await capture('axe');
    expect(axe).toMatch(/Splitter/i);
    expect(axe).toMatch(/Volltreffer/i);
    await key('DOWN', 120);
    const gmax = await capture('gmax');
    expect(gmax).toMatch(/Venusaur/i);
    expect(gmax).toMatch(/Schaden zu/i);
    const proof = process.env.B670_PROOF ?? path.join(os.tmpdir(), 'b670-combat-ui-04.png');
    await page.getByRole('img').screenshot({ path: proof });
    console.log(`Preuve : ${proof}`);
  } finally { await client.stop(); }
});
