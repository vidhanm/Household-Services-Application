<template>
  <v-container fluid class="analytics-dashboard pa-6">
    <!-- Header Section -->
    <v-row class="mb-6">
      <v-col cols="12">
        <h1 class="text-h4 font-weight-bold mb-2">Analytics Dashboard</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Comprehensive insights and metrics for your business
        </p>
      </v-col>
    </v-row>

    <!-- Loading Indicator -->
    <v-row v-if="loading" justify="center" class="my-12">
      <v-progress-circular indeterminate size="64" color="primary"></v-progress-circular>
    </v-row>

    <template v-else>
      <!-- Summary Stats -->
      <v-row class="mb-6">
        <v-col cols="12" sm="6" md="3">
          <v-card class="stat-card">
            <v-card-text>
              <div class="d-flex justify-space-between align-center">
                <div>
                  <div class="text-subtitle-2 text-medium-emphasis mb-1">Total Users</div>
                  <div class="text-h4 font-weight-bold">{{ dashboardStats.total_users }}</div>
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
                  <div class="text-h4 font-weight-bold">{{ dashboardStats.pending_verifications }}</div>
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
                  <div class="text-h4 font-weight-bold">{{ dashboardStats.active_services }}</div>
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
                  <div class="text-h4 font-weight-bold">₹{{ formatNumber(dashboardStats.total_revenue) }}</div>
                </div>
                <v-avatar color="info" size="48" class="elevation-1">
                  <v-icon icon="mdi-currency-inr" size="24" color="white"></v-icon>
                </v-avatar>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- First Row Charts -->
      <v-row class="mb-6">
        <!-- User Growth Chart -->
        <v-col cols="12" md="8">
          <v-card class="chart-card">
            <v-card-title class="d-flex align-center py-3 px-6">
              <v-icon icon="mdi-trending-up" color="primary" class="mr-2"></v-icon>
              User Registration Growth
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-4">
              <canvas ref="userGrowthChart" height="300"></canvas>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- User Roles Distribution -->
        <v-col cols="12" md="4">
          <v-card class="chart-card">
            <v-card-title class="d-flex align-center py-3 px-6">
              <v-icon icon="mdi-account-multiple" color="primary" class="mr-2"></v-icon>
              User Distribution
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-4">
              <canvas ref="userRolesChart" height="300"></canvas>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Second Row Charts -->
      <v-row class="mb-6">
        <!-- Popular Services -->
        <v-col cols="12" md="6">
          <v-card class="chart-card">
            <v-card-title class="d-flex align-center py-3 px-6">
              <v-icon icon="mdi-star" color="amber-darken-2" class="mr-2"></v-icon>
              Popular Services
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-4">
              <canvas ref="popularServicesChart" height="300"></canvas>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Service Revenue Analysis -->
        <v-col cols="12" md="6">
          <v-card class="chart-card">
            <v-card-title class="d-flex align-center py-3 px-6">
              <v-icon icon="mdi-cash-multiple" color="success" class="mr-2"></v-icon>
              Service Revenue
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-4">
              <canvas ref="serviceRevenueChart" height="300"></canvas>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Third Row Charts -->
      <v-row class="mb-6">
        <!-- Status Distribution -->
        <v-col cols="12" md="4">
          <v-card class="chart-card">
            <v-card-title class="d-flex align-center py-3 px-6">
              <v-icon icon="mdi-chart-donut" color="deep-purple" class="mr-2"></v-icon>
              Request Status
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-4">
              <canvas ref="statusDistributionChart" height="250"></canvas>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Monthly Revenue Trend -->
        <v-col cols="12" md="8">
          <v-card class="chart-card">
            <v-card-title class="d-flex align-center py-3 px-6">
              <v-icon icon="mdi-chart-line" color="info" class="mr-2"></v-icon>
              Monthly Revenue Trend
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-4">
              <canvas ref="revenueTrendChart" height="250"></canvas>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Top Professionals Table -->
      <v-row>
        <v-col cols="12">
          <v-card class="chart-card">
            <v-card-title class="d-flex align-center py-3 px-6">
              <v-icon icon="mdi-account-star" color="amber-darken-2" class="mr-2"></v-icon>
              Top Performing Professionals
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-0">
              <v-table>
                <thead>
                  <tr>
                    <th class="text-left">Professional</th>
                    <th class="text-center">Average Rating</th>
                    <th class="text-center">Completed Jobs</th>
                    <th class="text-center">Performance</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(pro, index) in analytics.professional_ratings" :key="index">
                    <td>{{ pro.name }}</td>
                    <td class="text-center">
                      <v-rating
                        :model-value="pro.rating"
                        color="amber"
                        density="compact"
                        half-increments
                        readonly
                        size="small"
                      ></v-rating>
                      <span class="text-caption ml-2">{{ pro.rating.toFixed(1) }}</span>
                    </td>
                    <td class="text-center">{{ pro.count }}</td>
                    <td class="text-center">
                      <v-chip
                        :color="getRatingColor(pro.rating)"
                        size="small"
                        text-color="white"
                      >
                        {{ getRatingLabel(pro.rating) }}
                      </v-chip>
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </v-container>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  name: 'AdminAnalytics',
  data() {
    return {
      loading: true,
      charts: {},
      dashboardStats: {
        total_users: 0,
        pending_verifications: 0,
        active_services: 0,
        total_revenue: 0
      },
      analytics: {
        users_growth: [],
        user_roles: [],
        popular_services: [],
        service_revenue: [],
        status_distribution: [],
        professional_ratings: [],
        revenue_trend: []
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
        
        this.dashboardStats = await response.json();
      } catch (error) {
        console.error('Error fetching dashboard stats:', error);
        this.showSnackbar('Failed to load dashboard statistics', 'error');
      }
    },
    
    async fetchAnalytics() {
      try {
        const response = await fetch('http://localhost:5000/admin/analytics/data', {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token'),
            'Accept': 'application/json'
          }
        });
        
        if (!response.ok) {
          throw new Error('Failed to fetch analytics data');
        }
        
        this.analytics = await response.json();
      } catch (error) {
        console.error('Error fetching analytics data:', error);
        this.showSnackbar('Failed to load analytics data', 'error');
        throw error; // Re-throw to be caught in mounted
      }
    },
    
    renderCharts() {
      console.log('renderCharts called');
      // Check that DOM is ready and canvas elements are rendered
      if (this.$refs.userGrowthChart) {
        console.log('Canvas elements found via refs, rendering charts');
        
        // Destroy any existing charts to prevent duplicates
        Object.values(this.charts).forEach(chart => {
          if (chart) chart.destroy();
        });
        
        // Create all charts
        this.createUserGrowthChart();
        this.createUserRolesChart();
        this.createPopularServicesChart();
        this.createServiceRevenueChart();
        this.createStatusDistributionChart();
        this.createRevenueTrendChart();
      } else {
        console.log('Canvas elements not ready yet, retrying in a moment');
        // Retry after a short delay to allow Vue to render the template
        setTimeout(() => this.renderCharts(), 100);
      }
    },
    
    createUserGrowthChart() {
      const ctx = this.$refs.userGrowthChart;
      if (!ctx) {
        console.error('User Growth Chart canvas element not found');
        return;
      }
      
      const labels = this.analytics.users_growth.map(item => this.formatMonth(item.month));
      const data = this.analytics.users_growth.map(item => item.count);
      
      this.charts.userGrowth = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'New Users',
            data: data,
            backgroundColor: 'rgba(66, 133, 244, 0.2)',
            borderColor: 'rgba(66, 133, 244, 1)',
            borderWidth: 2,
            tension: 0.4,
            fill: true,
            pointBackgroundColor: 'rgba(66, 133, 244, 1)',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
            },
            tooltip: {
              mode: 'index',
              intersect: false,
              callbacks: {
                label: (context) => `New Users: ${context.raw}`
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                precision: 0
              }
            }
          }
        }
      });
    },
    
    createUserRolesChart() {
      const ctx = this.$refs.userRolesChart;
      if (!ctx) {
        console.error('User Roles Chart canvas element not found');
        return;
      }
      
      const labels = this.analytics.user_roles.map(item => this.capitalizeFirstLetter(item.role));
      const data = this.analytics.user_roles.map(item => item.count);
      
      this.charts.userRoles = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: [
              'rgba(54, 162, 235, 0.8)',
              'rgba(255, 99, 132, 0.8)',
              'rgba(75, 192, 192, 0.8)',
              'rgba(255, 206, 86, 0.8)'
            ],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'right'
            },
            tooltip: {
              callbacks: {
                label: (context) => {
                  const total = context.dataset.data.reduce((acc, val) => acc + val, 0);
                  const percentage = Math.round((context.raw / total) * 100);
                  return `${context.label}: ${context.raw} (${percentage}%)`;
                }
              }
            }
          }
        }
      });
    },
    
    createPopularServicesChart() {
      const ctx = this.$refs.popularServicesChart;
      if (!ctx) {
        console.error('Popular Services Chart canvas element not found');
        return;
      }
      
      const labels = this.analytics.popular_services.map(item => item.service);
      const data = this.analytics.popular_services.map(item => item.count);
      
      this.charts.popularServices = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Service Requests',
            data: data,
            backgroundColor: 'rgba(255, 159, 64, 0.7)',
            borderColor: 'rgba(255, 159, 64, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y',
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            x: {
              beginAtZero: true,
              ticks: {
                precision: 0
              }
            }
          }
        }
      });
    },
    
    createServiceRevenueChart() {
      const ctx = this.$refs.serviceRevenueChart;
      if (!ctx) {
        console.error('Service Revenue Chart canvas element not found');
        return;
      }
      
      const labels = this.analytics.service_revenue.map(item => item.service);
      const data = this.analytics.service_revenue.map(item => item.revenue);
      
      this.charts.serviceRevenue = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Revenue (₹)',
            data: data,
            backgroundColor: 'rgba(75, 192, 192, 0.7)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: (value) => `₹${this.formatNumber(value)}`
              }
            }
          }
        }
      });
    },
    
    createStatusDistributionChart() {
      const ctx = this.$refs.statusDistributionChart;
      if (!ctx) {
        console.error('Status Distribution Chart canvas element not found');
        return;
      }
      
      const labels = this.analytics.status_distribution.map(item => this.capitalizeFirstLetter(item.status));
      const data = this.analytics.status_distribution.map(item => item.count);
      
      // Define colors for each status
      const backgroundColors = {
        'Requested': 'rgba(255, 193, 7, 0.8)',
        'Accepted': 'rgba(66, 133, 244, 0.8)',
        'In progress': 'rgba(255, 109, 0, 0.8)',
        'Completed': 'rgba(76, 175, 80, 0.8)',
        'Cancelled': 'rgba(244, 67, 54, 0.8)'
      };
      
      const colors = labels.map(label => backgroundColors[label] || 'rgba(189, 189, 189, 0.8)');
      
      this.charts.statusDistribution = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: colors,
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'right',
              labels: {
                boxWidth: 15
              }
            },
            tooltip: {
              callbacks: {
                label: (context) => {
                  const total = context.dataset.data.reduce((acc, val) => acc + val, 0);
                  const percentage = Math.round((context.raw / total) * 100);
                  return `${context.label}: ${context.raw} (${percentage}%)`;
                }
              }
            }
          }
        }
      });
    },
    
    createRevenueTrendChart() {
      const ctx = this.$refs.revenueTrendChart;
      if (!ctx) {
        console.error('Revenue Trend Chart canvas element not found');
        return;
      }
      
      const labels = this.analytics.revenue_trend.map(item => this.formatMonth(item.month));
      const data = this.analytics.revenue_trend.map(item => item.revenue);
      
      this.charts.revenueTrend = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Revenue',
            data: data,
            backgroundColor: 'rgba(26, 115, 232, 0.2)',
            borderColor: 'rgba(26, 115, 232, 1)',
            borderWidth: 2,
            tension: 0.3,
            fill: true,
            pointBackgroundColor: 'rgba(26, 115, 232, 1)',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: (context) => `Revenue: ₹${this.formatNumber(context.raw)}`
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: (value) => `₹${this.formatNumber(value)}`
              }
            }
          }
        }
      });
    },
    
    formatMonth(monthStr) {
      if (!monthStr) return '';
      const [year, month] = monthStr.split('-');
      const date = new Date(year, month - 1);
      return date.toLocaleDateString(undefined, { month: 'short', year: 'numeric' });
    },
    
    formatNumber(value) {
      return new Intl.NumberFormat('en-IN').format(value);
    },
    
    capitalizeFirstLetter(string) {
      if (!string) return '';
      return string.charAt(0).toUpperCase() + string.slice(1);
    },
    
    getRatingColor(rating) {
      if (rating >= 4.5) return 'success';
      if (rating >= 4.0) return 'light-green';
      if (rating >= 3.5) return 'amber';
      if (rating >= 3.0) return 'orange';
      return 'error';
    },
    
    getRatingLabel(rating) {
      if (rating >= 4.5) return 'Excellent';
      if (rating >= 4.0) return 'Very Good';
      if (rating >= 3.5) return 'Good';
      if (rating >= 3.0) return 'Average';
      return 'Poor';
    },
    
    showSnackbar(text, color = 'success') {
      this.$emit('show-snackbar', { text, color });
    }
  },
  async mounted() {
    console.log('Component mounted');
    
    try {
      // Fetch the data first
      await Promise.all([
        this.fetchDashboardStats(),
        this.fetchAnalytics()
      ]);
      
      console.log('Data fetched, setting loading to false');
      // Set loading to false to show the template with canvas elements
      this.loading = false;
      
      // Wait for the DOM to update after loading is set to false
      this.$nextTick(() => {
        console.log('DOM updated, attempting to render charts');
        this.renderCharts();
      });
    } catch (error) {
      console.error('Error initializing dashboard:', error);
      this.loading = false;
      this.showSnackbar('Failed to load dashboard data', 'error');
    }
  },
  beforeUnmount() {
    // Clean up charts
    Object.values(this.charts).forEach(chart => {
      if (chart) chart.destroy();
    });
  }
}
</script>

<style scoped>
.analytics-dashboard {
  background-color: var(--bg-secondary);
  min-height: 100vh;
}

.stat-card, .chart-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 12px;
  overflow: hidden;
  background-color: var(--card-bg);
  border: 1px solid var(--border-color);
}

.stat-card:hover, .chart-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 25px 0 var(--shadow-color);
}

.v-card-title {
  font-size: 1.1rem;
  font-weight: 600;
}

canvas {
  max-width: 100%;
}
</style> 