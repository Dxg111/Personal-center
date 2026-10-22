/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'bg-dark': '#0a0e1a',
        'bg-panel': '#0c1220',
        'bg-panel-2': '#111a2e',
        'line': '#1a2540',
        'neon-green': '#00ffc8',
        'neon-blue': '#00d2ff',
        'neon-yellow': '#ffb020',
        'text': '#c8d6e5',
        'text-dim': '#5a6b85',
        'text-bright': '#e8f4ff',
      },
      fontFamily: {
        'mono': ['JetBrains Mono', 'monospace'],
        'rajdhani': ['Rajdhani', 'sans-serif'],
      },
      animation: {
        'scanline': 'scanline 4s linear infinite',
        'blink': 'blink 1s step-end infinite',
        'pulse-dot': 'pulse-dot 2s ease-in-out infinite',
        'sweep': 'sweep 5s linear infinite',
      },
      keyframes: {
        scanline: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100vh)' },
        },
        blink: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.3' },
        },
        'pulse-dot': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.3' },
        },
        sweep: {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
      },
    },
  },
  plugins: [],
}
