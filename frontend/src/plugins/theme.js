import { ref, watch } from 'vue'

const THEME_KEY = 'user-theme'
const DARK = 'dark'
const LIGHT = 'light'

// Create a reactive theme state
const theme = ref(localStorage.getItem(THEME_KEY) || LIGHT)

// Watch for theme changes and update localStorage and document
watch(theme, (newTheme) => {
  localStorage.setItem(THEME_KEY, newTheme)
  updateTheme(newTheme)
})

// Function to update the document theme
function updateTheme(newTheme) {
  document.documentElement.classList.remove(DARK, LIGHT)
  document.documentElement.classList.add(newTheme)
}

// Initialize theme on page load
updateTheme(theme.value)

export function useTheme() {
  function toggleTheme() {
    theme.value = theme.value === LIGHT ? DARK : LIGHT
  }

  return {
    theme,
    toggleTheme,
    isDark: () => theme.value === DARK
  }
} 