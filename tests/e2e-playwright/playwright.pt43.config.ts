import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.', testMatch: 'specs/pt43-combat.spec.ts',
  outputDir: '../../test-results/pt43', timeout: 240_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
