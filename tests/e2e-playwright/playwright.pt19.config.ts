import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: ['specs/pt19-system.spec.ts', 'specs/pt19-move.spec.ts'],
  outputDir: '../../test-results/pt19',
  timeout: 360_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true },
});
