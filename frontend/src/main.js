/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'
import router from './router'  // Import the router
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'vuetify/styles'
import './plugins/theme'
import './assets/main.css'

const vuetify = createVuetify({
  components,
  directives,
})

const app = createApp(App)

registerPlugins(app)

app.use(router)  // Use the router
app.use(vuetify)

app.mount('#app')
