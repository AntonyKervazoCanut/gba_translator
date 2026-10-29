import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './specs', testMatch: 'es001-delivery.spec.ts',
  outputDir: '/tmp/f851-playwright-results', workers: 1, timeout: 1_200_000,
  reporter: 'list', use: { headless: true, viewport: { width: 1500, height: 1000 } },
});
