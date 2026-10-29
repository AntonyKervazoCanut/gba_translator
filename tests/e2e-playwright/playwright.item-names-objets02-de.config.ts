import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: '.', testMatch: 'specs/de-item-names-objets02.spec.ts',
  outputDir: '/tmp/b1027-playwright-results', timeout: 120_000,
  workers: 1, retries: 0, reporter: 'list', use: { headless: true },
});
