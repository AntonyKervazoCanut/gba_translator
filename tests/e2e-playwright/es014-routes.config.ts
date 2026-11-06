import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './specs', testMatch: ['es014-routes.spec.ts', 'es014-cube.spec.ts'],
  outputDir: '/tmp/f1042-playwright-results', workers: 1, timeout: 240_000,
  reporter: 'list', use: { headless: true },
});
