import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: 'specs/pt10-battle.spec.ts',
  outputDir: '../../test-results/pt10',
  timeout: 180_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true },
});
