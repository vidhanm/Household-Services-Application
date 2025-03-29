<template>
  <v-container>
    <v-card>
      <v-card-title>
        Service History
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" md="4">
            <v-text-field
              v-model="searchQuery"
              label="Search services"
              prepend-icon="mdi-magnify"
              @input="filterServices"
            ></v-text-field>
          </v-col>
        </v-row>
        
        <v-data-table
          :headers="headers"
          :items="filteredServices"
          :search="searchQuery"
          class="elevation-1"
        >
          <template v-slot:item.status="{ item }">
            <v-chip
              :color="getStatusColor(item.status)"
              dark
            >
              {{ item.status }}
            </v-chip>
          </template>
          <template v-slot:item.actions="{ item }">
            <v-btn
              v-if="item.status === 'Accepted'"
              color="success"
              small
              @click="markAsCompleted(item.id)"
            >
              Mark Completed
            </v-btn>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'CustomerServiceHistory',
  data() {
    return {
      searchQuery: '',
      services: [],
      headers: [
        { text: 'Service ID', value: 'id' },
        { text: 'Service Name', value: 'serviceName' },
        { text: 'Professional', value: 'professionalName' },
        { text: 'Contact', value: 'phoneNo' },
        { text: 'Date', value: 'bookingDate' },
        { text: 'Time', value: 'bookingTime' },
        { text: 'Status', value: 'status' },
        { text: 'Actions', value: 'actions', sortable: false }
      ]
    }
  },
  computed: {
    filteredServices() {
      return this.services.filter(service => 
        service.serviceName.toLowerCase().includes(this.searchQuery.toLowerCase())
      )
    }
  },
  methods: {
    getStatusColor(status) {
      switch (status) {
        case 'Completed': return 'green';
        case 'Accepted': return 'blue';
        case 'Requested': return 'orange';
        default: return 'grey';
      }
    },
    async fetchServiceHistory() {
      try {
        const response = await fetch('http://localhost:5000/api/customer/service-history', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          }
        });
        if (!response.ok) throw new Error('Failed to fetch service history');
        const data = await response.json();
        this.services = data.history || [];
      } catch (error) {
        console.error('Error:', error);
      }
    },
  },
  mounted() {
    this.fetchServiceHistory();
  }
}
</script>