import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: 'specs/cut-master.spec.ts',
  outputDir: '../../test-results/cut-master',
  timeout: 150_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true },
});
