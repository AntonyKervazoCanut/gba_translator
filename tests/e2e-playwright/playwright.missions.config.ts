import { defineConfig } from '@playwright/test';
export default defineConfig({testDir:'.',testMatch:'specs/missions-fr.spec.ts',outputDir:'../../test-results/missions',timeout:150_000,workers:1,retries:0,reporter:'list',use:{headless:true}});
