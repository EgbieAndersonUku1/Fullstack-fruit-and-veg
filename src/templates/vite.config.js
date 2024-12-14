import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    outDir: 'static/dist',  // Output the bundled files into the static/dist directory
    rollupOptions: {
      input: 'src/js/components/faq_bot_frontend.js'  // Entry point for the JS file
    }
  }
});
