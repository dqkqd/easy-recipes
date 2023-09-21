import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    specPattern: 'cypress/e2e/**/*.{cy,spec}.{js,jsx,ts,tsx}',
    baseUrl: 'http://localhost:4173'
  },

  component: {
    devServer: {
      framework: 'vue',
      bundler: 'vite'
    }
  },
  viewportWidth: 800,
  viewportHeight: 800,
  retries: {
    runMode: 2,
    openMode: 2
  }
});
