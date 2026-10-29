/** PT-36 : rendu du résumé réel, avec substitution des cellules dans une copie
 * privée. Les noms/descriptions livrés sont copiés dans tous les slots pour
 * ne pas dépendre du talent du Pokémon de la sauvegarde ; aucun effet de combat
 * ni association nom/description de cette sonde n'est livré ou revendiqué. */
import { test, expect } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { MgbaBridgeClient } from '../../../emulator-web/src/mgba-bridge.js';
import { normalizePortugueseOcr } from '../helpers/pt17-ocr.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
// La police inclinée du nom fait confondre S/Z, D/O et u/a à Vision.
// Les octets restent comparés exactement avant toute substitution de cellule.
function distance(a: string, b: string): number {
  let row = Array.from({ length: b.length + 1 }, (_, i) => i);
  for (let i = 0; i < a.length; i++) {
    const next = [i + 1];
    for (let j = 0; j < b.length; j++) next.push(Math.min(next[j] + 1,
      row[j + 1] + 1, row[j] + Number(a[i] !== b[j])));
    row = next;
  }
  return row[b.length];
}
function hasName(text: string, name: string): boolean {
  const expected = normalizePortugueseOcr(name).toLowerCase();
  return (text.match(/[a-z]+/g) ?? []).some(word => {
    if (word.length > expected.length && word.endsWith('l')) word = word.slice(0, -1);
    return word.length >= expected.length && word.length <= expected.length + 1 && distance(word, expected) <= (expected.length > 12 ? 3 : 2);
  });
}
for (const sample of [
  { name: 'Supercrescimento', cell: 0xa367e9, ref: 0x96df40, text: 'Golpes múltiplos acertam 5 vezes.' },
  { name: 'Incêndio', cell: 0xa367fa, ref: 0x96df9c, text: 'Atravessa barreiras e neblina.' },
  { name: 'Dilúvio', cell: 0xa3680b, ref: 0x96df3c, text: 'Mantém equipe acordada.' },
]) {
 test(`le résumé rend ${sample.name} et la description livrée sans débordement`, async ({ page }) => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'pt36-abilities-'));
  const rom = fs.readFileSync(process.env.ROM_PATH ?? path.join(root, 'output/roms/GenedRom-pt.gba'));
  const encode = (text: string): Buffer => execFileSync('python3', ['-c',
    'from src.core.text_codec import TextEncoder; import sys; sys.stdout.buffer.write(TextEncoder.encode_pokemon(sys.argv[1], strict=True))', text], { cwd: root });
  const name = encode(sample.name);
  const description = encode(sample.text);
  expect(rom.subarray(sample.cell, sample.cell + name.length)).toEqual(name);
  const target = rom.readUInt32LE(sample.ref) - 0x08000000;
  expect(rom.subarray(target, target + description.length)).toEqual(description);
  // On conserve les chaînes livrées ; seuls les index du banc de rendu changent.
  for (let id = 0; id < 293; id++) {
    name.copy(rom, 0xa36398 + id * 17);
    rom.writeUInt32LE(target + 0x08000000, 0x96de04 + id * 4);
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
request.customWords = ["Supercrescimento", "Dilúvio", "Incêndio"]
if CommandLine.arguments.count > 2 {
 request.regionOfInterest = CGRect(x: 0, y: 0, width: 1, height: 0.14)
}
try VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([request])
print((request.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\\n"))
`);
  const ocr = path.join(temp, 'ocr');
  execFileSync('swiftc', [swift, '-o', ocr], { timeout: 60_000 });
  process.env.QT_QPA_PLATFORM = 'offscreen';
  process.env.MGBA_PATH ??= '/opt/homebrew/opt/mgba/bin/mGBA';
  const client = new MgbaBridgeClient();
  const key = async (name: string, frames = 90) => {
    await client.pressKey(name, 4); await client.advanceFrames(frames);
  };
  async function capture(label: string): Promise<string> {
    const shot = path.join(temp, `${label}.png`);
    await client.screenshot(shot);
    await page.setContent(`<style>body{margin:0}img{width:960px;height:640px;image-rendering:pixelated}</style><img alt="PT-36 : sonde du résumé ${sample.name}" src="data:image/png;base64,${fs.readFileSync(shot).toString('base64')}">`);
    const large = path.join(temp, `${label}-large.png`);
    await page.getByRole('img').screenshot({ path: large });
    const all = execFileSync(ocr, [large], { encoding: 'utf8', timeout: 60_000 });
    const descriptionOnly = execFileSync(ocr, [large, 'description'], { encoding: 'utf8', timeout: 60_000 });
    return normalizePortugueseOcr(all + '\n' + descriptionOnly).toLowerCase();
  }
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
      await key('A', 120); await key('A'); await key('A', 150); await key('RIGHT', 120);
      const text = await capture(`candidate-${candidate}`);
      console.log(text);
      if (hasName(text, sample.name)) { found = true; break; }
    }
    expect(found, 'nom intégral dans le résumé réel').toBe(true);
    const text = await capture('verified');
    expect(text).toContain(normalizePortugueseOcr(sample.text).toLowerCase());
    // Une navigation aller-retour doit reconstruire le même texte complet.
    await key('RIGHT', 120); await key('LEFT', 120);
    const returned = await capture('returned');
    expect(hasName(returned, sample.name)).toBe(true);
    expect(returned).toContain(normalizePortugueseOcr(sample.text).toLowerCase());
    await page.getByRole('img').screenshot({ path: path.join(os.tmpdir(), `pt36-${sample.cell.toString(16)}-proof.png`) });
  } finally { await client.stop(); }
 });
}
