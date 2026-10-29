import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.', testMatch: 'specs/pt33-borrius.spec.ts',
  outputDir: '../../test-results/pt33', timeout: 360_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
