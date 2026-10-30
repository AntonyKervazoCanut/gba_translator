import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.', testMatch: 'specs/pt55-species.spec.ts',
  outputDir: '../../test-results/pt55', timeout: 240_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
