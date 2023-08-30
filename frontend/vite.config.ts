import { fileURLToPath, URL } from 'node:url';

import vue from '@vitejs/plugin-vue';
import { defineConfig } from 'vite';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue({
      template: {
        compilerOptions: {
          nodeTransforms: [
            (node) => {
              if (process.env.NODE_ENV === 'production') {
                if (node.type === 1 /*NodeTypes.ELEMENT*/) {
                  for (let i = 0; i < node.props.length; i++) {
                    const p = node.props[i];
                    if (p && p.type === 6 /*NodeTypes.ATTRIBUTE*/ && p.name === 'data-test') {
                      node.props.splice(i, 1);
                      i--;
                    }
                  }
                }
              }
            }
          ]
        }
      }
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
});
