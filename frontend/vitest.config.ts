import { fileURLToPath } from 'node:url';
import { configDefaults, defineConfig, mergeConfig } from 'vitest/config';
import viteConfig from './vite.config';

export default mergeConfig(
  viteConfig,
  defineConfig({
    test: {
      environment: 'jsdom',
      exclude: [...configDefaults.exclude, 'e2e/*'],
      root: fileURLToPath(new URL('./', import.meta.url)),

      // https://github.com/vuetifyjs/vuetify/issues/14749
      setupFiles: 'vuetify.config.ts',
      server: {
        deps: {
          inline: ['vuetify']
        }
      },
      globals: true
    }
  })
);
