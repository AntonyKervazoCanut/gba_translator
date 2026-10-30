import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: '.', testMatch: ['specs/pt53-species.spec.ts'],
  outputDir: '../../test-results/pt53', timeout: 360_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
