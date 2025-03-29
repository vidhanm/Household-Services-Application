<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" sm="8" md="6">
          <v-card class="elevation-12">
            <v-toolbar color="primary" dark flat>
              <v-toolbar-title>Create Service Request</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form @submit.prevent="createServiceRequest">
                <v-select
                  v-model="serviceId"
                  :items="services"
                  item-title="name"
                  item-value="id"
                  label="Select Service"
                  required
                ></v-select>
                <v-textarea
                  v-model="remarks"
                  label="Remarks"
                  name="remarks"
                ></v-textarea>
                <v-btn type="submit" color="primary" block class="mt-4">Submit Request</v-btn>
              </v-form>
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
        serviceId: null,
        remarks: '',
        services: [], // This will be populated with available services
      };
    },
    methods: {
      async createServiceRequest() {
        try {
          const response = await fetch('http://localhost:5000/customer/service-request', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
            body: JSON.stringify({
              service_id: this.serviceId,
              remarks: this.remarks,
            }),
          });
  
          if (!response.ok) {
            throw new Error('Failed to create service request');
          }
  
          const data = await response.json();
          console.log('Service request created:', data);
          // Handle successful creation (e.g., show success message, redirect)
        } catch (error) {
          console.error('Error creating service request:', error);
          // Handle error (e.g., show error message)
        }
      },
      async fetchServices() {
        try {
          const response = await fetch('http://localhost:5000/services/search', {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
          });
  
          if (!response.ok) {
            throw new Error('Failed to fetch services');
          }
  
          this.services = await response.json();
        } catch (error) {
          console.error('Error fetching services:', error);
        }
      },
    },
    mounted() {
      this.fetchServices();
    },
  };
  </script>