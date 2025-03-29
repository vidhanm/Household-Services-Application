<template>
  <div>
    <v-card class="elevation-2 rounded-lg">
      <v-card-title class="d-flex align-center py-3">
        <v-icon color="primary" class="mr-2">mdi-account-group</v-icon>
        <span class="text-h6">Users Management</span>
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search users..."
          hide-details
          outlined
          dense
          class="mx-2"
          style="max-width: 300px"
        ></v-text-field>
      </v-card-title>
      <v-divider></v-divider>
      <v-data-table
        :headers="headers"
        :items="users"
        :search="search"
        :loading="loading"
        :items-per-page="10"
        class="elevation-0"
      >
        <template v-slot:item.is_active="{ item }">
          <v-chip
            small
            :color="item.is_active ? 'success' : 'error'"
            text-color="white"
          >
            {{ item.is_active ? 'Active' : 'Inactive' }}
          </v-chip>
        </template>
        <template v-slot:item.actions="{ item }">
          <div class="d-flex align-center justify-space-around">
            <v-btn
              small
              :color="item.is_active ? 'error' : 'success'"
              @click="blockUser(item)"
              :disabled="item.role === 'admin'"
              class="mr-2"
              :class="{'opacity-5': item.role === 'admin'}"
              elevation="1"
              :outlined="item.role === 'admin'"
            >
              {{ item.is_active ? 'Block' : 'Unblock' }}
            </v-btn>
            <v-btn
              small
              color="primary"
              fab
              elevation="1"
              @click="editUser(item)"
              class="ml-1"
              :disabled="item.role === 'admin' && item.id !== currentUserId"
            >
              <v-icon small>mdi-pencil</v-icon>
            </v-btn>
          </div>
        </template>
        <template v-slot:no-data>
          <v-alert type="info" class="ma-4">No users found</v-alert>
        </template>
      </v-data-table>
    </v-card>

    <!-- Edit User Dialog -->
    <v-dialog v-model="editDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h6">Edit User</v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="editedUser.username"
                  label="Username"
                  outlined
                  dense
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedUser.email"
                  label="Email"
                  outlined
                  dense
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-select
                  v-model="editedUser.role"
                  :items="['admin', 'customer', 'professional']"
                  label="Role"
                  outlined
                  dense
                ></v-select>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="editDialog = false">Cancel</v-btn>
          <v-btn color="blue darken-1" text @click="saveUser">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: 'AdminUsers',
  data() {
    return {
      search: '',
      loading: false,
      users: [],
      headers: [
        { text: 'ID', value: 'id', width: '80px' },
        { text: 'Username', value: 'username' },
        { text: 'Email', value: 'email' },
        { text: 'Role', value: 'roleDisplay' },
        { text: 'Date Created', value: 'date_created' },
        { text: 'Status', value: 'is_active', width: '120px' },
        { text: 'Actions', value: 'actions', sortable: false, width: '120px' }
      ],
      currentUserId: null,
      editDialog: false,
      editedUser: {
        id: null,
        username: '',
        email: '',
        role: '',
      }
    }
  },
  methods: {
    async fetchUsers() {
      this.loading = true;
      try {
        const response = await fetch('http://localhost:5000/admin/users', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (response.ok) {
          const data = await response.json();
          this.users = data.users;
          
          // Add formatted role display
          this.users.forEach(user => {
            user.roleDisplay = this.capitalizeFirstLetter(user.role);
            
            // Format date
            if (user.date_created) {
              const date = new Date(user.date_created);
              user.date_created = new Intl.DateTimeFormat('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
              }).format(date);
            }
          });
        } else {
          console.error('Failed to fetch users:', response.statusText);
        }
      } catch (error) {
        console.error('Error fetching users:', error);
      } finally {
        this.loading = false;
      }
    },
    
    capitalizeFirstLetter(string) {
      return string.charAt(0).toUpperCase() + string.slice(1);
    },
    
    async blockUser(user) {
      try {
        const response = await fetch(`http://localhost:5000/admin/users/${user.id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            is_active: !user.is_active // Toggle active status
          })
        });
        
        if (response.ok) {
          // Update the user status locally for immediate feedback
          user.is_active = !user.is_active;
          
          // Show a success message
          this.$emit('show-snackbar', {
            text: `User ${user.username} ${user.is_active ? 'activated' : 'blocked'} successfully`,
            color: user.is_active ? 'success' : 'error'
          });
        } else {
          const errorData = await response.json();
          this.$emit('show-snackbar', {
            text: errorData.message || 'Failed to update user status',
            color: 'error'
          });
        }
      } catch (error) {
        console.error('Error updating user:', error);
        this.$emit('show-snackbar', {
          text: 'An error occurred while updating user status',
          color: 'error'
        });
      }
    },
    editUser(user) {
      // Implementation for editing user
      this.editedUser = {
        id: user.id,
        username: user.username,
        email: user.email,
        role: user.role,
      };
      this.editDialog = true;
    },
    async getCurrentUser() {
      try {
        // Parse the JWT token to get the current user ID
        const token = localStorage.getItem('token');
        if (token) {
          const base64Url = token.split('.')[1];
          const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
          const jsonPayload = decodeURIComponent(atob(base64).split('').map((c) => {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
          }).join(''));
          
          const payload = JSON.parse(jsonPayload);
          this.currentUserId = payload.sub || payload.user_id;
        }
      } catch (error) {
        console.error('Error getting current user ID:', error);
      }
    },
    async saveUser() {
      try {
        this.loading = true;
        const response = await fetch(`http://localhost:5000/admin/users/${this.editedUser.id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.editedUser.username,
            email: this.editedUser.email,
            role: this.editedUser.role
          })
        });
        
        if (response.ok) {
          // Close the dialog
          this.editDialog = false;
          
          // Refresh the users list
          await this.fetchUsers();
          
          // Show success message
          this.$emit('show-snackbar', {
            text: 'User updated successfully',
            color: 'success'
          });
        } else {
          const errorData = await response.json();
          this.$emit('show-snackbar', {
            text: errorData.message || 'Failed to update user',
            color: 'error'
          });
        }
      } catch (error) {
        console.error('Error updating user:', error);
        this.$emit('show-snackbar', {
          text: 'An error occurred while updating the user',
          color: 'error'
        });
      } finally {
        this.loading = false;
      }
    }
  },
  async mounted() {
    await this.getCurrentUser();
    this.fetchUsers();
  }
}
</script>

<style scoped>
.opacity-5 {
  opacity: 0.5;
}

.v-data-table ::v-deep .v-data-table__wrapper {
  min-height: 400px;
}

.v-data-table ::v-deep tbody tr:hover {
  background-color: rgba(0, 0, 0, 0.03);
}

.v-data-table ::v-deep tbody tr td {
  border-bottom: thin solid rgba(0, 0, 0, 0.12);
}
</style> 