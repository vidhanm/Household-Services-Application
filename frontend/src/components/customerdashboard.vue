<template>
  <v-container fluid class="dashboard-container pa-6">
    <!-- Search and Filter Section -->
    <v-row class="mb-6">
      <v-col cols="12" md="6">
        <h1 class="text-h4 font-weight-bold mb-2">Find Services</h1>
        <p class="text-subtitle-1 text-medium-emphasis">Discover the perfect service for your needs</p>
      </v-col>
      <v-col cols="12" md="6">
        <v-row>
          <v-col cols="8">
            <v-text-field
              v-model="searchQuery"
              prepend-inner-icon="mdi-magnify"
              label="Search services..."
              variant="outlined"
              density="comfortable"
              hide-details
              @input="filterServices"
            ></v-text-field>
          </v-col>
          <v-col cols="4">
            <v-select
              v-model="selectedCategory"
              :items="categories"
              label="Category"
              variant="outlined"
              density="comfortable"
              hide-details
              @update:model-value="filterServices"
            ></v-select>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <!-- Services Grid -->
    <v-row>
      <v-col v-for="service in filteredServices" :key="service.id" cols="12" sm="6" md="4" lg="3">
        <v-card class="service-card h-100" elevation="2" rounded="lg">
          <!-- Service Image -->
          <v-img
            :src="getServiceImage(service.name)"
            height="200"
            cover
            class="align-end"
          >
            <v-card-title class="text-white px-4 pb-4 service-title-overlay">
              {{ service.name }}
            </v-card-title>
          </v-img>

          <v-card-text class="pt-4">
            <!-- Rating -->
            <div class="d-flex flex-column mb-3">
              <div class="d-flex align-center mb-1">
                <v-rating
                  v-model="service.rating"
                  readonly
                  half-increments
                  :length="5"
                  active-color="warning"
                  background-color="warning-lighten-3"
                  hover
                >
                  <template #item="props">
                    <v-icon
                      :color="props.isFilled ? 'warning' : 'warning-lighten-3'"
                      :icon="props.isFilled ? 'mdi-star' : 'mdi-star-outline'"
                      :size="20"
                    />
                  </template>
                </v-rating>
                <span class="text-subtitle-2 ml-2 font-weight-medium" :class="getRatingColor(service.rating)">
                  {{ service.rating ? service.rating.toFixed(1) : 'New' }}
                </span>
              </div>
              <div class="d-flex align-center">
                <span class="text-caption text-medium-emphasis">
                  {{ service.ratingCount || 0 }} {{ service.ratingCount === 1 ? 'review' : 'reviews' }}
                </span>
                <v-tooltip location="bottom" v-if="service.rating">
                  <template #activator="{ props }">
                    <v-icon
                      icon="mdi-information"
                      size="14"
                      class="ml-1"
                      color="primary"
                      v-bind="props"
                    />
                  </template>
                  <div class="pa-2">
                    <div class="text-subtitle-2 mb-1">Rating Breakdown</div>
                    <div class="d-flex align-center text-caption">
                      <v-progress-linear
                        model-value="70"
                        color="warning"
                        height="4"
                        class="mx-2"
                        style="width: 50px"
                      />
                      <span>{{ Math.round(service.rating * 20) }}% positive</span>
                    </div>
                  </div>
                </v-tooltip>
              </div>
            </div>

            <!-- Price -->
            <div class="d-flex align-center justify-space-between mb-2">
              <div>
                <span class="text-h6 font-weight-bold">₹{{ service.price }}</span>
                <span class="text-subtitle-2 text-medium-emphasis">/service</span>
              </div>
              <v-chip
                color="success"
                size="small"
                variant="tonal"
              >
                Available
              </v-chip>
            </div>

            <!-- Description -->
            <p class="text-body-2 text-medium-emphasis mb-4">
              {{ getServiceDescription(service.name) }}
            </p>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions class="pa-4">
            <v-btn
              block
              color="primary"
              variant="elevated"
              @click="selectService(service)"
              :elevation="0"
              class="text-none"
            >
              Book Now
              <v-icon icon="mdi-arrow-right" class="ml-2"></v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- No Results -->
    <v-row v-if="filteredServices.length === 0" justify="center" class="mt-8">
      <v-col cols="12" class="text-center">
        <v-icon icon="mdi-file-search-outline" size="64" color="grey-lighten-1"></v-icon>
        <h3 class="text-h6 mt-4">No services found</h3>
        <p class="text-subtitle-1 text-medium-emphasis">Try adjusting your search or filters</p>
      </v-col>
    </v-row>

    <!-- Booking Modal -->
    <booking-modal
      v-model="showBookingModal"
      :service="selectedService"
      @confirm-booking="addToCartHandler"
      @cancel="closeBookingModal"
    ></booking-modal>

    <!-- Success Snackbar -->
    <v-snackbar
      v-model="showSnackbar"
      :color="snackbarColor"
      location="top"
      :timeout="3000"
    >
      {{ snackbarText }}
    </v-snackbar>
  </v-container>
</template>

<script>
import BookingModal from './BookingModal.vue';

export default {
  components: {
    BookingModal
  },
  inject: ['updateCart', 'addToCart'],
  data() {
    return {
      services: [],
      searchQuery: '',
      selectedCategory: 'All',
      categories: ['All', 'Cleaning', 'Repair', 'Maintenance', 'Installation'],
      showBookingModal: false,
      selectedService: null,
      showSnackbar: false,
      snackbarText: '',
      snackbarColor: 'success',
    };
  },
  computed: {
    filteredServices() {
      let filtered = [...this.services];
      
      // Apply search filter
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(service => 
          service.name.toLowerCase().includes(query)
        );
      }

      // Apply category filter
      if (this.selectedCategory && this.selectedCategory !== 'All') {
        filtered = filtered.filter(service => 
          this.getServiceCategory(service.name) === this.selectedCategory
        );
      }

      return filtered;
    }
  },
  methods: {
    getServiceImage(serviceName) {
      const images = {
        'Home cleaner': 'https://images.unsplash.com/photo-1581578731548-c64695cc6952',
        'Plumber': 'https://images.unsplash.com/photo-1600566752355-35792bedcfea',
        'Carpenter': 'https://images.unsplash.com/photo-1588544621848-6244f38b8e0b',
        // Add more service images here
      };
      return images[serviceName] || 'https://images.unsplash.com/photo-1517646287270-a5a9ca602e5c';
    },
    getServiceDescription(serviceName) {
      const descriptions = {
        'Home cleaner': 'Professional home cleaning services for a spotless living space.',
        'Plumber': 'Expert plumbing services for repairs, installations, and maintenance.',
        'Carpenter': 'Skilled carpentry work for furniture repair and custom woodwork.',
        // Add more service descriptions here
      };
      return descriptions[serviceName] || 'Professional service at your doorstep.';
    },
    getServiceCategory(serviceName) {
      const categories = {
        'Home cleaner': 'Cleaning',
        'Plumber': 'Repair',
        'Carpenter': 'Maintenance',
        // Add more service categories here
      };
      return categories[serviceName] || 'Other';
    },
    selectService(service) {
      this.selectedService = service;
      this.showBookingModal = true;
    },
    addToCartHandler(bookingDetails) {
      this.addToCart(bookingDetails);
      this.showBookingModal = false;
      this.showSnackbar = true;
      this.snackbarText = 'Service added to cart successfully!';
      this.snackbarColor = 'success';
    },
    closeBookingModal() {
      console.log("close booking modal called")
      this.showBookingModal = false;
      this.$nextTick(() => {
    this.selectedService = null;
  });
    },
    filterServices() {
      // The filtering is handled by the computed property
    },
    getRatingColor(rating) {
      if (!rating) return 'text-medium-emphasis';
      if (rating >= 4.5) return 'success--text';
      if (rating >= 4.0) return 'warning--text';
      if (rating >= 3.0) return 'orange--text';
      return 'error--text';
    },
    async fetchServices() {
      try {
        const response = await fetch('http://localhost:5000/customer/services/search', {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token'),
            'Accept': 'application/json'
          }
        });
        
        if (!response.ok) {
          throw new Error('Failed to fetch services');
        }
        
        const data = await response.json();
        
        if (Array.isArray(data)) {
          this.services = data.map(service => ({
            ...service,
            rating: service.rating || 0,
            ratingCount: service.ratingCount || 0
          }));
        }
      } catch (error) {
        console.error('Error fetching services:', error);
        this.showSnackbar = true;
        this.snackbarText = 'Failed to load services. Please try again.';
        this.snackbarColor = 'error';
      }
    }
  },
  mounted() {
    this.fetchServices();
  }
};
</script>

<style scoped>
.dashboard-container {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.service-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden;
}

.service-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 25px 0 rgba(0, 0, 0, 0.1) !important;
}

.service-title-overlay {
  background: linear-gradient(to top, rgba(0, 0, 0, 0.7) 0%, rgba(0, 0, 0, 0) 100%);
  width: 100%;
}

:deep(.v-card-title) {
  line-height: 1.4;
}

.v-btn {
  text-transform: none;
  font-weight: 600;
}

:deep(.v-field) {
  border-radius: 8px;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .dashboard-container {
    padding: 1rem !important;
  }
}
</style>