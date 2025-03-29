<template>
  <v-container fluid class="fill-height registration-container">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-8 rounded-lg registration-card" :class="{ 'theme--dark': isDark() }">
          <div class="text-center pt-8">
            <v-avatar size="80" color="primary" class="elevation-4">
              <v-icon size="48" color="white">mdi-account-plus</v-icon>
            </v-avatar>
            <h1 class="text-h4 font-weight-bold mt-4 mb-2">Customer Registration</h1>
            <p class="text-body-1 text-medium-emphasis mb-6">Join our community of satisfied customers</p>
          </div>

          <v-card-text>
            <v-form @submit.prevent="register" class="registration-form">
              <v-slide-y-transition group>
                <v-text-field
                  v-model="username"
                  label="Username"
                  prepend-inner-icon="mdi-account"
                  variant="outlined"
                  class="mb-4"
                  :rules="[v => !!v || 'Username is required']"
                  required
                ></v-text-field>

                <v-text-field
                  v-model="email"
                  label="Email"
                  prepend-inner-icon="mdi-email"
                  variant="outlined"
                  class="mb-4"
                  :rules="[
                    v => !!v || 'Email is required',
                    v => /.+@.+\..+/.test(v) || 'Email must be valid'
                  ]"
                  required
                ></v-text-field>

                <v-text-field
                  v-model="phone"
                  label="Phone Number"
                  prepend-inner-icon="mdi-phone"
                  variant="outlined"
                  class="mb-4"
                  :rules="[
                    v => !!v || 'Phone number is required',
                    v => /^\d{10}$/.test(v) || 'Phone number must be 10 digits'
                  ]"
                  required
                ></v-text-field>

                <v-text-field
                  v-model="password"
                  label="Password"
                  prepend-inner-icon="mdi-lock"
                  :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                  variant="outlined"
                  class="mb-6"
                  :type="showPassword ? 'text' : 'password'"
                  :rules="[
                    v => !!v || 'Password is required',
                    v => v.length >= 8 || 'Password must be at least 8 characters'
                  ]"
                  @click:append-inner="showPassword = !showPassword"
                  required
                ></v-text-field>
              </v-slide-y-transition>

              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                class="mb-4"
                elevation="2"
                :loading="loading"
              >
                Register
              </v-btn>
            </v-form>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions class="pa-6 d-flex flex-column align-center">
            <p class="text-body-2 text-medium-emphasis mb-2">Are you a service provider?</p>
            <v-btn
              variant="outlined"
              color="primary"
              @click="goToProfessionalRegister"
              class="px-8"
            >
              Register as Professional
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { useTheme } from '../plugins/theme'

export default {
  name: 'CustomerRegister',
  inject: ['updateAuthState'],
  setup() {
    const { isDark } = useTheme()
    return { isDark }
  },
  data() {
    return {
      username: '',
      email: '',
      phone: '',
      password: '',
      showPassword: false,
      loading: false,
    }
  },
  methods: {
    async register() {
      this.loading = true
      try {
        const response = await fetch('http://localhost:5000/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            phone: this.phone,
            password: this.password,
            role: 'customer',
          }),
        })

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.message || 'Registration failed')
        }

        const data = await response.json()
        console.log('Registration successful:', data)
        this.$router.push('/login')
      } catch (error) {
        console.error('Registration failed:', error.message)
        alert(error.message)
      } finally {
        this.loading = false
      }
    },
    goToProfessionalRegister() {
      this.$router.push('/register-professional')
    },
  },
}
</script>

<style scoped>
.registration-container {
  background: var(--bg-secondary);
  min-height: 100vh;
}

.registration-card {
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  transition: transform 0.3s ease;
}

.registration-card:hover {
  transform: translateY(-5px);
}

.registration-form {
  max-width: 400px;
  margin: 0 auto;
}

:deep(.v-field) {
  border-radius: 8px !important;
}

:deep(.v-field__input) {
  padding: 16px 12px;
}

:deep(.v-label) {
  font-size: 0.95rem;
}

.theme--dark {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}
</style>