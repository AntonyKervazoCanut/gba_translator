import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.', testMatch: 'specs/pt25-borrius.spec.ts',
  outputDir: '../../test-results/pt25', timeout: 240_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
