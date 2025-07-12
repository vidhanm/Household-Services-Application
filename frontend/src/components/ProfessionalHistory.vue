<template>
  <v-container fluid class="history-page pa-6">
    <!-- Header Section -->
    <v-row class="mb-6">
      <v-col cols="12">
        <h1 class="text-h4 font-weight-bold mb-2">Service History</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          View your completed service requests and customer feedback
        </p>
      </v-col>
    </v-row>

    <!-- Stats Cards -->
    <v-row class="mb-6">
      <v-col cols="12" sm="4">
        <v-card class="stat-card">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <div class="text-subtitle-2 text-medium-emphasis mb-1">Completed Services</div>
                <div class="text-h4 font-weight-bold">{{ completedServices.length }}</div>
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
                <div class="text-subtitle-2 text-medium-emphasis mb-1">Average Rating</div>
                <div class="text-h4 font-weight-bold">{{ averageRating.toFixed(1) }}</div>
              </div>
              <v-avatar color="warning" size="48" class="elevation-1">
                <v-icon icon="mdi-star" size="24" color="white"></v-icon>
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
                <div class="text-h4 font-weight-bold">₹{{ formatNumber(totalEarnings) }}</div>
              </div>
              <v-avatar color="info" size="48" class="elevation-1">
                <v-icon icon="mdi-currency-inr" size="24" color="white"></v-icon>
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Filter Controls -->
    <v-card class="mb-6 rounded-lg">
      <v-card-text class="py-4">
        <v-row align="center">
          <v-col cols="12" sm="4">
            <v-text-field
              v-model="search"
              prepend-inner-icon="mdi-magnify"
              label="Search by customer or service"
              density="comfortable"
              variant="outlined"
              hide-details
              clearable
            ></v-text-field>
          </v-col>
          
          <v-col cols="12" sm="3">
            <v-select
              v-model="serviceFilter"
              label="Service Type"
              :items="serviceTypes"
              variant="outlined"
              density="comfortable"
              hide-details
              clearable
            ></v-select>
          </v-col>
          
          <v-col cols="12" sm="3">
            <v-menu
              ref="dateMenu"
              v-model="dateMenu"
              :close-on-content-click="false"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ props }">
                <v-text-field
                  v-model="dateRangeText"
                  label="Date Range"
                  prepend-inner-icon="mdi-calendar"
                  readonly
                  v-bind="props"
                  variant="outlined"
                  density="comfortable"
                  hide-details
                  clearable
                  @click:clear="clearDateFilter"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="dateRange"
                range
                @update:model-value="dateMenu = false"
              ></v-date-picker>
            </v-menu>
          </v-col>
          
          <v-col cols="12" sm="2">
            <v-btn
              color="primary"
              variant="tonal"
              block
              @click="resetFilters"
              prepend-icon="mdi-filter-off"
            >
              Reset Filters
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- History List -->
    <v-card class="history-card rounded-lg">
      <v-card-title class="d-flex align-center py-4 px-6">
        <v-icon icon="mdi-history" color="primary" class="mr-2" size="24"></v-icon>
        Completed Services
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          variant="text"
          prepend-icon="mdi-download"
          @click="exportHistory"
          :disabled="filteredServices.length === 0"
        >
          Export
        </v-btn>
      </v-card-title>
      
      <v-divider></v-divider>

      <v-data-table
        :headers="headers"
        :items="filteredServices"
        :search="search"
        :loading="loading"
        class="elevation-0"
      >
        <template v-slot:item.service_type="{ item }">
          <div class="d-flex align-center">
            <v-avatar size="32" color="primary" class="mr-2">
              <v-icon size="16" color="white">{{ getServiceIcon(item.service_type) }}</v-icon>
            </v-avatar>
            {{ item.service_type }}
          </div>
        </template>

        <template v-slot:item.date_of_request="{ item }">
          {{ formatDate(item.date_of_request) }}
        </template>

        <template v-slot:item.price="{ item }">
          <span class="font-weight-medium">₹{{ formatNumber(item.price) }}</span>
        </template>

        <template v-slot:item.rating="{ item }">
          <v-rating
            :model-value="item.rating || 0"
            color="amber"
            density="compact"
            half-increments
            readonly
            size="small"
          ></v-rating>
          <span class="text-caption ml-2">{{ item.rating ? item.rating.toFixed(1) : 'N/A' }}</span>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn
            icon="mdi-eye"
            variant="text"
            density="comfortable"
            color="primary"
            @click="viewServiceDetails(item)"
            size="small"
          ></v-btn>
        </template>

        <template v-slot:no-data>
          <div class="text-center py-6">
            <v-icon icon="mdi-history-off" size="64" color="grey-lighten-1"></v-icon>
            <div class="text-h6 mt-4">No Service History</div>
            <p class="text-medium-emphasis">You don't have any completed services yet</p>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- Service Details Dialog -->
    <v-dialog v-model="detailsDialog" max-width="700px">
      <v-card v-if="selectedService" class="rounded-lg">
        <v-card-title class="d-flex align-center py-3 px-6">
          <v-icon icon="mdi-clipboard-text" color="primary" class="mr-2"></v-icon>
          Service Details
          <v-spacer></v-spacer>
          <v-btn icon="mdi-close" variant="text" @click="detailsDialog = false"></v-btn>
        </v-card-title>
        
        <v-divider></v-divider>
        
        <v-card-text class="pa-4">
          <v-row>
            <v-col cols="12" sm="6">
              <div class="text-subtitle-2 text-grey-darken-1">Service Type</div>
              <div class="text-h6 mb-3">{{ selectedService.service_type }}</div>
              
              <div class="text-subtitle-2 text-grey-darken-1">Customer</div>
              <div class="text-h6 mb-3">{{ selectedService.customer_name }}</div>
              
              <div class="text-subtitle-2 text-grey-darken-1">Date Completed</div>
              <div class="text-h6 mb-3">{{ formatDate(selectedService.date_of_request) }}</div>
            </v-col>
            
            <v-col cols="12" sm="6">
              <div class="text-subtitle-2 text-grey-darken-1">Service ID</div>
              <div class="text-h6 mb-3">#{{ selectedService.id }}</div>
              
              <div class="text-subtitle-2 text-grey-darken-1">Amount</div>
              <div class="text-h6 mb-3">₹{{ formatNumber(selectedService.price) }}</div>
              
              <div class="text-subtitle-2 text-grey-darken-1">Duration</div>
              <div class="text-h6 mb-3">{{ selectedService.duration }} minutes</div>
            </v-col>
            
            <v-col cols="12">
              <div class="text-subtitle-2 text-grey-darken-1">Rating</div>
              <div class="d-flex align-center mb-3">
                <v-rating
                  :model-value="selectedService.rating || 0"
                  color="amber"
                  half-increments
                  readonly
                ></v-rating>
                <span class="ml-2 text-h6">{{ selectedService.rating ? selectedService.rating.toFixed(1) : 'N/A' }}</span>
              </div>
            </v-col>
            
            <v-col cols="12">
              <div class="text-subtitle-2 text-grey-darken-1">Feedback</div>
              <div class="text-body-1 pa-3 bg-grey-lighten-4 rounded-lg">
                {{ selectedService.feedback || 'No feedback provided' }}
              </div>
            </v-col>
          </v-row>
        </v-card-text>
        
        <v-divider></v-divider>
        
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn variant="elevated" color="primary" @click="detailsDialog = false">
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
export default {
  name: 'ProfessionalHistory',
  data() {
    return {
      loading: true,
      completedServices: [],
      serviceTypes: [],
      search: '',
      serviceFilter: null,
      dateRange: [],
      dateMenu: false,
      detailsDialog: false,
      selectedService: null,
      headers: [
        { title: 'Service', key: 'service_type' },
        { title: 'Customer', key: 'customer_name' },
        { title: 'Date Completed', key: 'date_of_request' },
        { title: 'Amount', key: 'price' },
        { title: 'Rating', key: 'rating' },
        { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
      ]
    };
  },
  computed: {
    dateRangeText() {
      if (this.dateRange.length === 2) {
        return `${this.formatDate(this.dateRange[0])} to ${this.formatDate(this.dateRange[1])}`;
      }
      return '';
    },
    
    filteredServices() {
      let filtered = [...this.completedServices];
      
      // Apply service type filter
      if (this.serviceFilter) {
        filtered = filtered.filter(service => service.service_type === this.serviceFilter);
      }
      
      // Apply date range filter
      if (this.dateRange.length === 2) {
        const startDate = new Date(this.dateRange[0]);
        const endDate = new Date(this.dateRange[1]);
        endDate.setHours(23, 59, 59); // Include the whole end date
        
        filtered = filtered.filter(service => {
          const serviceDate = new Date(service.date_of_request);
          return serviceDate >= startDate && serviceDate <= endDate;
        });
      }
      
      return filtered;
    },
    
    totalEarnings() {
      return this.completedServices.reduce((total, service) => total + (service.price || 0), 0);
    },
    
    averageRating() { 
      const ratedServices = this.completedServices.filter(service => service.rating);
      if (ratedServices.length === 0) return 0;
      
      const sum = ratedServices.reduce((total, service) => total + service.rating, 0);
      return sum / ratedServices.length;
    }
  },
  methods: {
    formatNumber(value) {
      return new Intl.NumberFormat('en-IN').format(value || 0);
    },
    
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    
    getServiceIcon(serviceName) {
      const icons = {
        'Plumber': 'mdi-water-pump',
        'Electrical Work': 'mdi-lightning-bolt',
        'Carpenter': 'mdi-hammer',
        'Home Cleaning': 'mdi-broom',
        'Painter': 'mdi-paint',
        'Beauty and Spa': 'mdi-spa',
        'Fitness and Yoga': 'mdi-yoga',
        'Pest Control': 'mdi-bug',
        'Interior Design': 'mdi-floor-plan',
        'AC Repair': 'mdi-air-conditioner',
        'Saloon': 'mdi-content-cut',
        'Massage': 'mdi-hand-heart'
      };
      return icons[serviceName] || 'mdi-briefcase';
    },
    
    resetFilters() {
      this.search = '';
      this.serviceFilter = null;
      this.dateRange = [];
    },
    
    clearDateFilter() {
      this.dateRange = [];
    },
    
    viewServiceDetails(service) {
      this.selectedService = service;
      this.detailsDialog = true;
    },
    
    async fetchServiceHistory() {
      this.loading = true;
      try {
        const response = await fetch('http://localhost:5000/professional/history', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          }
        });
        
        if (!response.ok) {
          throw new Error('Failed to fetch service history');
        }
        
        const data = await response.json();
        this.completedServices = data.completed_services || [];
        
        // Process the data to handle potential missing fields
        this.completedServices = this.completedServices.map(service => {
          return {
            ...service,
            // Set defaults for potentially missing fields
            duration: service.duration || 0,
            rating: service.rating || 0,
            feedback: service.feedback || ''
          };
        });
        
        // Extract unique service types for filter
        const types = new Set(this.completedServices.map(service => service.service_type));
        this.serviceTypes = [...types];
        
      } catch (error) {
        console.error('Error fetching service history:', error);
        this.$emit('show-snackbar', {
          text: 'Failed to load service history',
          color: 'error'
        });
      } finally {
        this.loading = false;
      }
    },
    
    exportHistory() {
      // Simple CSV export of filtered services
      if (this.filteredServices.length === 0) return;
      
      const headers = ['Service ID', 'Service Type', 'Customer', 'Date', 'Amount', 'Rating', 'Feedback'];
      const csvContent = [
        headers.join(','),
        ...this.filteredServices.map(service => [
          service.id,
          service.service_type,
          service.customer_name,
          this.formatDate(service.date_of_request),
          service.price,
          service.rating || 'N/A',
          (service.feedback || 'No feedback').replace(/,/g, ';') // Replace commas in feedback
        ].join(','))
      ].join('\n');
      
      // Create download link
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', `service_history_${new Date().toISOString().slice(0, 10)}.csv`);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  },
  mounted() {
    this.fetchServiceHistory();
  }
};
</script>

<style scoped>
.history-page {
  background-color: var(--bg-secondary, #f8f9fa);
  min-height: 100vh;
}

.stat-card, .history-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 12px;
  overflow: hidden;
  background-color: var(--card-bg, white);
  border: 1px solid var(--border-color, #e0e0e0);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 25px 0 rgba(0, 0, 0, 0.05);
}

.v-card-title {
  font-size: 1.1rem;
  font-weight: 600;
}

:deep(.v-data-table) {
  background: var(--card-bg, white);
}

:deep(.v-data-table__tr:hover) {
  background-color: var(--hover-color, rgba(0, 0, 0, 0.03));
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .history-page {
    padding: 16px !important;
  }
}
</style> 