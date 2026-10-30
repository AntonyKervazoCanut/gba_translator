import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.', testMatch: 'specs/pt58-antisis.spec.ts',
  outputDir: '../../test-results/pt58', timeout: 240_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
