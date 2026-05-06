module.exports = {
  content: [
    './content/**/*.{md,html}',
    './layouts/**/*.html',
    './data/**/*.{yaml,yml}',
  ],
  theme: {
    extend: {
      colors: {
        blue: {
          50: '#f0f4fb',
          100: '#e0e8f7',
          200: '#c8d7f0',
          300: '#a3bce5',
          400: '#7897d8',
          500: '#5570B5', // Logo blue as the primary
          600: '#5570B5', // Logo blue
          700: '#3d548a',
          800: '#2f4169',
          900: '#1d2a3a',
        }
      }
    },
  },
  plugins: [],
}
