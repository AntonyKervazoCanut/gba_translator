import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: ['specs/pt49-items.spec.ts', 'specs/pt49-tm.spec.ts'],
  outputDir: '../../test-results/pt49',
  timeout: 360_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true },
});
