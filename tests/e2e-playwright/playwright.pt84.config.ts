import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.', testMatch: 'specs/pt84-dialogues.spec.ts',
  outputDir: '../../test-results/pt84', timeout: 240_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
