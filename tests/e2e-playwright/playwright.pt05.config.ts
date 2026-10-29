import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: 'specs/pt05-items.spec.ts',
  outputDir: '../../test-results/pt05',
  timeout: 150_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true },
});
