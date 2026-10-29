import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './specs',
  testMatch: 'es-maint-fonts.spec.ts',
  outputDir: '/tmp/f850-playwright-results',
  workers: 1,
  timeout: 120_000,
  reporter: 'list',
  use: { headless: true, viewport: { width: 1000, height: 850 } },
});
