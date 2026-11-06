import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './specs', testMatch: ['es013-moves.spec.ts', 'es013-natures.spec.ts', 'es013-system.spec.ts'],
  outputDir: '/tmp/f1044-playwright-results', workers: 1, timeout: 240_000,
  reporter: 'list', use: { headless: true },
});
