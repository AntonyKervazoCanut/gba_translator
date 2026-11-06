import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './specs', testMatch: ['es004-delivery.spec.ts', 'es004-words.spec.ts'],
  outputDir: '/tmp/f854-playwright-results', workers: 1, timeout: 240_000,
  reporter: 'list', use: { headless: true },
});
