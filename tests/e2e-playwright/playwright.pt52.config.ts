import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.', testMatch: 'specs/pt52-pokedex.spec.ts',
  outputDir: '../../test-results/pt52', timeout: 420_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
