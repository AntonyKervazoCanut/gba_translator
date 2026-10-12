import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: 'specs/crateris-story.spec.ts',
  outputDir: '../../test-results/crateris',
  timeout: 240_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true },
});
