<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12">
          <v-card>
            <v-card-title>Rejected Requests</v-card-title>
            <v-card-text>
              <v-list>
                <v-list-item v-for="request in rejectedRequests" :key="request.id">
                  <v-list-item-content>
                    <v-list-item-title class="text-h6">
                      Service Request #{{ request.service_id }}
                    </v-list-item-title>
                    <v-list-item-subtitle class="mt-2">
                      <strong>Customer ID:</strong> {{ request.customer_id }}
                    </v-list-item-subtitle>
                    <v-list-item-subtitle>
                      <strong>Date Rejected:</strong> {{ new Date(request.date_of_request).toLocaleString() }}
                    </v-list-item-subtitle>
                    <v-list-item-subtitle>
                      <strong>Status:</strong> 
                      <v-chip small color="error" text-color="white">
                        {{ request.status }}
                      </v-chip>
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  export default {
    data() {
      return {
        rejectedRequests: [],
        refreshInterval: null
      };
    },
    methods: {
      async fetchRejectedRequests() {
        try {
          const response = await fetch('http://localhost:5000/professional/dashboard', {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
          });
  
          if (!response.ok) {
            throw new Error('Failed to fetch requests');
          }
  
          const data = await response.json();
          this.rejectedRequests = data.rejected_requests || [];
        } catch (error) {
          console.error('Error fetching rejected requests:', error);
        }
      }
    },
    mounted() {
      this.fetchRejectedRequests();
      this.refreshInterval = setInterval(this.fetchRejectedRequests, 30000);
    },
    beforeDestroy() {
      if (this.refreshInterval) {
        clearInterval(this.refreshInterval);
      }
    }
  };
  </script>