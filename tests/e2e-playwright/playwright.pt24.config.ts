import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: ['specs/pt24-dialogue.spec.ts', 'specs/pt24-item.spec.ts'],
  outputDir: '../../test-results/pt24',
  timeout: 360_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true },
});
