import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: '.', testMatch: 'specs/es008-grammar.spec.ts',
  outputDir: '../../test-results/es008-grammar', timeout: 120_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
