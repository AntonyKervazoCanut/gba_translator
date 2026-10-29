import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: 'specs/pt04-dialogue.spec.ts',
  outputDir: '../../test-results/pt04',
  timeout: 150_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true },
});
