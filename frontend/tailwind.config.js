/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // Oceano da Grand Line — azuis profundos (fundos, cabeçalhos)
        ocean: {
          50: '#eef6fb',
          100: '#d5e8f4',
          200: '#a9d0e8',
          300: '#6fb0d6',
          400: '#3d8cbf',
          500: '#256d9f',
          600: '#1b5583',
          700: '#17456a',
          800: '#123753',
          900: '#0d2540',
          950: '#08182c',
        },
        // Tesouro / chapéu de palha — dourados (destaque principal)
        treasure: {
          50: '#fdf8ec',
          100: '#faedc9',
          200: '#f5d98e',
          300: '#f0c254',
          400: '#eaad2f',
          500: '#d9911c',
          600: '#bd6f15',
          700: '#9d5115',
          800: '#804017',
          900: '#6a3516',
        },
        // Colete do Luffy / Jolly Roger — vermelho coral (CTA)
        coral: {
          50: '#fdf3f2',
          100: '#fce3e1',
          200: '#facdc8',
          300: '#f5a99f',
          400: '#ed7568',
          500: '#e2493a',
          600: '#cf301f',
          700: '#ad2517',
          800: '#8f2217',
          900: '#77221a',
        },
        // Pergaminho / mapa do tesouro — cremes (fundos claros)
        parchment: {
          50: '#fdfbf5',
          100: '#faf4e4',
          200: '#f3e7c6',
        },
      },
      fontFamily: {
        display: ['"Pirata One"', 'cursive'],
        sans: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        card: '0 10px 30px -12px rgba(13, 37, 64, 0.25)',
        'card-hover': '0 22px 45px -15px rgba(13, 37, 64, 0.35)',
        glow: '0 0 0 3px rgba(240, 194, 84, 0.35)',
      },
      backgroundImage: {
        'ocean-hero':
          'radial-gradient(circle at 20% 20%, rgba(240,194,84,0.15), transparent 40%), radial-gradient(circle at 85% 15%, rgba(226,73,58,0.18), transparent 45%), linear-gradient(160deg, #0d2540 0%, #123753 55%, #08182c 100%)',
      },
      keyframes: {
        'fade-up': {
          '0%': { opacity: '0', transform: 'translateY(14px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'float-slow': {
          '0%,100%': { transform: 'translateY(0) rotate(-3deg)' },
          '50%': { transform: 'translateY(-10px) rotate(3deg)' },
        },
      },
      animation: {
        'fade-up': 'fade-up 0.5s ease-out both',
        'float-slow': 'float-slow 6s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
