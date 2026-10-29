import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: 'specs/de-combat-ui-03.spec.ts',
  outputDir: '../../test-results/combat-ui-03',
  timeout: 120_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true },
});
