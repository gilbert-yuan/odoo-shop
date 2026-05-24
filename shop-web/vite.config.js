import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  server: {
    host: "0.0.0.0",
    port: 4173,
    proxy: {
      "/web": {
        target: "http://127.0.0.1:8069",
        changeOrigin: true
      },
      "/shop": {
        target: "http://127.0.0.1:8069",
        changeOrigin: true
      },
      "/website": {
        target: "http://127.0.0.1:8069",
        changeOrigin: true
      },
      "/website_sale": {
        target: "http://127.0.0.1:8069",
        changeOrigin: true
      },
      "/sale": {
        target: "http://127.0.0.1:8069",
        changeOrigin: true
      },
      "/coupon": {
        target: "http://127.0.0.1:8069",
        changeOrigin: true
      }
    }
  }
});
