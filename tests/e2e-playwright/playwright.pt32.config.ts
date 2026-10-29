import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.', testMatch: 'specs/pt32-battle-forms.spec.ts',
  outputDir: '../../test-results/pt32', timeout: 240_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
