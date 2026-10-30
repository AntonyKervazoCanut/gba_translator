import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: '.', testMatch: ['specs/pt54-species.spec.ts'],
  outputDir: '../../test-results/pt54', timeout: 180_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
