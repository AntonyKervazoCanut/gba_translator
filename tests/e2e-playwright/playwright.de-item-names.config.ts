import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: '.', testMatch: 'specs/de-item-names-objets-01.spec.ts',
  outputDir: '../../test-results/de-item-names', timeout: 200_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
