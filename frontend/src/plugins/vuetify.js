/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#007bff',
          secondary: '#6c757d',
          accent: '#4dabf7',
          error: '#dc3545',
          info: '#17a2b8',
          success: '#28a745',
          warning: '#ffc107',
          background: '#ffffff',
          surface: '#f8f9fa',
        }
      },
      dark: {
        dark: true,
        colors: {
          primary: '#4dabf7',
          secondary: '#909090',
          accent: '#74c0fc',
          error: '#ff4444',
          info: '#33b5e5',
          success: '#00C851',
          warning: '#ffbb33',
          background: '#1a1a1a',
          surface: '#2d2d2d',
        }
      }
    }
  }
})
