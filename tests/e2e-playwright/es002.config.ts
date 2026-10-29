import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './specs', testMatch: 'es002.spec.ts',
  outputDir: '/tmp/es002-playwright-results',
  timeout: 600_000, workers: 1, retries: 0, reporter: 'list',
  use: { headless: true },
});
