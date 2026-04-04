import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ mode }) => ({
  // GitHub Pages 部署在 /computer-design/ 子路径下，本地开发仍使用根路径。
  base: mode === 'production' ? '/computer-design/' : '/',
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5173,
  },
}))