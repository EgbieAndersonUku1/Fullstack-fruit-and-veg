import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    outDir: 'static/dist',  
    rollupOptions: {
      input: 'static/js/components/faq_bot_frontend.js'  //  entry point for JS
    }
  }
});