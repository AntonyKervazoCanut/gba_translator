import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './specs', testMatch: 'es013-system.spec.ts',
  outputDir: '/tmp/f1044-system-playwright', workers: 1, timeout: 150_000,
  reporter: 'list', use: { headless: true },
});
