import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// The browser (including your phone) only talks to port 5173.
// Vite forwards /api/* to the backend, so no CORS or IP problems.
const backend = process.env.VITE_PROXY_TARGET ?? "http://localhost:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    proxy: { "/api": { target: backend, changeOrigin: true } },
  },
});
