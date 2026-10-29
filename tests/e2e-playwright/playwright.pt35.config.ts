import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.', testMatch: 'specs/pt35-combat.spec.ts',
  outputDir: '../../test-results/pt35', timeout: 240_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
