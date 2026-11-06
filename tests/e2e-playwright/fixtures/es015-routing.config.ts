import { defineConfig } from '@playwright/test';
import os from 'node:os';
import path from 'node:path';
export default defineConfig({
  testDir: '../specs', testMatch: 'es015-routing.spec.ts', workers: 1,
  timeout: 120_000, reporter: 'list',
  outputDir: path.join(os.tmpdir(), 'f1043-playwright-results'),
  use: { headless: true, browserName: 'chromium', viewport: {width: 1200, height: 900} },
});
