import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: 'specs/mom-cube.spec.ts',
  outputDir: '../../test-results/mom-cube',
  timeout: 150_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true },
});
