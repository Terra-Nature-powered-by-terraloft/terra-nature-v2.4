import type { Config } from "tailwindcss"

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "obsidian": "#0a0a0f",
        "midnight": "#0d0d1a",
        "electric-indigo": "#6366f1",
        "soft-lavender": "#a5b4fc",
        "thermal-amber": "#f59e0b",
        "cold-white": "#f8fafc",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
}

export default config
