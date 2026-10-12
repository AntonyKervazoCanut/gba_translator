import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: 'specs/dark-gem.spec.ts',
  outputDir: '../../test-results/dark-gem',
  timeout: 120_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true },
});
