import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: '.', testMatch: ['specs/pt57-categories.spec.ts'],
  outputDir: '../../test-results/pt57', timeout: 360_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
