import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.', testMatch: 'specs/pt26-borrius.spec.ts',
  outputDir: '../../test-results/pt26', timeout: 240_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
