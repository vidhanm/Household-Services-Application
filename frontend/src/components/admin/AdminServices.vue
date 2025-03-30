<template>
  <v-container fluid class="admin-services pa-6">
    <!-- Header Section -->
    <v-row class="mb-6">
      <v-col cols="12">
        <h1 class="text-h4 font-weight-bold mb-2">Services Management</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Add, edit, and manage service offerings
        </p>
      </v-col>
    </v-row>

    <v-card class="mb-6 rounded-lg elevation-1">
      <v-card-title class="d-flex align-center py-3 px-6">
        <v-icon icon="mdi-briefcase" color="primary" class="mr-2"></v-icon>
        Services
        <v-spacer></v-spacer>
        <v-btn color="primary" prepend-icon="mdi-plus" @click="openAddDialog">
          Add New Service
        </v-btn>
      </v-card-title>
      
      <v-divider></v-divider>
      
      <v-data-table
        :headers="headers"
        :items="services"
        :items-per-page="10"
        class="elevation-0"
      >
        <template v-slot:item.price="{ item }">
          ₹{{ formatNumber(item.price) }}
        </template>
        
        <template v-slot:item.time_required="{ item }">
          {{ item.time_required }} min
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
          <v-btn icon="mdi-pencil" variant="text" density="comfortable" color="primary" @click="editService(item)"></v-btn>
          <v-btn icon="mdi-delete" variant="text" density="comfortable" color="error" @click="deleteService(item)"></v-btn>
        </template>
      </v-data-table>
    </v-card>

    <!-- Add/Edit Service Dialog -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card class="rounded-lg">
        <v-card-title class="d-flex align-center py-3 px-6">
          <v-icon icon="mdi-briefcase-edit" color="primary" class="mr-2"></v-icon>
          {{ formTitle }}
        </v-card-title>

        <v-divider></v-divider>

        <v-card-text class="pa-4">
          <v-form ref="form">
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.name"
                  label="Service Name"
                  variant="outlined"
                  density="comfortable"
                  required
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="editedItem.price"
                  label="Price (₹)"
                  type="number"
                  variant="outlined"
                  density="comfortable"
                  prefix="₹"
                  required
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="editedItem.time_required"
                  label="Time Required"
                  type="number"
                  variant="outlined"
                  density="comfortable"
                  suffix="minutes"
                  required
                ></v-text-field>
              </v-col>
              
              <v-col cols="12">
                <v-textarea
                  v-model="editedItem.description"
                  label="Description"
                  variant="outlined"
                  density="comfortable"
                  rows="4"
                ></v-textarea>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn variant="text" color="grey-darken-1" @click="close">Cancel</v-btn>
          <v-btn variant="elevated" color="primary" @click="save">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    services: [],
    dialog: false,
    headers: [
      { title: 'Service Name', key: 'name' },
      { title: 'Price', key: 'price' },
      { title: 'Time Required', key: 'time_required' },
      { title: 'Rating', key: 'rating' },
      { title: 'Reviews', key: 'rating_count' },
      { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
    ],
    editedIndex: -1,
    editedItem: {
      name: '',
      price: 0,
      time_required: 60,
      description: ''
    }
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? 'New Service' : 'Edit Service'
    }
  },

  mounted() {
    this.fetchServices()
  },

  methods: {
    formatNumber(value) {
      return new Intl.NumberFormat('en-IN').format(value);
    },
    
    async fetchServices() {
      try {
        const response = await fetch('http://localhost:5000/admin/services', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        const data = await response.json()
        this.services = data.services
      } catch (error) {
        console.error('Error fetching services:', error)
        this.showSnackbar('Failed to load services', 'error')
      }
    },

    openAddDialog() {
      this.editedIndex = -1
      this.editedItem = {
        name: '',
        price: 0,
        time_required: 60,
        description: ''
      }
      this.dialog = true
    },

    editService(item) {
      this.editedIndex = this.services.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },

    async deleteService(item) {
      if (confirm('Are you sure you want to delete this service?')) {
        try {
          const response = await fetch(`http://localhost:5000/admin/services/${item.id}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          })
          if (response.ok) {
            this.services = this.services.filter(s => s.id !== item.id)
            this.showSnackbar('Service deleted successfully', 'success')
          }
        } catch (error) {
          console.error('Error deleting service:', error)
          this.showSnackbar('Error deleting service', 'error')
        }
      }
    },

    async save() {
      try {
        const method = this.editedIndex === -1 ? 'POST' : 'PUT'
        const url = this.editedIndex === -1 
          ? 'http://localhost:5000/admin/services'
          : `http://localhost:5000/admin/services/${this.editedItem.id}`

        const response = await fetch(url, {
          method,
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(this.editedItem)
        })

        if (response.ok) {
          await this.fetchServices()
          this.close()
          this.showSnackbar(`Service ${this.editedIndex === -1 ? 'added' : 'updated'} successfully`, 'success')
        }
      } catch (error) {
        console.error('Error saving service:', error)
        this.showSnackbar('Error saving service', 'error')
      }
    },

    close() {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, {
          name: '',
          price: 0,
          time_required: 60,
          description: ''
        })
        this.editedIndex = -1
      })
    },
    
    showSnackbar(text, color = 'success') {
      this.$emit('show-snackbar', { text, color });
    }
  }
}
</script>

<style scoped>
.admin-services {
  background-color: var(--bg-secondary);
  min-height: 100vh;
}

.v-card {
  border-radius: 12px;
  overflow: hidden;
  background-color: var(--card-bg);
  border: 1px solid var(--border-color);
}

.v-card-title {
  font-size: 1.1rem;
  font-weight: 600;
}
</style>