import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.', testMatch: 'specs/pt86-dialogues.spec.ts',
  outputDir: '../../test-results/pt86', timeout: 240_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
