<template>
  <v-container fluid class="fill-height registration-container">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="10" md="8" lg="6">
        <v-card class="elevation-8 rounded-lg registration-card" :class="{ 'theme--dark': isDark() }">
          <div class="text-center pt-8">
            <v-avatar size="80" color="primary" class="elevation-4">
              <v-icon size="48" color="white">mdi-briefcase-account</v-icon>
            </v-avatar>
            <h1 class="text-h4 font-weight-bold mt-4 mb-2">Professional Registration</h1>
            <p class="text-body-1 text-medium-emphasis mb-6">Join our network of trusted service providers</p>
          </div>

          <v-card-text>
            <v-form @submit.prevent="register" class="registration-form" enctype="multipart/form-data">
              <v-row>
                <v-col cols="12" md="6">
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
                      class="mb-4"
                      :type="showPassword ? 'text' : 'password'"
                      :rules="[
                        v => !!v || 'Password is required',
                        v => v.length >= 8 || 'Password must be at least 8 characters'
                      ]"
                      @click:append-inner="showPassword = !showPassword"
                      required
                    ></v-text-field>
                  </v-slide-y-transition>
                </v-col>

                <v-col cols="12" md="6">
                  <v-slide-y-transition group>
                    <v-text-field
                      v-model="age"
                      label="Age"
                      prepend-inner-icon="mdi-calendar"
                      variant="outlined"
                      type="number"
                      class="mb-4"
                      :rules="[
                        v => !!v || 'Age is required',
                        v => v >= 18 || 'Must be at least 18 years old'
                      ]"
                      required
                    ></v-text-field>

                    <v-text-field
                      v-model="service"
                      label="Proposed Service Type"
                      prepend-inner-icon="mdi-briefcase"
                      variant="outlined"
                      class="mb-4"
                      :rules="[v => !!v || 'Service type is required']"
                      hint="Describe the service you want to provide"
                      persistent-hint
                      required
                    ></v-text-field>

                    <v-text-field
                      v-model="experience"
                      label="Experience (years)"
                      prepend-inner-icon="mdi-briefcase-clock"
                      variant="outlined"
                      type="number"
                      class="mb-4"
                      :rules="[
                        v => !!v || 'Experience is required',
                        v => v >= 0 || 'Experience cannot be negative'
                      ]"
                      required
                    ></v-text-field>

                    <v-file-input
                      v-model="document"
                      label="Upload Verification Document"
                      accept=".pdf,.doc,.docx"
                      prepend-inner-icon="mdi-file-document"
                      variant="outlined"
                      class="mb-4"
                      :rules="documentRules"
                      show-size
                      required
                    ></v-file-input>
                  </v-slide-y-transition>
                </v-col>
              </v-row>

              <v-alert
                v-if="showPendingAlert"
                type="info"
                variant="tonal"
                class="mb-4"
              >
                Your registration will be pending until admin approval
              </v-alert>

              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                class="mb-4"
                elevation="2"
                :loading="loading"
              >
                Register as Professional
              </v-btn>
            </v-form>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions class="pa-6 d-flex flex-column align-center">
            <p class="text-body-2 text-medium-emphasis mb-2">Looking for services?</p>
            <v-btn
              variant="outlined"
              color="primary"
              :to="'/register'"
              class="px-8"
            >
              Register as Customer
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
  name: 'RegisterProfessional',
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
      age: '',
      service: '',
      experience: '',
      document: null,
      showPassword: false,
      showPendingAlert: false,
      loading: false,
      documentRules: [
        v => !!v || 'Document is required',
        v => !v || v.size < 5000000 || 'Document size should be less than 5 MB',
      ]
    }
  },
  methods: {
    async register() {
      this.loading = true
      try {
        const formData = new FormData()
        formData.append('username', this.username)
        formData.append('email', this.email)
        formData.append('phone', this.phone)
        formData.append('password', this.password)
        formData.append('role', 'professional')
        formData.append('age', this.age)
        formData.append('service', this.service)
        formData.append('experience', this.experience)
        formData.append('document', this.document)

        const response = await fetch('http://localhost:5000/register', {
          method: 'POST',
          body: formData
        })

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.message || 'Registration failed')
        }

        const data = await response.json()
        this.showPendingAlert = true
        setTimeout(() => {
          this.$router.push('/login')
        }, 3000)
      } catch (error) {
        console.error('Registration failed:', error.message)
        alert(error.message)
      } finally {
        this.loading = false
      }
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
  max-width: 800px;
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

:deep(.v-alert) {
  border-radius: 8px;
}
</style>