import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: 'specs/crateris-sign.spec.ts',
  outputDir: '../../test-results/crateris-sign',
  timeout: 150_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true },
});
