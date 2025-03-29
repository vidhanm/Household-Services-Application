<template>
  <v-card>
    <v-card-title>
      Pending Professional Approvals
      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>

    <v-data-table
      :headers="headers"
      :items="pendingProfessionals"
      :search="search"
      :loading="loading"
    >
      <template v-slot:item.document="{ item }">
        <v-btn small text color="primary" @click="viewDocument(item.id)">
          View Document
        </v-btn>
      </template>

      <template v-slot:item.actions="{ item }">
        <v-btn small color="success" @click="showApprovalDialog(item)">
          Approve
        </v-btn>
        <v-btn small color="error" class="ml-2" @click="rejectProfessional(item.id)">
          Reject
        </v-btn>
      </template>
    </v-data-table>

    <!-- Approval Dialog -->
    <v-dialog v-model="approvalDialog" max-width="500px">
      <v-card>
        <v-card-title>Approve Professional</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="approveProfessional">
            <v-text-field
              v-model="approvalForm.serviceName"
              label="Service Name"
              required
            ></v-text-field>
            <v-text-field
              v-model="approvalForm.price"
              label="Base Price"
              type="number"
              required
            ></v-text-field>
            <v-text-field
              v-model="approvalForm.timeRequired"
              label="Time Required (minutes)"
              type="number"
              required
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="approveProfessional">Approve</v-btn>
          <v-btn color="error" text @click="approvalDialog = false">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
export default {
  name: 'AdminVerifyProfessionals',
  data() {
    return {
      search: '',
      loading: false,
      pendingProfessionals: [],
      approvalDialog: false,
      selectedProfessional: null,
      approvalForm: {
        serviceName: '',
        price: '',
        timeRequired: ''
      },
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Name', value: 'name' },
        { text: 'Proposed Service', value: 'service' },
        { text: 'Experience', value: 'experience' },
        { text: 'Documents', value: 'document' },
        { text: 'Actions', value: 'actions', sortable: false }
      ]
    }
  },
  methods: {
    async fetchPendingProfessionals() {
      try {
        this.loading = true;
        const response = await fetch('http://localhost:5000/admin/professionals/pending', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        const data = await response.json();
        this.pendingProfessionals = data.pending_professionals;
      } catch (error) {
        console.error('Error fetching pending professionals:', error);
      } finally {
        this.loading = false;
      }
    },

    showApprovalDialog(professional) {
      this.selectedProfessional = professional;
      this.approvalForm.serviceName = professional.service;
      this.approvalDialog = true;
    },

    async approveProfessional() {
      try {
        const response = await fetch(`http://localhost:5000/admin/professionals/approve/${this.selectedProfessional.id}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({
            approved: true,
            service_name: this.approvalForm.serviceName,
            price: parseFloat(this.approvalForm.price),
            time_required: parseInt(this.approvalForm.timeRequired)
          })
        });

        if (!response.ok) throw new Error('Failed to approve professional');
        
        await this.fetchPendingProfessionals();
        this.approvalDialog = false;
      } catch (error) {
        console.error('Error approving professional:', error);
      }
    },

    async rejectProfessional(id) {
      if (!confirm('Are you sure you want to reject this professional?')) return;
      
      try {
        const response = await fetch(`http://localhost:5000/admin/professionals/approve/${id}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({
            approved: false
          })
        });

        if (!response.ok) throw new Error('Failed to reject professional');
        
        await this.fetchPendingProfessionals();
      } catch (error) {
        console.error('Error rejecting professional:', error);
      }
    },

    viewDocument(id) {
      window.open(`http://localhost:5000/api/admin/certificate/${id}`, '_blank');
    }
  },
  mounted() {
    this.fetchPendingProfessionals();
  }
}
</script> 