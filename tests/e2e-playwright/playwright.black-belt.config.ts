import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: 'specs/black-belt.spec.ts',
  outputDir: '../../test-results/black-belt',
  timeout: 120_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true },
});
