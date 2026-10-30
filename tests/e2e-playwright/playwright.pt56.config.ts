import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: '.', testMatch: ['specs/pt56-species.spec.ts'],
  outputDir: '../../test-results/pt56', timeout: 180_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
