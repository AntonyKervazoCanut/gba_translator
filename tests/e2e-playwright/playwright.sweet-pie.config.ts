import { defineConfig } from '@playwright/test';
export default defineConfig({testDir:'.',testMatch:'specs/sweet-pie-fr.spec.ts',outputDir:'../../test-results/sweet-pie',timeout:150_000,workers:1,retries:0,reporter:'list',use:{headless:true}});
