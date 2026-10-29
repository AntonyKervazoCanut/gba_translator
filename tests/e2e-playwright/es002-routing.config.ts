import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './specs', testMatch: 'es002-routing.spec.ts',
  outputDir: '/tmp/b1032-playwright-results', workers: 1, timeout: 600_000,
  reporter: 'list', use: { headless: true, viewport: { width: 1500, height: 2000 } },
});
