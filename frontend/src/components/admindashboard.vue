<template>
  <v-container fluid class="admin-dashboard pa-6">
    <!-- Header Section -->
    <v-row class="mb-6">
      <v-col cols="12" md="8">
        <h1 class="text-h4 font-weight-bold mb-2">Admin Dashboard</h1>
        <p class="text-subtitle-1 text-medium-emphasis">Manage users, services, and system settings</p>
      </v-col>
    </v-row>

    <!-- Stats Cards -->
    <v-row class="mb-6">
      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <div class="text-subtitle-2 text-medium-emphasis mb-1">Total Users</div>
                <div class="text-h4 font-weight-bold">{{ totalUsers }}</div>
              </div>
              <v-avatar color="primary" size="48" class="elevation-1">
                <v-icon icon="mdi-account-group" size="24" color="white"></v-icon>
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <div class="text-subtitle-2 text-medium-emphasis mb-1">Pending Verifications</div>
                <div class="text-h4 font-weight-bold">{{ pendingVerifications }}</div>
              </div>
              <v-avatar color="warning" size="48" class="elevation-1">
                <v-icon icon="mdi-account-clock" size="24" color="white"></v-icon>
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <div class="text-subtitle-2 text-medium-emphasis mb-1">Active Services</div>
                <div class="text-h4 font-weight-bold">{{ activeServices }}</div>
              </div>
              <v-avatar color="success" size="48" class="elevation-1">
                <v-icon icon="mdi-briefcase-check" size="24" color="white"></v-icon>
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <div class="text-subtitle-2 text-medium-emphasis mb-1">Total Revenue</div>
                <div class="text-h4 font-weight-bold">₹{{ totalRevenue }}</div>
              </div>
              <v-avatar color="info" size="48" class="elevation-1">
                <v-icon icon="mdi-currency-inr" size="24" color="white"></v-icon>
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Quick Actions -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex align-center py-3 px-6">
            <v-icon icon="mdi-lightning-bolt" color="warning" class="mr-2"></v-icon>
            Quick Actions
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="py-4">
            <v-row>
              <v-col cols="12" sm="6" md="3">
                <v-btn
                  block
                  color="primary"
                  variant="elevated"
                  prepend-icon="mdi-account-plus"
                  @click="addNewUser"
                >
                  Add New User
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-btn
                  block
                  color="success"
                  variant="elevated"
                  prepend-icon="mdi-briefcase-plus"
                  @click="addNewService"
                >
                  Add New Service
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-btn
                  block
                  color="info"
                  variant="elevated"
                  prepend-icon="mdi-file-download"
                  @click="downloadReport"
                >
                  Download Report
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-btn
                  block
                  color="warning"
                  variant="elevated"
                  prepend-icon="mdi-cog"
                  @click="systemSettings"
                >
                  System Settings
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Main Content -->
    <v-row>
      <v-col cols="12">
        <v-card class="content-card">
          <router-view></router-view>
        </v-card>
      </v-col>
    </v-row>

    <!-- Notification Snackbar -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="3000"
    >
      {{ snackbar.text }}
      <template v-slot:actions>
        <v-btn
          color="white"
          variant="text"
          @click="snackbar.show = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
export default {
  name: 'AdminDashboard',
  data() {
    return {
      totalUsers: 0,
      pendingVerifications: 0,
      activeServices: 0,
      totalRevenue: 0,
      snackbar: {
        show: false,
        text: '',
        color: 'success'
      }
    }
  },
  methods: {
    async fetchDashboardStats() {
      try {
        const response = await fetch('http://localhost:5000/admin/dashboard/stats', {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token'),
            'Accept': 'application/json'
          }
        });
        
        if (!response.ok) {
          throw new Error('Failed to fetch dashboard stats');
        }
        
        const data = await response.json();
        this.totalUsers = data.total_users || 0;
        this.pendingVerifications = data.pending_verifications || 0;
        this.activeServices = data.active_services || 0;
        this.totalRevenue = data.total_revenue || 0;
      } catch (error) {
        console.error('Error fetching dashboard stats:', error);
        this.showSnackbar('Failed to load dashboard statistics', 'error');
      }
    },
    addNewUser() {
      this.$router.push('/admin/users/new');
    },
    addNewService() {
      this.$router.push('/admin/services/new');
    },
    downloadReport() {
      this.$router.push('/admin/export-report');
    },
    systemSettings() {
      this.$router.push('/admin/settings');
    },
    showSnackbar(text, color = 'success') {
      this.snackbar.text = text;
      this.snackbar.color = color;
      this.snackbar.show = true;
    }
  },
  mounted() {
    this.fetchDashboardStats();
  }
}
</script>

<style scoped>
.admin-dashboard {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.stat-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 12px;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 25px 0 rgba(0, 0, 0, 0.05);
}

.content-card {
  border-radius: 12px;
  overflow: hidden;
}

:deep(.v-btn) {
  text-transform: none;
  font-weight: 500;
  letter-spacing: 0.5px;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .admin-dashboard {
    padding: 1rem !important;
  }
}
</style>
