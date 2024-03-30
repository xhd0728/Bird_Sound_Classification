module.exports = {
  purge: ['./src/**/*.vue'],
  theme: {
    screens: {
      sm: '640px',
      // => @media (min-width: 640px) { ... }
      md: '768px',
      // => @media (min-width: 768px) { ... }
      lg: '1138px',
      // => @media (min-width: 1024px) { ... }
    },
    extend: {
      borderRadius: {
        xl: '1rem',
      },
    },
  },
  variants: {},
  plugins: [],
}
