/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        border: "rgb(39 39 42)",
        input: "rgb(39 39 42)",
        background: "rgb(9 9 11)",
        foreground: "rgb(250 250 250)",
        primary: {
          DEFAULT: "rgb(59 130 246)",
          foreground: "rgb(250 250 250)",
        },
        secondary: {
          DEFAULT: "rgb(39 39 42)",
          foreground: "rgb(250 250 250)",
        },
        muted: {
          DEFAULT: "rgb(39 39 42)",
          foreground: "rgb(161 161 170)",
        },
        accent: {
          DEFAULT: "rgb(39 39 42)",
          foreground: "rgb(250 250 250)",
        },
      },
      keyframes: {
        "fade-in": {
          "0%": { opacity: 0 },
          "100%": { opacity: 1 },
        },
        "slide-up": {
          "0%": { transform: "translateY(10px)", opacity: 0 },
          "100%": { transform: "translateY(0)", opacity: 1 },
        },
      },
      animation: {
        "fade-in": "fade-in 0.5s ease-out",
        "slide-up": "slide-up 0.5s ease-out",
      },
    },
  },
  plugins: [],
} 