import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './specs', testMatch: 'es011-aliases.spec.ts',
  outputDir: '/tmp/f1041-playwright-results', workers: 1, timeout: 120_000,
  reporter: 'list', use: { headless: true },
});
