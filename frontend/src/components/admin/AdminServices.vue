<template>
    <v-container>
      <v-card>
        <v-card-title>
          Services Management
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="openAddDialog">
            Add New Service
          </v-btn>
        </v-card-title>
        
        <v-data-table
          :headers="headers"
          :items="services"
          :items-per-page="10"
          class="elevation-1"
        >
          <template v-slot:item.actions="{ item }">
            <v-icon small class="mr-2" @click="editService(item)">
              mdi-pencil
            </v-icon>
            <v-icon small @click="deleteService(item)">
              mdi-delete
            </v-icon>
          </template>
        </v-data-table>
      </v-card>
  
      <!-- Add/Edit Service Dialog -->
      <v-dialog v-model="dialog" max-width="500px">
        <v-card>
          <v-card-title>
            <span>{{ formTitle }}</span>
          </v-card-title>
  
          <v-card-text>
            <v-form ref="form">
              <v-text-field
                v-model="editedItem.name"
                label="Service Name"
                required
              ></v-text-field>
              <v-text-field
                v-model="editedItem.price"
                label="Price"
                type="number"
                required
              ></v-text-field>
              <v-text-field
                v-model="editedItem.time_required"
                label="Time Required (minutes)"
                type="number"
                required
              ></v-text-field>
              <v-textarea
                v-model="editedItem.description"
                label="Description"
              ></v-textarea>
            </v-form>
          </v-card-text>
  
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
            <v-btn color="blue darken-1" text @click="save">Save</v-btn>
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
        { text: 'Service Name', value: 'name' },
        { text: 'Price', value: 'price' },
        { text: 'Time Required', value: 'time_required' },
        { text: 'Rating', value: 'rating' },
        { text: 'Reviews', value: 'rating_count' },
        { text: 'Actions', value: 'actions', sortable: false }
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
            }
          } catch (error) {
            console.error('Error deleting service:', error)
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
          }
        } catch (error) {
          console.error('Error saving service:', error)
        }
      },
  
      close() {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      }
    }
  }
  </script>