import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: 'specs/dialogues-07-de.spec.ts',
  outputDir: '../../test-results/dialogues-07-de',
  timeout: 240_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true },
});
