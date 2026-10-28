import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: 'specs/tm-case-descriptions.spec.ts',
  outputDir: '../../test-results/tm-descriptions',
  timeout: 120_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true },
});
