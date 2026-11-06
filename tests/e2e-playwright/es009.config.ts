import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './specs', testMatch: 'es009-formatted.spec.ts',
  outputDir: '/tmp/f1040-playwright-results', workers: 1, timeout: 240_000,
  reporter: 'list', use: { headless: true },
});
