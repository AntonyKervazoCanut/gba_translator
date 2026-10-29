import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: ['specs/pt23-dialogues.spec.ts'],
  outputDir: '../../test-results/pt23',
  timeout: 360_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true },
});
