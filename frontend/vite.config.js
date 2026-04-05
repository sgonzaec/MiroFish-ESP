import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    open: true,
    proxy: {
      '/api': {
        target: 'personal-mirofish-kjcpry-7a5a50-161-22-42-62.traefik.me',
        changeOrigin: true,
        secure: false
      }
    }
  }
})
