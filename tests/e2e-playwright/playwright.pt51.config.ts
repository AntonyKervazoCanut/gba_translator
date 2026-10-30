import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.', testMatch: 'specs/pt51-pokedex.spec.ts',
  outputDir: '../../test-results/pt51', timeout: 240_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
