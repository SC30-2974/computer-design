import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ mode }) => ({
  // GitHub Pages 项目页需要仓库子路径；本地开发保持根路径。
  base: mode === 'production' ? '/computer-design/' : '/',
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5173,
  },
}))
