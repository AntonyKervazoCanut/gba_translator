import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: ['specs/pt46-system.spec.ts'],
  outputDir: '../../test-results/pt46',
  timeout: 360_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true },
});
