import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: '.', testMatch: 'specs/pokedex-01-de.spec.ts',
  outputDir: '../../test-results/pokedex-01-de', timeout: 240_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
