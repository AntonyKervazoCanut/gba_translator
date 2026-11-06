import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: ['specs/hi01-dialogues.spec.ts', 'specs/hi01-battle.spec.ts'],
  outputDir: '../../test-results/hi01',
  timeout: 300_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { headless: true, viewport: { width: 1500, height: 1100 } },
});
