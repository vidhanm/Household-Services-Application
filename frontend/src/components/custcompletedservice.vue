<template>
    <v-container>
      <v-card>
        <v-card-title>
          Completed Services
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            single-line
            hide-details
          ></v-text-field>
        </v-card-title>
        <v-card-text>
          <v-data-table
            :headers="headers"
            :items="completedServices"
            :search="search"
            :items-per-page="5"
            class="elevation-1"
          >
            <template v-slot:item.price="{ item }">
              ₹{{ item.price }}
            </template>
            
            <template v-slot:item.professional="{ item }">
              <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                  <div v-bind="attrs" v-on="on">
                    {{ item.professionalName }}
                    <v-icon small class="ml-1">mdi-information</v-icon>
                  </div>
                </template>
                <div>
                  <strong>Experience:</strong> {{ item.professional?.experience }} years<br>
                  <strong>Description:</strong> {{ item.professional?.description }}
                </div>
              </v-tooltip>
            </template>
  
            <template v-slot:item.actions="{ item }">
              <v-btn
                small
                color="primary"
                @click="showServiceDetails(item)"
              >
                View Details
              </v-btn>
            </template>
          </v-data-table>
        </v-card-text>
      </v-card>
  
      <!-- Service Details Dialog -->
      <v-dialog v-model="detailsDialog" max-width="500">
        <v-card v-if="selectedService">
          <v-card-title>Service Details</v-card-title>
          <v-card-text>
            <v-list dense>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-subtitle>Service ID</v-list-item-subtitle>
                  <v-list-item-title>{{ selectedService.id }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-subtitle>Service Type</v-list-item-subtitle>
                  <v-list-item-title>{{ selectedService.serviceName }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-subtitle>Professional</v-list-item-subtitle>
                  <v-list-item-title>{{ selectedService.professionalName }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-subtitle>Contact</v-list-item-subtitle>
                  <v-list-item-title>{{ selectedService.phoneNo }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-subtitle>Booking Date & Time</v-list-item-subtitle>
                  <v-list-item-title>{{ selectedService.bookingDate }} {{ selectedService.bookingTime }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-subtitle>Duration</v-list-item-subtitle>
                  <v-list-item-title>{{ selectedService.duration }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-subtitle>Price</v-list-item-subtitle>
                  <v-list-item-title>₹{{ selectedService.price }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-subtitle>Remarks</v-list-item-subtitle>
                  <v-list-item-title>{{ selectedService.remarks }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" text @click="detailsDialog = false">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </template>
  
  <script>
  export default {
    name: 'CompletedServices',
    data() {
      return {
        search: '',
        completedServices: [],
        detailsDialog: false,
        selectedService: null,
        headers: [
          { text: 'Service ID', value: 'id' },
          { text: 'Service', value: 'serviceName' },
          { text: 'Professional', value: 'professional' },
          { text: 'Date', value: 'bookingDate' },
          { text: 'Time', value: 'bookingTime' },
          { text: 'Duration', value: 'duration' },
          { text: 'Price', value: 'price' },
          { text: 'Actions', value: 'actions', sortable: false }
        ]
      }
    },
    methods: {
      async fetchCompletedServices() {
        try {
          const response = await fetch('http://localhost:5000/api/customer/completed-services', {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`,
              'Content-Type': 'application/json'
            }
          });
          if (!response.ok) throw new Error('Failed to fetch completed services');
          const data = await response.json();
          this.completedServices = data.completed || [];
        } catch (error) {
          console.error('Error:', error);
        }
      },
      showServiceDetails(service) {
        this.selectedService = service;
        this.detailsDialog = true;
      }
    },
    mounted() {
      this.fetchCompletedServices();
    }
  }
  </script>