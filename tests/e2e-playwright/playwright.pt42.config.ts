import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.', testMatch: 'specs/pt42-dexnav.spec.ts',
  outputDir: '../../test-results/pt42', timeout: 360_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
