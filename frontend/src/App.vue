<template>
  <v-app>
    <!-- Modern App Bar -->
    <v-app-bar 
      app 
      elevation="1"
      :color="$vuetify.theme.dark ? 'grey-darken-4' : 'white'"
      :class="{'px-4': !isMobile}"
    >
      <!-- Brand Section -->
      <div class="d-flex align-center">
        <v-icon
          color="primary"
          size="32"
          class="mr-2"
        >
          mdi-home-variant
        </v-icon>
        <v-toolbar-title class="font-weight-bold">
          <span class="primary--text">Household</span> Services
          <span v-if="isLoggedIn && userRole === 'professional'" class="text-subtitle-2 ml-2 text-medium-emphasis">
            / Professional
          </span>
        </v-toolbar-title>
      </div>

      <v-spacer></v-spacer>

      <!-- Customer Navigation -->
      <template v-if="isLoggedIn && userRole === 'customer'">
        <div class="d-none d-md-flex align-center">
          <v-btn
            v-for="item in customerNavItems"
            :key="item.title"
            :to="item.to"
            variant="text"
            rounded="lg"
            class="mx-1 text-none"
            :class="{ 'v-btn--active': isActiveRoute(item.to) }"
          >
            <v-icon :icon="item.icon" class="mr-1" size="20"></v-icon>
            {{ item.title }}
          </v-btn>

          <!-- Cart Button -->
          <v-btn
            icon="mdi-cart"
            variant="text"
            @click="goToCheckout"
            class="ml-2"
          >
            <v-badge
              :content="cartItemCount"
              :value="cartItemCount"
              color="error"
              location="top end"
            >
              <v-icon>mdi-cart</v-icon>
            </v-badge>
          </v-btn>
        </div>

        <!-- Mobile Menu -->
        <v-app-bar-nav-icon
          class="d-md-none"
          @click="drawer = !drawer"
        ></v-app-bar-nav-icon>
      </template>

      <!-- Professional Navigation -->
      <template v-if="isLoggedIn && userRole === 'professional'">
        <div class="d-none d-md-flex align-center">
          <v-btn
            v-for="item in professionalNavItems"
            :key="item.title"
            :to="item.to"
            variant="text"
            rounded="lg"
            class="mx-1 text-none"
            :class="{ 'v-btn--active': isActiveRoute(item.to) }"
          >
            <v-icon :icon="item.icon" class="mr-1" size="20"></v-icon>
            {{ item.title }}
          </v-btn>

          <v-btn
            icon="mdi-bell"
            variant="text"
            class="ml-2"
          >
            <v-badge
              :content="pendingRequestsCount"
              :value="pendingRequestsCount"
              color="error"
              location="top end"
            >
              <v-icon>mdi-bell</v-icon>
            </v-badge>
          </v-btn>
        </div>

        <!-- Mobile Menu -->
        <v-app-bar-nav-icon
          class="d-md-none"
          @click="drawer = !drawer"
        ></v-app-bar-nav-icon>
      </template>

      <!-- Admin Navigation -->
      <template v-if="isLoggedIn && userRole === 'admin'">
        <div class="d-none d-md-flex align-center">
          <v-btn
            v-for="item in adminNavItems"
            :key="item.title"
            :to="item.to"
            variant="text"
            rounded="lg"
            class="mx-1 text-none"
            :class="{ 'v-btn--active': isActiveRoute(item.to) }"
          >
            <v-icon :icon="item.icon" class="mr-1" size="20"></v-icon>
            {{ item.title }}
          </v-btn>
        </div>

        <!-- Mobile Menu -->
        <v-app-bar-nav-icon
          class="d-md-none"
          @click="drawer = !drawer"
        ></v-app-bar-nav-icon>
      </template>

      <!-- Auth Buttons -->
      <template v-if="!isLoggedIn">
        <v-btn
          to="/login"
          variant="text"
          rounded="lg"
          class="text-none mr-2"
        >
          <v-icon icon="mdi-login" class="mr-1" size="20"></v-icon>
          Sign In
        </v-btn>
        <v-btn
          to="/register"
          color="primary"
          rounded="lg"
          class="text-none"
          elevation="0"
        >
          Sign Up
        </v-btn>
      </template>

      <!-- Theme Toggle -->
      <!-- <v-btn
        icon
        variant="text"
        @click="toggleTheme"
        class="ml-2"
      >
        <!-- <v-icon>{{ isDark() ? 'mdi-weather-sunny' : 'mdi-weather-night' }}</v-icon> -->
      <!-- </v-btn>  -->

      <!-- User Menu -->
      <template v-if="isLoggedIn">
        <v-menu
          transition="slide-y-transition"
          :close-on-content-click="false"
        >
          <template v-slot:activator="{ props }">
            <v-btn
              class="ml-2"
              variant="text"
              v-bind="props"
              rounded="lg"
            >
              <v-avatar size="32" color="primary" class="mr-2">
                <span class="text-h6 text-white">{{ userInitials }}</span>
              </v-avatar>
              <v-icon icon="mdi-chevron-down"></v-icon>
            </v-btn>
          </template>

          <v-card min-width="200" elevation="4" rounded="lg" class="mt-2">
            <v-list>
              <v-list-item>
                <template v-slot:prepend>
                  <v-avatar size="40" color="primary">
                    <span class="text-h6 text-white">{{ userInitials }}</span>
                  </v-avatar>
                </template>
                <v-list-item-title class="text-subtitle-1 font-weight-medium">
                  {{ userName }}
                </v-list-item-title>
                <v-list-item-subtitle class="text-caption">
                  {{ userEmail }}
                </v-list-item-subtitle>
              </v-list-item>

              <v-divider class="my-2"></v-divider>

              <v-list-item
                link
                @click="logout"
                class="text-error"
              >
                <template v-slot:prepend>
                  <v-icon icon="mdi-logout" color="error"></v-icon>
                </template>
                <v-list-item-title>Logout</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card>
        </v-menu>
      </template>
    </v-app-bar>

    <!-- Mobile Navigation Drawer -->
    <v-navigation-drawer
      v-model="drawer"
      temporary
      location="right"
      width="280"
    >
      <v-list>
        <!-- Customer Navigation Items -->
        <template v-if="userRole === 'customer'">
          <v-list-item
            v-for="item in customerNavItems"
            :key="item.title"
            :to="item.to"
            :prepend-icon="item.icon"
            :title="item.title"
            rounded="lg"
          ></v-list-item>

          <v-divider class="my-2"></v-divider>

          <v-list-item
            @click="goToCheckout"
            prepend-icon="mdi-cart"
            title="Cart"
            rounded="lg"
          >
            <template v-slot:append>
              <v-badge
                :content="cartItemCount"
                :value="cartItemCount"
                color="error"
              ></v-badge>
            </template>
          </v-list-item>
        </template>

        <!-- Professional Navigation Items -->
        <template v-if="userRole === 'professional'">
          <v-list-item
            v-for="item in professionalNavItems"
            :key="item.title"
            :to="item.to"
            :prepend-icon="item.icon"
            :title="item.title"
            rounded="lg"
          ></v-list-item>

          <v-divider class="my-2"></v-divider>

          <v-list-item
            prepend-icon="mdi-bell"
            title="Notifications"
            rounded="lg"
          >
            <template v-slot:append>
              <v-badge
                :content="pendingRequestsCount"
                :value="pendingRequestsCount"
                color="error"
              ></v-badge>
            </template>
          </v-list-item>
        </template>

        <!-- Admin Navigation Items -->
        <template v-if="userRole === 'admin'">
          <v-list-item
            v-for="item in adminNavItems"
            :key="item.title"
            :to="item.to"
            :prepend-icon="item.icon"
            :title="item.title"
            rounded="lg"
          ></v-list-item>
        </template>
      </v-list>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main>
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </v-main>
  </v-app>
</template>

<script>
import { useTheme } from './plugins/theme'
import { watch } from 'vue'
import { useTheme as useVuetifyTheme } from 'vuetify'

export default {
  name: 'App',
  data() {
    return {
      isLoggedIn: false,
      userRole: null,
      userEmail: null,
      userName: null,
      cartItemCount: 0,
      cartItems: [],
      drawer: false,
      pendingRequestsCount: 0,
      customerNavItems: [
        { title: 'Home', icon: 'mdi-home', to: '/customer-dashboard' },
        { title: 'Ongoing', icon: 'mdi-clock-outline', to: '/customer/ongoing-services' },
        { title: 'Completed', icon: 'mdi-check-circle-outline', to: '/customer/completed-services' },
        // { title: 'Summary', icon: 'mdi-file-document-outline', to: '/customer/summary' },
      ],
      professionalNavItems: [
        { title: 'Dashboard', icon: 'mdi-view-dashboard', to: '/professional-dashboard' },
        // { title: 'Schedule', icon: 'mdi-calendar-clock', to: '/professional/schedule' },
        { title: 'History', icon: 'mdi-history', to: '/professional/history' },
        // { title: 'Earnings', icon: 'mdi-currency-inr', to: '/professional/earnings' },
      ],
      adminNavItems: [
        { title: 'Users', icon: 'mdi-account-group', to: '/admin/users' },
        { title: 'Verify Professionals', icon: 'mdi-account-check', to: '/admin/verify-professionals' },
        { title: 'Export Report', icon: 'mdi-file-chart', to: '/admin/export-report' },
        { title: 'Services', icon: 'mdi-briefcase', to: '/admin/services' },
        { title: 'Analytics', icon: 'mdi-chart-bar', to: '/admin/analytics' },
        // { title: 'Settings', icon: 'mdi-cog', to: '/admin/settings' }
      ]
    }
  },
  computed: {
    isMobile() {
      return this.$vuetify?.display?.mobile ?? false;
    },
    userInitials() {
      if (!this.userName) return 'U';
      const names = this.userName.split(' ');
      if (names.length > 1) {
        // If there are multiple names, use first letter of first and last name
        return (names[0].charAt(0) + names[names.length - 1].charAt(0)).toUpperCase();
      }
      // If single name, use first letter
      return names[0].charAt(0).toUpperCase();
    }
  },
  provide() {
    return {
      updateAuthState: this.checkAuth,
      updateCart: this.updateCartCount,
      addToCart: this.addToCart,
      removeFromCart: this.removeFromCart,
      clearCart: this.clearCart,
      getCartItems: () => this.cartItems
    }
  },
  created() {
    this.checkAuth();
  },
  methods: {
    isActiveRoute(path) {
      return this.$route.path === path;
    },
    checkAuth() {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          // Decode the token
          const base64Url = token.split('.')[1];
          const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
          const decodedPayload = decodeURIComponent(
            atob(base64)
              .split('')
              .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
              .join('')
          );
          
          const payload = JSON.parse(decodedPayload);
          console.log('Decoded token payload:', payload); // Debug log
          
          if (payload.exp < Date.now() / 1000) {
            console.log('Token expired');
            this.logout();
            return;
          }
          
          // Check for required fields
          if (!payload.role || !payload.username || !payload.email) {
            console.error('Missing required claims in token payload:', payload);
            this.logout();
            return;
          }
          
          // Update user state
          this.userRole = payload.role;
          this.userEmail = payload.email;
          this.userName = payload.username;
          this.isLoggedIn = true;
          
          console.log('User state updated:', {
            role: this.userRole,
            email: this.userEmail,
            name: this.userName
          });
        } catch (error) {
          console.error('Error decoding token:', error);
          this.logout();
        }
      } else {
        this.isLoggedIn = false;
        this.userRole = null;
        this.userEmail = null;
        this.userName = null;
      }
    },
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('cart');
      this.isLoggedIn = false;
      this.userRole = null;
      this.userEmail = null;
      this.userName = null;
      this.cartItemCount = 0;
      this.drawer = false;
      
      this.$router.push('/login').then(() => {
        window.location.reload();
      });
    },
    updateCartCount(count) {
      this.cartItemCount = count;
    },
    async goToCheckout() {
      try {
        await this.$router.push('/checkout');
        this.drawer = false;
        this.$nextTick(() => {
          this.$forceUpdate();
        });
      } catch (err) {
        if (err.name !== 'NavigationDuplicated') {
          console.error('Navigation error:', err);
        }
      }
    },
    addToCart(item) {
      this.cartItems.push(item);
      this.cartItemCount = this.cartItems.length;
    },
    removeFromCart(index) {
      this.cartItems.splice(index, 1);
      this.cartItemCount = this.cartItems.length;
    },
    clearCart() {
      this.cartItems = [];
      this.cartItemCount = 0;
    },
    async fetchPendingRequests() {
      if (this.userRole === 'professional') {
        try {
          const response = await fetch('http://localhost:5000/professional/dashboard', {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`,
              'Accept': 'application/json'
            }
          });
          
          if (!response.ok) {
            throw new Error('Failed to fetch pending requests');
          }
          
          const data = await response.json();
          this.pendingRequestsCount = (data.pending_requests || []).length;
        } catch (error) {
          console.error('Error fetching pending requests:', error);
        }
      }
    }
  },
  mounted() {
    this.checkAuth();
    this.fetchPendingRequests();
  },
  watch: {
    userRole: {
      immediate: true,
      handler(newRole) {
        if (newRole === 'professional') {
          this.fetchPendingRequests();
        }
      }
    }
  },
  setup() {
    const { theme, toggleTheme, isDark } = useTheme()
    const vuetifyTheme = useVuetifyTheme()

    // Sync our theme with Vuetify's theme
    watch(theme, (newTheme) => {
      vuetifyTheme.global.name.value = newTheme
    })

    // Initialize Vuetify theme based on our theme
    vuetifyTheme.global.name.value = theme.value
  }
}
</script>

<style scoped>
.v-btn--active {
  background-color: var(--v-primary-lighten5);
  color: rgb(var(--v-theme-primary)) !important;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

:deep(.v-btn) {
  text-transform: none;
  font-weight: 500;
}

:deep(.v-toolbar-title) {
  font-size: 1.25rem;
  letter-spacing: 0.5px;
}

/* Responsive Styles */
@media (max-width: 600px) {
  :deep(.v-toolbar-title) {
    font-size: 1.1rem;
  }
}
</style>