<template>
  <v-container>
    <v-card>
      <v-card-title>
        Ongoing Services
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" md="4">
            <v-text-field
              v-model="searchQuery"
              label="Search ongoing services"
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

    <!-- Add Rating Modal -->
    <v-dialog v-model="showRatingModal" max-width="500px">
      <v-card>
        <v-card-title>Rate Service</v-card-title>
        <v-card-text>
          <v-row class="mt-3">
            <v-col cols="12" class="text-center">
              <v-rating
                v-model="rating"
                color="warning"
                half-increments
                hover
                size="large"
              ></v-rating>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12">
              <v-textarea
                v-model="feedback"
                label="Your Feedback"
                outlined
                rows="3"
                placeholder="Please share your experience..."
              ></v-textarea>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey darken-1" text @click="closeRatingModal">Cancel</v-btn>
          <v-btn color="success" @click="submitRatingAndComplete">Submit & Complete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
export default {
  name: 'OngoingServices',
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
      ],
      showRatingModal: false,
      rating: 0,
      feedback: '',
      selectedServiceId: null
    }
  },
  computed: {
    filteredServices() {
      return this.services.filter(service => 
        service.status === 'Accepted' &&
        service.serviceName.toLowerCase().includes(this.searchQuery.toLowerCase())
      )
    }
  },
  methods: {
    getStatusColor(status) {
      return status === 'Accepted' ? 'blue' : 'grey'
    },
    async fetchOngoingServices() {
      try {
        const response = await fetch('http://localhost:5000/api/customer/ongoing-services', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          }
        });
        if (!response.ok) throw new Error('Failed to fetch ongoing services');
        const data = await response.json();
        this.services = data.services || [];
      } catch (error) {
        console.error('Error:', error);
      }
    },
    markAsCompleted(requestId) {
      this.selectedServiceId = requestId;
      this.showRatingModal = true;
    },
    closeRatingModal() {
      this.showRatingModal = false;
      this.rating = 0;
      this.feedback = '';
      this.selectedServiceId = null;
    },
    async submitRatingAndComplete() {
      try {
        const response = await fetch(`http://localhost:5000/api/customer-feedback/${this.selectedServiceId}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({
            rating: this.rating,
            feedback: this.feedback
          })
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || 'Failed to submit rating');
        }
        
        const data = await response.json();
        console.log('Success:', data);
        await this.fetchOngoingServices();
        this.closeRatingModal();
      } catch (error) {
        console.error('Error:', error);
        alert(error.message || 'Failed to submit rating and complete service');
      }
    }
  },
  mounted() {
    this.fetchOngoingServices();
  }
}
</script>