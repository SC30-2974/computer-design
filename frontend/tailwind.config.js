export default {
  content: ['./index.html', './src/**/*.{vue,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        cyber: {
          950: '#020617',
          900: '#07111f',
          800: '#0f172a',
          500: '#22d3ee',
          400: '#67e8f9',
        },
      },
      boxShadow: {
        glow: '0 0 40px rgba(34, 211, 238, 0.18)',
      },
    },
  },
  plugins: [],
}
