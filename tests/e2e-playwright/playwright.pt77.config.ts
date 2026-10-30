import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.', testMatch: 'specs/pt77-scenario.spec.ts',
  outputDir: '../../test-results/pt77', timeout: 240_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
