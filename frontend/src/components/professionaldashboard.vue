<template>
  <v-container fluid class="dashboard-container pa-6">
    <v-row class="mb-6">
      <v-col cols="12" md="8">
        <h1 class="text-h4 font-weight-bold mb-2">Service Requests</h1>
        <p class="text-subtitle-1 text-medium-emphasis">Manage your service requests and bookings</p>
      </v-col>
      <v-col cols="12" md="4" class="d-flex align-center justify-end">
        <v-chip-group
          v-model="activeView"
          mandatory
          selected-class="primary"
        >
          <v-chip
            filter
            variant="elevated"
            value="home"
            :class="{ 'custom-chip': true, 'active-chip': activeView === 'home' }"
          >
            <v-icon start icon="mdi-clock-outline" size="18"></v-icon>
            Pending ({{ pendingRequests.length }})
          </v-chip>
          <v-chip
            filter
            variant="elevated"
            value="accepted"
            :class="{ 'custom-chip': true, 'active-chip': activeView === 'accepted' }"
          >
            <v-icon start icon="mdi-check-circle" size="18"></v-icon>
            Accepted ({{ acceptedRequests.length }})
          </v-chip>
          <v-chip
            filter
            variant="elevated"
            value="rejected"
            :class="{ 'custom-chip': true, 'active-chip': activeView === 'rejected' }"
          >
            <v-icon start icon="mdi-close-circle" size="18"></v-icon>
            Rejected ({{ rejectedRequests.length }})
          </v-chip>
        </v-chip-group>
      </v-col>
    </v-row>

    <!-- Stats Cards -->
    <v-row class="mb-6">
      <v-col cols="12" sm="4">
        <v-card class="stat-card">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <div class="text-subtitle-2 text-medium-emphasis mb-1">Pending Requests</div>
                <div class="text-h4 font-weight-bold">{{ pendingRequests.length }}</div>
              </div>
              <v-avatar color="primary" size="48" class="elevation-1">
                <v-icon icon="mdi-clock-outline" size="24" color="white"></v-icon>
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card class="stat-card">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <div class="text-subtitle-2 text-medium-emphasis mb-1">Accepted Jobs</div>
                <div class="text-h4 font-weight-bold">{{ acceptedRequests.length }}</div>
              </div>
              <v-avatar color="success" size="48" class="elevation-1">
                <v-icon icon="mdi-check-circle" size="24" color="white"></v-icon>
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card class="stat-card">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <div class="text-subtitle-2 text-medium-emphasis mb-1">Total Earnings</div>
                <div class="text-h4 font-weight-bold">₹{{ calculateTotalEarnings() }}</div>
              </div>
              <v-avatar color="info" size="48" class="elevation-1">
                <v-icon icon="mdi-currency-inr" size="24" color="white"></v-icon>
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Request Lists -->
    <v-card class="request-card">
      <!-- Pending Requests -->
      <div v-if="activeView === 'home'">
        <v-card-title class="d-flex align-center py-4 px-6">
          <v-icon icon="mdi-clock-outline" color="primary" class="mr-2" size="24"></v-icon>
          Pending Requests
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-0">
          <v-list v-if="pendingRequests.length > 0">
            <template v-for="(request, index) in pendingRequests" :key="request.id">
              <v-list-item
                :class="{ 'list-item-hover': true }"
              >
                <template v-slot:prepend>
                  <v-avatar color="primary" variant="tonal">
                    <v-icon icon="mdi-account"></v-icon>
                  </v-avatar>
                </template>

                <v-list-item-title class="font-weight-medium mb-1">
                  Service Request #{{ request.service_id }}
                </v-list-item-title>
                
                <v-list-item-subtitle>
                  <v-icon icon="mdi-account" size="16" class="mr-1"></v-icon>
                  Customer ID: {{ request.customer_id }}
                </v-list-item-subtitle>
                
                <v-list-item-subtitle>
                  <v-icon icon="mdi-calendar" size="16" class="mr-1"></v-icon>
                  {{ new Date(request.date_of_request).toLocaleString() }}
                </v-list-item-subtitle>

                <template v-slot:append>
                  <div class="d-flex gap-2">
                    <v-btn
                      @click="handleRequest(request.id, 'accept')"
                      color="success"
                      variant="tonal"
                      size="small"
                    >
                      <v-icon icon="mdi-check" size="20" class="mr-1"></v-icon>
                      Accept
                    </v-btn>
                    <v-btn
                      @click="handleRequest(request.id, 'reject')"
                      color="error"
                      variant="tonal"
                      size="small"
                    >
                      <v-icon icon="mdi-close" size="20" class="mr-1"></v-icon>
                      Reject
                    </v-btn>
                  </div>
                </template>
              </v-list-item>
              <v-divider v-if="index < pendingRequests.length - 1"></v-divider>
            </template>
          </v-list>
          <div v-else class="pa-6 text-center">
            <v-icon icon="mdi-tray-check" size="64" color="grey-lighten-1"></v-icon>
            <div class="text-h6 mt-4">No Pending Requests</div>
            <p class="text-medium-emphasis">You're all caught up!</p>
          </div>
        </v-card-text>
      </div>

      <!-- Accepted Requests -->
      <div v-if="activeView === 'accepted'">
        <v-card-title class="d-flex align-center py-4 px-6">
          <v-icon icon="mdi-check-circle" color="success" class="mr-2" size="24"></v-icon>
          Accepted Requests
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-0">
          <v-list v-if="acceptedRequests.length > 0">
            <template v-for="(request, index) in acceptedRequests" :key="request.id">
              <v-list-item>
                <template v-slot:prepend>
                  <v-avatar color="success" variant="tonal">
                    <v-icon icon="mdi-account"></v-icon>
                  </v-avatar>
                </template>

                <v-list-item-title class="font-weight-medium mb-1">
                  Service Request #{{ request.service_id }}
                </v-list-item-title>
                
                <v-list-item-subtitle>
                  <v-icon icon="mdi-account" size="16" class="mr-1"></v-icon>
                  Customer ID: {{ request.customer_id }}
                </v-list-item-subtitle>
                
                <v-list-item-subtitle>
                  <v-icon icon="mdi-calendar" size="16" class="mr-1"></v-icon>
                  {{ new Date(request.date_of_request).toLocaleString() }}
                </v-list-item-subtitle>

                <template v-slot:append>
                  <v-chip color="success" size="small">Accepted</v-chip>
                </template>
              </v-list-item>
              <v-divider v-if="index < acceptedRequests.length - 1"></v-divider>
            </template>
          </v-list>
          <div v-else class="pa-6 text-center">
            <v-icon icon="mdi-clipboard-check" size="64" color="grey-lighten-1"></v-icon>
            <div class="text-h6 mt-4">No Accepted Requests</div>
            <p class="text-medium-emphasis">You haven't accepted any requests yet</p>
          </div>
        </v-card-text>
      </div>

      <!-- Rejected Requests -->
      <div v-if="activeView === 'rejected'">
        <v-card-title class="d-flex align-center py-4 px-6">
          <v-icon icon="mdi-close-circle" color="error" class="mr-2" size="24"></v-icon>
          Rejected Requests
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-0">
          <v-list v-if="rejectedRequests.length > 0">
            <template v-for="(request, index) in rejectedRequests" :key="request.id">
              <v-list-item>
                <template v-slot:prepend>
                  <v-avatar color="error" variant="tonal">
                    <v-icon icon="mdi-account"></v-icon>
                  </v-avatar>
                </template>

                <v-list-item-title class="font-weight-medium mb-1">
                  Service Request #{{ request.service_id }}
                </v-list-item-title>
                
                <v-list-item-subtitle>
                  <v-icon icon="mdi-account" size="16" class="mr-1"></v-icon>
                  Customer ID: {{ request.customer_id }}
                </v-list-item-subtitle>
                
                <v-list-item-subtitle>
                  <v-icon icon="mdi-calendar" size="16" class="mr-1"></v-icon>
                  {{ new Date(request.date_of_request).toLocaleString() }}
                </v-list-item-subtitle>

                <template v-slot:append>
                  <v-chip color="error" size="small">Rejected</v-chip>
                </template>
              </v-list-item>
              <v-divider v-if="index < rejectedRequests.length - 1"></v-divider>
            </template>
          </v-list>
          <div v-else class="pa-6 text-center">
            <v-icon icon="mdi-clipboard-remove" size="64" color="grey-lighten-1"></v-icon>
            <div class="text-h6 mt-4">No Rejected Requests</div>
            <p class="text-medium-emphasis">You haven't rejected any requests</p>
          </div>
        </v-card-text>
      </div>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      activeView: 'home',
      pendingRequests: [],
      acceptedRequests: [],
      rejectedRequests: []
    };
  },
  methods: {
    calculateTotalEarnings() {
      // This is a placeholder calculation - adjust based on your actual data structure
      return this.acceptedRequests.reduce((total, request) => total + (request.price || 0), 0);
    },
    async fetchRequests() {
      try {
        const response = await fetch('http://localhost:5000/professional/dashboard', {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch requests');
        }

        const data = await response.json();
        this.pendingRequests = data.pending_requests || [];
        this.acceptedRequests = data.accepted_requests || [];
        this.rejectedRequests = data.rejected_requests || [];
      } catch (error) {
        console.error('Error fetching requests:', error);
      }
    },
    async handleRequest(requestId, action) {
      try {
        const response = await fetch('http://localhost:5000/professional/dashboard', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Accept': 'application/json',
          },
          body: JSON.stringify({
            request_id: requestId,
            action: action,
          }),
        });

        if (!response.ok) {
          throw new Error(`Failed to ${action} request`);
        }

        await this.fetchRequests();
      } catch (error) {
        console.error(`Error ${action}ing request:`, error);
      }
    },
  },
  mounted() {
    this.fetchRequests();
  },
  watch: {
    '$route.query.view': {
      immediate: true,
      handler(newView) {
        if (newView === 'rejected') {
          this.activeView = 'rejected';
        } else if (newView === 'accepted') {
          this.activeView = 'accepted';
        } else {
          this.activeView = 'home';
        }
      }
    }
  }
};
</script>

<style scoped>
.dashboard-container {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.custom-chip {
  font-weight: 500;
  transition: all 0.3s ease;
}

.active-chip {
  transform: scale(1.05);
}

.stat-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 12px;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 25px 0 rgba(0, 0, 0, 0.05);
}

.request-card {
  border-radius: 12px;
  overflow: hidden;
}

.list-item-hover {
  transition: background-color 0.3s ease;
}

.list-item-hover:hover {
  background-color: rgb(var(--v-theme-surface-variant));
}

:deep(.v-list-item) {
  padding: 16px;
}

:deep(.v-btn) {
  text-transform: none;
  font-weight: 500;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .dashboard-container {
    padding: 1rem !important;
  }
  
  :deep(.v-chip-group) {
    justify-content: center;
  }
}
</style>