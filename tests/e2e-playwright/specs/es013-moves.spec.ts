/** ES-013 : sonde éphémère du résumé, sans sauvegarde en jeu. */
import { test, expect } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { MgbaBridgeClient } from '../../../emulator-web/src/mgba-bridge.js';


const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');

const normalize = (text: string): string => text.normalize('NFD').replace(/\p{M}/gu, '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();

test('ES-013 : cinq lignes dans le résumé natif', async ({ page }) => {
    const offset = '482874';
    const text = '¡PRUEBA ES 013!\nNiño y pingüino\nPrimera prueba\nSegunda prueba\n¿ÚLTIMA LÍNEA?';
    const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'f1044-moves-'));
    const rom = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-f1044-sentinel.gba'));
    const encode = (value: string): Buffer => execFileSync(process.env.PYTHON ?? 'python3', ['-c',
      'from src.core.text_codec import TextEncoder, SPANISH_GLYPH_CHARS; import sys; sys.stdout.buffer.write(TextEncoder.encode_pokemon(sys.argv[1], strict=True, skip_aliases=SPANISH_GLYPH_CHARS))', value], { cwd: root });
    const name = encode('Pound');
    const description = encode(text);
    expect([...description].filter(byte => byte === 0xfe)).toHaveLength(4);
    const base = rom.readUInt32LE(0x308a4) - 0x08000000;
    expect(base).toBe(0xa40a10);
    expect(rom.subarray(base + 13, base + 13 + name.length)).toEqual(name);
    const contract = JSON.parse(fs.readFileSync(path.join(root, 'tests/unit/fixtures/es013_moves_contract.json'), 'utf8')) as {
      entries: {offset: string; pointer_offsets: number[]; source_hex: string}[];
    };
    expect(contract.entries).toHaveLength(6);
    for (const entry of contract.entries) {
      const targets = entry.pointer_offsets.map(ref => rom.readUInt32LE(ref) - 0x08000000);
      expect(targets).toHaveLength(3);
      expect(new Set(targets).size, `miroirs et table active ${entry.offset}`).toBe(1);
      expect(targets[0]).toBeGreaterThanOrEqual(0);
      expect(targets[0]).toBeLessThan(rom.length);
      const terminator = rom.indexOf(0xff, targets[0]);
      expect(terminator - targets[0]).toBeGreaterThan(0);
      expect(terminator - targets[0]).toBeLessThan(512);
      expect(rom.subarray(targets[0], terminator + 1).toString('hex'), `sentinelle livrée ${entry.offset}`).not.toBe(entry.source_hex);
    }
    const target = rom.readUInt32LE(0x99f198) - 0x08000000;
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
request.recognitionLanguages = ["es-ES", "en-US"]
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
      await page.setContent(`<style>body{margin:0}img{width:960px;height:640px;image-rendering:pixelated}</style><img alt="ES-013 : sonde du résumé ${offset}" src="data:image/png;base64,${fs.readFileSync(shot).toString('base64')}">`);
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
      const proof = path.join(os.tmpdir(), 'f1044-summary-proof.png');
      await page.getByRole('img').screenshot({ path: proof });
      console.log(`Preuve ES-013 : ${proof}`);
    } finally { await client.stop(); }
  });
