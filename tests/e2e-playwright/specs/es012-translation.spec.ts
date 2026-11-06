/** ES-012 : métriques et imprimeur natifs, trois lignes simultanées.
 * Sonde RAM de la fonte normale ; aucun parcours naturel de menu revendiqué.
 * Aucun texte, police, pointeur ROM ou fichier de sauvegarde n'est modifié. */
import { test, expect } from '@playwright/test';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const normalize = (s: string): string => s.normalize('NFD').replace(/\p{M}/gu, '').replace(/\s+/g, ' ').trim().toLowerCase();
interface Entry {
  offset: string; decision: string; references: string[]; texte?: string;
  encoded_hex: string; budget_px: number; largeurs_px: number[];
}
interface Measurement { target: number; width: number; lines: number; bytes: number }
interface Result { marker: number; failed_index: number; rows: Measurement[] }

test('ES-012 : 361 budgets moteur et six impressions complètes aux pointeurs finaux', async ({ page }) => {
  const reportPath = path.join(root, 'docs/analysis/es/012_TRAITEMENT.json');
  const report = JSON.parse(fs.readFileSync(reportPath, 'utf8')) as {entries: Entry[]};
  const records = report.entries.filter((entry): entry is Entry & {texte: string} => entry.texte !== undefined);
  expect(records).toHaveLength(361);
  const rom = fs.readFileSync(path.join(root, 'output/roms/GenedRom-es-maint.gba'));
  for (const entry of records) for (const reference of entry.references) {
    const target = rom.readUInt32LE(Number(reference)) - 0x08000000;
    const expected = Buffer.from(entry.encoded_hex, 'hex');
    expect(target).toBeGreaterThanOrEqual(0);
    expect(target + expected.length).toBeLessThanOrEqual(rom.length);
    expect(rom.subarray(target, target + expected.length), entry.offset).toEqual(expected);
  }
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'es012-native-'));
  fs.writeFileSync(path.join(temp, 'game.gba'), rom);
  fs.writeFileSync(path.join(temp, 'ocr.swift'), `import Foundation
import Vision
let r = VNRecognizeTextRequest()
r.recognitionLevel = .accurate
r.recognitionLanguages = ["es-ES", "en-US"]
r.usesLanguageCorrection = false
try VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([r])
print((r.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\\n"))
`);
  const ocr = path.join(temp, 'ocr');
  execFileSync('swiftc', [path.join(temp, 'ocr.swift'), '-o', ocr]);
  const cases = [0, records.findIndex(e => e.decision === 'importe'),
    records.findIndex(e => Math.max(...e.largeurs_px) === 232),
    records.findIndex(e => e.offset === '0x00454284'),
    records.findIndex(e => e.offset === '0x00454966'),
    records.findIndex(e => e.offset === '0x00454D80')];
  expect(new Set(cases).size).toBe(6);
  expect(Math.min(...cases)).toBeGreaterThanOrEqual(0);
  const pictures: string[] = [];
  let measurements: Measurement[] = [];
  for (const [scene, selected] of cases.entries()) {
    const directory = path.join(temp, String(scene));
    fs.mkdirSync(directory);
    execFileSync(process.env.PYTHON ?? 'python3', [
      'tests/e2e-playwright/fixtures/prepare_es012_probe.py', directory, reportPath, String(selected),
    ], {cwd: root});
    const log = fs.openSync(path.join(directory, 'mgba.log'), 'w');
    const child = spawn(process.env.MGBA_PATH ?? '/opt/homebrew/opt/mgba/bin/mGBA', [
      '-C', 'mute=1', '-C', 'videoDriver=1', '-C', 'fpsTarget=240',
      '-C', 'audioSync=0', '-C', 'videoSync=0',
      ...['savegamePath', 'savestatePath', 'screenshotPath', 'cheatsPath'].flatMap(key => ['-C', `${key}=${directory}`]),
      '--script', path.join(directory, 'probe.lua'), path.join(temp, 'game.gba'),
    ], {env: {...process.env, QT_QPA_PLATFORM: 'offscreen'}, stdio: ['ignore', log, log]});
    let launchError: Error | undefined;
    child.on('error', error => { launchError = error; });
    try {
      await expect.poll(() => {
        if (launchError) throw launchError;
        if (child.exitCode !== null) throw new Error(fs.readFileSync(path.join(directory, 'mgba.log'), 'utf8'));
        return fs.existsSync(path.join(directory, 'result.json'));
      }, {timeout: 60_000}).toBe(true);
      const result = JSON.parse(fs.readFileSync(path.join(directory, 'result.json'), 'utf8')) as Result;
      expect(result.marker, `budget natif invalide : index ${result.failed_index}`).toBe(0x862);
      expect(result.rows).toHaveLength(361);
      for (const [index, measured] of result.rows.entries()) {
        const entry = records[index];
        expect(measured.target).toBe(rom.readUInt32LE(Number(entry.references[0])));
        expect(measured.width, entry.offset).toBeLessThanOrEqual(entry.budget_px);
        expect(measured.lines).toBe(entry.texte.split('\n').length);
        expect(measured.bytes).toBe(entry.encoded_hex.length / 2);
      }
      measurements = result.rows;
      const png = fs.readFileSync(path.join(directory, 'render.png'));
      const entry = records[selected];
      const picture = `<figure><figcaption>${entry.offset} · ${entry.budget_px} px · imprimeur natif</figcaption><img alt="${entry.offset}" src="data:image/png;base64,${png.toString('base64')}"></figure>`;
      await page.setContent(`<style>img{width:960px;height:640px;image-rendering:pixelated}</style>${picture}`);
      await page.getByRole('img').evaluate(img => (img as HTMLImageElement).decode());
      const large = path.join(directory, 'large.png');
      await page.getByRole('img').screenshot({path: large});
      const text = normalize(execFileSync(ocr, [large], {encoding: 'utf8'}));
      console.log(entry.offset, text);
      for (const line of entry.texte.split('\n')) expect(text, line).toContain(normalize(line));
      pictures.push(picture);
    } finally {
      if (child.exitCode === null) child.kill('SIGTERM');
      await new Promise<void>(resolve => {
        if (child.exitCode !== null || child.signalCode !== null || launchError) resolve();
        else child.once('exit', () => resolve());
      });
      fs.closeSync(log);
    }
  }
  const measurementPath = path.join(root, 'output/reports/es012-native-widths.json');
  fs.mkdirSync(path.dirname(measurementPath), {recursive: true});
  fs.writeFileSync(measurementPath, JSON.stringify(records.map((entry, n) => ({offset: entry.offset, ...measurements[n]})), null, 2));
  await page.setContent(`<style>body{margin:0;background:#18202a;color:white;font:18px sans-serif}main{display:grid;grid-template-columns:repeat(3,720px);gap:8px;padding:8px;width:max-content}figure{margin:0}img{width:720px;height:480px;image-rendering:pixelated}</style><main>${pictures.join('')}</main>`);
  await expect(page.getByRole('img')).toHaveCount(6);
  await page.getByRole('img').evaluateAll(images => Promise.all(images.map(img => (img as HTMLImageElement).decode())));
  const proof = path.join(os.tmpdir(), 'f862-es012-proof.png');
  await page.locator('main').screenshot({path: proof});
  console.log(`Preuve après assertions : ${proof}`);
});
