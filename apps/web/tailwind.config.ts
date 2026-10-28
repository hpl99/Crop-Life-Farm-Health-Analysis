import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: ["class", '[data-theme="high-contrast"]'],
  theme: {
    extend: {
      colors: {
        forest: {
          DEFAULT: "#2F5D3A",
          dark: "#1E3D26",
          light: "#3E7A4D",
        },
        leaf: {
          DEFAULT: "#5B8C3E",
          light: "#72AB50",
        },
        soil: {
          DEFAULT: "#6B4A2F",
          dark: "#4A321E",
        },
        ochre: {
          DEFAULT: "#D9A441",
          light: "#F0BD5D",
        },
        terracotta: {
          DEFAULT: "#B5532F",
          light: "#D16B45",
        },
        teal: {
          DEFAULT: "#2F7F86",
          light: "#3FA1AA",
        },
        cream: {
          DEFAULT: "#FAF5E9",
          dark: "#F0E8D0",
        },
        charcoal: {
          DEFAULT: "#2B2B26",
          muted: "#5A5A52",
        },
      },
      fontFamily: {
        sans: ["Mukta", "Noto Sans", "Noto Sans Devanagari", "sans-serif"],
        devanagari: ["Noto Sans Devanagari", "Mukta", "sans-serif"],
      },
      borderRadius: {
        card: "24px",
        panel: "32px",
        hero: "40px",
      },
      boxShadow: {
        card: "0 4px 12px rgba(0,0,0,0.05)",
        elevated: "0 8px 24px rgba(0,0,0,0.08)",
      },
    },
  },
  plugins: [],
};

export default config;

