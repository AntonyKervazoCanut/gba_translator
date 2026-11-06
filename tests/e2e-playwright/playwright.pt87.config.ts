import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.', testMatch: 'specs/pt87-scenario.spec.ts',
  outputDir: '../../test-results/pt87', timeout: 240_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
