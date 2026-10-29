import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './specs', testMatch: 'item-description-routes.spec.ts',
  outputDir: '/tmp/b1031-playwright-results', workers: 1, timeout: 120_000,
  reporter: 'list', use: { headless: true },
});
