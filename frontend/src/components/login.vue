<template>
  <v-container fluid class="pa-0 login-wrapper">
    <v-row no-gutters style="min-height: 100vh;">
      <!-- Left Section -->
      <v-col cols="12" md="6" class="login-form-section">
        <div class="login-content px-12 py-16">
          <!-- Logo Section -->
          <div class="mb-16">
            <v-icon color="primary" size="40" class="mb-2">mdi-home-variant</v-icon>
            <h1 class="text-h5 font-weight-bold">Household Services</h1>
          </div>

          <!-- Main Content -->
          <div class="login-form-container">
            <h2 class="text-h4 font-weight-bold mb-2">Welcome back</h2>
            <p class="text-subtitle-1 text-medium-emphasis mb-8">Please enter your details to sign in</p>

            <v-form @submit.prevent="login" ref="loginForm" v-model="isFormValid">
              <!-- Username Field -->
              <v-text-field
                v-model="username"
                :rules="[rules.required]"
                label="Username"
                placeholder="Enter your username"
                variant="outlined"
                density="comfortable"
                bg-color="grey-lighten-4"
                class="mb-4"
                :error-messages="errors.username"
                @focus="clearError('username')"
              ></v-text-field>

              <!-- Password Field -->
              <v-text-field
                v-model="password"
                :rules="[rules.required]"
                label="Password"
                placeholder="••••••••"
                variant="outlined"
                density="comfortable"
                bg-color="grey-lighten-4"
                :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                :type="showPassword ? 'text' : 'password'"
                class="mb-4"
                :error-messages="errors.password"
                @click:append-inner="showPassword = !showPassword"
                @focus="clearError('password')"
              ></v-text-field>

              <!-- Remember & Forgot -->
              <div class="d-flex justify-space-between align-center mb-8">
                <v-checkbox
                  v-model="rememberMe"
                  label="Remember me"
                  hide-details
                  density="comfortable"
                  color="primary"
                ></v-checkbox>
                <v-btn
                  variant="text"
                  color="primary"
                  class="font-weight-medium"
                  @click="forgotPassword"
                >
                  Forgot password?
                </v-btn>
              </div>

              <!-- Sign In Button -->
              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                :loading="isLoading"
                :disabled="!isFormValid"
                class="mb-4 py-6"
                elevation="0"
              >
                Sign in
              </v-btn>

              <!-- Social Login -->
              <div class="text-center mb-6">
                <p class="text-medium-emphasis mb-4">Or continue with</p>
                <div class="d-flex justify-center gap-4">
                  <v-btn
                    variant="outlined"
                    icon="mdi-google"
                    size="x-large"
                    color="grey-darken-1"
                  ></v-btn>
                  <v-btn
                    variant="outlined"
                    icon="mdi-facebook"
                    size="x-large"
                    color="grey-darken-1"
                  ></v-btn>
                  <v-btn
                    variant="outlined"
                    icon="mdi-apple"
                    size="x-large"
                    color="grey-darken-1"
                  ></v-btn>
                </div>
              </div>

              <!-- Register Link -->
              <div class="text-center">
                <span class="text-medium-emphasis">Don't have an account? </span>
                <v-btn
                  variant="text"
                  color="primary"
                  class="font-weight-bold px-2"
                  @click="$router.push('/register')"
                >
                  Sign up for free
                </v-btn>
              </div>
            </v-form>
          </div>
        </div>
      </v-col>

      <!-- Right Section - Decorative -->
      <v-col cols="12" md="6" class="d-none d-md-block position-relative overflow-hidden">
        <div class="decorative-background"></div>
      </v-col>
    </v-row>

    <!-- Error Alert -->
    <v-snackbar
      v-model="showErrorMessage"
      color="error"
      location="top"
      :timeout="4000"
    >
      {{ errorMessage }}
      <template v-slot:actions>
        <v-btn
          color="white"
          variant="text"
          @click="errorMessage = ''"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>

    <!-- Success Snackbar -->
    <v-snackbar
      v-model="showSuccessSnackbar"
      color="success"
      location="top"
      :timeout="3000"
    >
      Login successful! Redirecting...
    </v-snackbar>
  </v-container>
</template>

<script>
export default {
  name: 'Login',
  inject: ['updateAuthState'],
  data() {
    return {
      username: '',
      password: '',
      showPassword: false,
      rememberMe: false,
      isLoading: false,
      isFormValid: false,
      errorMessage: '',
      showSuccessSnackbar: false,
      showErrorMessage: false,
      errors: {
        username: '',
        password: '',
      },
      rules: {
        required: v => !!v || 'This field is required',
      }
    };
  },
  watch: {
    errorMessage(newVal) {
      this.showErrorMessage = !!newVal;
    }
  },
  methods: {
    clearError(field) {
      this.errors[field] = '';
      this.errorMessage = '';
    },
    forgotPassword() {
      this.$router.push('/forgot-password');
    },
    async login() {
      try {
        if (!this.$refs.loginForm.validate()) return;

        this.isLoading = true;
        this.errorMessage = '';

        const response = await fetch('http://localhost:5000/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || 'Invalid credentials');
        }

        if (!data.access_token) {
          throw new Error('No access token received');
        }

        // Store token and remember me preference
        localStorage.setItem('token', data.access_token);
        if (this.rememberMe) {
          localStorage.setItem('rememberedUser', this.username);
        } else {
          localStorage.removeItem('rememberedUser');
        }

        this.updateAuthState(true);
        this.showSuccessSnackbar = true;

        // Decode and redirect based on role
        const base64Url = data.access_token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const payload = JSON.parse(window.atob(base64));

        setTimeout(() => {
          if (payload.role === 'customer') {
            this.$router.push('/customer-dashboard');
          } else if (payload.role === 'professional') {
            this.$router.push('/professional-dashboard');
          } else if (payload.role === 'admin') {
            this.$router.push('/admin-dashboard');
          }
        }, 1000);

      } catch (error) {
        console.error('Login failed:', error);
        this.errorMessage = error.message || 'Login failed. Please try again.';
      } finally {
        this.isLoading = false;
      }
    }
  },
  mounted() {
    // Check for remembered username
    const rememberedUser = localStorage.getItem('rememberedUser');
    if (rememberedUser) {
      this.username = rememberedUser;
      this.rememberMe = true;
    }
  }
}
</script>

<style scoped>
.login-wrapper {
  background-color: white;
  min-height: 100vh;
}

.login-form-section {
  display: flex;
  align-items: center;
}

.login-content {
  width: 100%;
  max-width: 480px;
  margin: 0 auto;
}

.login-form-container {
  animation: fadeInUp 0.6s ease-out;
}

.decorative-background {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background: linear-gradient(45deg, #6b8afd, #4d6ce1);
  overflow: hidden;
}

.decorative-background::before {
  content: '';
  position: absolute;
  width: 150%;
  height: 150%;
  top: -25%;
  left: -25%;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="rgba(255,255,255,0.1)"/></svg>') repeat;
  animation: rotate 60s linear infinite;
}

.v-text-field {
  border-radius: 12px;
}

:deep(.v-field) {
  border-radius: 12px !important;
  transition: all 0.3s ease;
}

:deep(.v-field:hover) {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

:deep(.v-btn) {
  letter-spacing: 0.5px;
  text-transform: none;
  border-radius: 12px;
  font-weight: 600;
}

.v-btn.v-btn--size-large {
  height: 48px;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Responsive adjustments */
@media (max-width: 960px) {
  .login-content {
    padding: 2rem;
    max-width: 100%;
  }
}
</style>
