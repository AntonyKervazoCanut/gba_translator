import { defineConfig } from '@playwright/test';
export default defineConfig({testDir:'./specs',testMatch:/es003-(delivery|cube)\.spec\.ts/,outputDir:'/tmp/f853-final-playwright',workers:1,timeout:300000,reporter:'list',use:{headless:true,viewport:{width:1500,height:2000}}});
