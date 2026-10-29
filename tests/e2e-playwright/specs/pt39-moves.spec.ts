/** PT-39 : moteur du résumé réel, alimenté par les octets livrés dans une copie
 * privée. Le banc substitue le nom Pound et une description PT-39 aux slots
 * de la fixture ; cette association artificielle n'est jamais livrée. */
import { test, expect } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { MgbaBridgeClient } from '../../../emulator-web/src/mgba-bridge.js';
import { normalizePortugueseOcr } from '../helpers/pt17-ocr.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
interface AuditedText { offset: string; portuguese: string; references: number[] }
const normalize = (text: string): string => normalizePortugueseOcr(text).toLowerCase();

// Happy Hour couvre les cinq lignes et Pikachu les descriptions G-Max partagées.
// Vision confond « porca »/« porco » et « Urshifu »/« Urshitu » dans les autres
// échantillons : garder un contrôle OCR exact, sans correction de mots.
for (const offset of ['0xa3e022', '0xa3e0a0', '0xa4021f']) {
  test(`le résumé restitue le nom conservé et la description ${offset}`, async ({ page }) => {
    const audit = JSON.parse(fs.readFileSync(path.join(root, 'languages/pt/data/pt39_audit.json'), 'utf8'));
    const row = (audit.entries as AuditedText[]).find(entry => entry.offset === offset)!;
    const text = row.portuguese.replaceAll('\\n', '\n');
    const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'pt39-moves-'));
    const rom = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-pt.gba'));
    const encode = (value: string): Buffer => execFileSync('python3', ['-c',
      'from src.core.text_codec import TextEncoder; import sys; sys.stdout.buffer.write(TextEncoder.encode_pokemon(sys.argv[1], strict=True))', value], { cwd: root });
    const name = encode('Pound');
    const description = encode(text);
    const base = rom.readUInt32LE(0x308a4) - 0x08000000;
    expect(base).toBe(0xa40a10);
    expect(rom.subarray(base + 13, base + 13 + name.length)).toEqual(name);
    const target = rom.readUInt32LE(row.references[0]) - 0x08000000;
    expect(rom.subarray(target, target + description.length)).toEqual(description);
    // Les pointeurs et les noms de la copie de test sont remplacés uniquement
    // après vérification exacte de leurs octets dans la ROM réellement bâtie.
    for (let id = 1; id < 894; id++) {
      name.copy(rom, base + id * 13);
      rom.writeUInt32LE(target + 0x08000000, 0x99f190 + id * 4);
    }
    const romPath = path.join(temp, 'game.gba');
    fs.writeFileSync(romPath, rom);
    fs.copyFileSync(path.join(root, 'tests/fixtures/saves/party_hp_bar_fr.sav'), path.join(temp, 'game.sav'));
    const swift = path.join(temp, 'ocr.swift');
    fs.writeFileSync(swift, `
import Foundation
import Vision
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.recognitionLanguages = ["pt-BR", "en-US"]
request.usesLanguageCorrection = true
request.customWords = ["Pound", "Urshifu", "G-Max", "Max Guard"]
try VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([request])
print((request.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\\n"))
`);
    const ocr = path.join(temp, 'ocr');
    execFileSync('swiftc', [swift, '-o', ocr], { timeout: 60_000 });
    process.env.QT_QPA_PLATFORM = 'offscreen';
    process.env.MGBA_PATH ??= '/opt/homebrew/opt/mgba/bin/mGBA';
    const client = new MgbaBridgeClient();
    const key = async (value: string, frames = 90): Promise<void> => {
      await client.pressKey(value, 4); await client.advanceFrames(frames);
    };
    const capture = async (label: string): Promise<string> => {
      const shot = path.join(temp, `${label}.png`);
      await client.screenshot(shot);
      await page.setContent(`<style>body{margin:0}img{width:960px;height:640px;image-rendering:pixelated}</style><img alt="PT-39 : sonde du résumé ${offset}" src="data:image/png;base64,${fs.readFileSync(shot).toString('base64')}">`);
      const large = path.join(temp, `${label}-large.png`);
      await page.getByRole('img').screenshot({ path: large });
      return normalize(execFileSync(ocr, [large], { encoding: 'utf8', timeout: 60_000 }));
    };
    try {
      await client.startMgba(romPath);
      await client.advanceFrames(300);
      for (const frames of [60, 60, 120, 120]) await key('A', frames);
      await client.advanceFrames(180);
      expect(Number((await client.getState()).playerX)).toBeGreaterThan(0);
      await key('START');
      await client.saveState(1);
      let found = false;
      for (let candidate = 0; candidate < 4; candidate++) {
        if (candidate) { await client.loadState(1); await client.advanceFrames(20); }
        for (let i = 0; i < candidate; i++) await key('DOWN', 20);
        await key('A', 120); await key('A'); await key('A', 150);
        await key('RIGHT', 120); await key('RIGHT', 120); await key('A', 120);
        const actual = await capture(`candidate-${candidate}`);
        console.log(actual);
        if (actual.includes('pound')) { found = true; break; }
      }
      expect(found, 'nom anglais conservé dans le résumé réel').toBe(true);
      const actual = await capture('verified');
      expect(actual).toContain(normalize(text));
      // Le moteur doit reconstruire intégralement les lignes après navigation.
      await key('B', 120); await key('LEFT', 120); await key('RIGHT', 120); await key('A', 120);
      const returned = await capture('returned');
      expect(returned).toContain('pound');
      expect(returned).toContain(normalize(text));
      const proof = path.join(os.tmpdir(), `pt39-${offset.slice(2)}-proof.png`);
      await page.getByRole('img').screenshot({ path: proof });
      console.log(`Preuve PT-39 : ${proof}`);
    } finally { await client.stop(); }
  });
}
