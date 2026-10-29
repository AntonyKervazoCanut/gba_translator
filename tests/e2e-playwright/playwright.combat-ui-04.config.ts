import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: 'specs/combat-ui-04-de.spec.ts',
  outputDir: '../../test-results/combat-ui-04-de',
  timeout: 300_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true },
});
