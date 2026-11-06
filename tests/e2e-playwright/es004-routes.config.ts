import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './specs', testMatch: 'es004-routes.spec.ts',
  outputDir: '/tmp/f1035-playwright-results', workers: 1, timeout: 240_000,
  reporter: 'list', use: { headless: true },
});
