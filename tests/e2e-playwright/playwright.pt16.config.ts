import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.', testMatch: 'specs/pt16-pokedex.spec.ts',
  outputDir: '../../test-results/pt16', timeout: 240_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
