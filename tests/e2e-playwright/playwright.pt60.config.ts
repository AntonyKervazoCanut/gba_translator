import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.', testMatch: 'specs/pt60-scenario.spec.ts',
  outputDir: '../../test-results/pt60', timeout: 360_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
