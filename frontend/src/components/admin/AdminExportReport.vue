<template>
    <v-container>
      <v-card>
        <v-card-title>
          Export Service Reports
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
            :loading="loading"
          >
            <template v-slot:top>
              <v-toolbar flat>
                <v-toolbar-title>Completed Services</v-toolbar-title>
                <v-divider class="mx-4" inset vertical></v-divider>
                <v-spacer></v-spacer>
                <v-btn
                  color="primary"
                  dark
                  @click="exportToCSV"
                  :loading="exporting"
                >
                  Export to CSV
                  <v-icon right>mdi-download</v-icon>
                </v-btn>
              </v-toolbar>
            </template>
          </v-data-table>
        </v-card-text>
  
        <!-- Success Snackbar -->
        <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000">
          {{ snackbarText }}
          <template v-slot:action="{ attrs }">
            <v-btn text v-bind="attrs" @click="snackbar = false">Close</v-btn>
          </template>
        </v-snackbar>
      </v-card>
    </v-container>
  </template>
  
  <script>
  export default {
    name: 'AdminExportReport',
    data() {
      return {
        search: '',
        loading: false,
        exporting: false,
        completedServices: [],
        snackbar: false,
        snackbarText: '',
        snackbarColor: 'success',
        headers: [
          { text: 'Service ID', value: 'service_id' },
          { text: 'Customer ID', value: 'customer_id' },
          { text: 'Professional ID', value: 'professional_id' },
          { text: 'Date of Request', value: 'date_of_request' },
          { text: 'Date of Completion', value: 'date_of_completion' },
          { text: 'Service Type', value: 'service_type' },
          { text: 'Rating', value: 'rating' },
          { text: 'Remarks', value: 'remarks' }
        ]
      }
    },
    methods: {
      async fetchCompletedServices() {
        try {
          this.loading = true;
          const response = await fetch('http://localhost:5000/admin/completed-services', {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          });
          
          if (!response.ok) throw new Error('Failed to fetch completed services');
          
          const data = await response.json();
          this.completedServices = data.completed_services;
        } catch (error) {
          console.error('Error fetching completed services:', error);
          this.showSnackbar('Error fetching services', 'error');
        } finally {
          this.loading = false;
        }
      },
  
      async exportToCSV() {
        try {
          this.exporting = true;
          const response = await fetch('http://localhost:5000/admin/export-services', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          });
  
          if (!response.ok) throw new Error('Failed to initiate export');
  
          const data = await response.json();
          this.showSnackbar('Export job started. You will be notified when complete.', 'info');
        } catch (error) {
          console.error('Error starting export:', error);
          this.showSnackbar('Error starting export', 'error');
        } finally {
          this.exporting = false;
        }
      },
  
      showSnackbar(text, color = 'success') {
        this.snackbarText = text;
        this.snackbarColor = color;
        this.snackbar = true;
      }
    },
    mounted() {
      this.fetchCompletedServices();
    }
  }
  </script>