<template>
  <button class="theme-toggle" @click="toggleTheme" :title="isDark() ? 'Switch to Light Mode' : 'Switch to Dark Mode'">
    <span v-if="isDark()">🌞</span>
    <span v-else>🌙</span>
  </button>
</template>

<script setup>
import { useTheme } from '../plugins/theme'

const { toggleTheme, isDark } = useTheme()
</script>

<style scoped>
.theme-toggle {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  font-size: 1.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease;
}

.theme-toggle:hover {
  background-color: var(--bg-secondary);
}

.theme-toggle:focus {
  outline: 2px solid var(--accent-color);
  outline-offset: 2px;
}
</style> 