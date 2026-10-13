/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    screens: { sm: '640px', md: '768px', lg: '992px', xl: '1280px', '2xl': '1440px' },
    extend: {
      colors: {
        'text-primary': '#2e2a42',
        purple: { 100: '#5934c5', hover: '#7a55fd', active: '#5a20e1', disabled: 'rgb(208,183,243)' },
        violet: { 100: '#d7befc' },
        latte: { 100: '#fcfbfa', 125: '#c7c3c0', 150: '#f9f5f1' },
        'sea-green': { 100: '#4ca67e' },
        tangerine: '#ff914d',
        apricot: '#ffa552',
        marigold: '#ffd55d',
        star: '#ffdd7d',
        ink: '#0a0a0a',
        pill: { development: '#ffd6a7', neutral: '#f1f5f9', health: '#ffc9c9', sleep: '#e7e5e4' },
        slate: { 100: '#f1f5f9', 800: '#1d293d' },
        gray: { 50: '#f9fafb', 300: '#d1d5dc', 700: '#364153', 900: '#101828' },
      },
      fontFamily: {
        sans: ['sansRegular', '"sansRegular Fallback"'],
        'sans-regular': ['sansRegular', '"sansRegular Fallback"'],
        'sans-book': ['sansBook', '"sansBook Fallback"'],
        'sans-semibold': ['sansSemibold', '"sansSemibold Fallback"'],
        'sans-bold': ['sansBold', '"sansBold Fallback"'],
        'sans-black': ['sansBlack'],
        serif: ['"serif"', '"serif Fallback"'],
      },
      backgroundImage: {
        'features-gradient': 'radial-gradient(534.59% 131.83% at 43.09% 3.04%, #FF93AB 0%, #FF9C7F 2.14%, #FFA168 23.66%, #F9F5F1 65.12%)',
        'faq-gradient': 'radial-gradient(rgb(165,201,242) 0, #f9f5f1 70%)',
        'pricing-radial': 'radial-gradient(45.01% 50.02% at 50% 52.71%, #ff914d 0, #f9f5f1 100%)',
      },
      boxShadow: {
        DEFAULT: '0 1px 3px 0 #0000001a, 0 1px 2px -1px #0000001a',
        sm: '0 1px 3px 0 #0000001a, 0 1px 2px -1px #0000001a',
        md: '0 4px 6px -1px #0000001a, 0 2px 4px -2px #0000001a',
        '2xl': '0 25px 50px -12px #00000040',
      },
      transitionTimingFunction: { DEFAULT: 'cubic-bezier(0.4,0,0.2,1)' },
    },
  },
  plugins: [],
}
