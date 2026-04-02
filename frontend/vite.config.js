import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')

  return {
    plugins: [react()],
    server: env.VITE_DEV_API_URL
      ? {
          proxy: {
            '/api': env.VITE_DEV_API_URL
          }
        }
      : undefined
  }
})
