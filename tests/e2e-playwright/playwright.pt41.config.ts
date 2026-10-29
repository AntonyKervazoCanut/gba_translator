import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: '.', testMatch: ['specs/pt41-move-name.spec.ts'],
  outputDir: '../../test-results/pt41', timeout: 180_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
