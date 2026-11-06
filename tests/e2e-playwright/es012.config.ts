import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './specs', testMatch: 'es012-translation.spec.ts',
  outputDir: '/tmp/es012-playwright-results', workers: 1, timeout: 600_000,
  reporter: 'list', use: { headless: true },
});
