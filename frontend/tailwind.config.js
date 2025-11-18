@"
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        wordsmith: {
          dark: '#1a1a1a',
          darker: '#0f0f0f',
          gray: '#2a2a2a',
          'gray-light': '#3a3a3a',
          'gray-text': '#9ca3af',
          'gray-border': '#374151',
          blue: '#3b82f6',
          purple: '#8b5cf6',
          orange: '#f97316',
          green: '#10b981',
          yellow: '#f59e0b'
        }
      },
      animation: {
        'pulse-slow': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-subtle': 'bounce 1s ease-in-out infinite',
      }
    },
  },
  plugins: [],
}
"@ | Out-File -FilePath "tailwind.config.js" -Encoding UTF8