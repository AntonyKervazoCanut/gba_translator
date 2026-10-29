import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: '.', testMatch: ['specs/pt30-items.spec.ts'],
  outputDir: '../../test-results/pt30', timeout: 180_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
