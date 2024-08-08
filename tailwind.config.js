/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
  theme: {
    colors: {
      dracula: '#D30C7B',
      stdbg: '282A36',
    }
  }
}