import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: '.', testMatch: 'specs/de-structured-combat-ui-03*.spec.ts',
  outputDir: '../../test-results/structured-combat-ui-03',
  timeout: 240_000, workers: 1, retries: 0, reporter: 'list',
  use: { headless: true },
});
