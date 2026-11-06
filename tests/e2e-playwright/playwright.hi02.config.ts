import { defineConfig } from '@playwright/test';
import os from 'node:os';
import path from 'node:path';

export default defineConfig({
  testDir: '.',
  testMatch: 'specs/hi02-surfaces.spec.ts',
  outputDir: path.join(os.tmpdir(), 'f694-hi02-playwright'),
  timeout: 420_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true, browserName: 'chromium', viewport: { width: 1500, height: 1000 } },
});
