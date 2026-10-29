import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: 'specs/pt15-system.spec.ts',
  outputDir: '../../test-results/pt15',
  timeout: 360_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true },
});
