import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: ['specs/pt37-system.spec.ts', 'specs/pt37-move.spec.ts'],
  outputDir: '../../test-results/pt37',
  timeout: 360_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true },
});
