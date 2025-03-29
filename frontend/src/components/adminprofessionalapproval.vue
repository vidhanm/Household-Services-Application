<template>
  <v-container>
    <v-card>
      <v-card-title>Pending Professional Approvals</v-card-title>
      <v-card-text>
        <v-data-table
          :headers="headers"
          :items="pendingProfessionals"
          class="elevation-1"
        >
          <template v-slot:item.actions="{ item }">
            <v-dialog v-model="approvalDialogs[item.id]" max-width="500px">
              <template v-slot:activator="{ on, attrs }">
                <v-btn color="primary" v-bind="attrs" v-on="on">Review</v-btn>
              </template>
              <v-card>
                <v-card-title>Approve Professional</v-card-title>
                <v-card-text>
                  <v-form @submit.prevent="approveProfessional(item.id)">
                    <v-text-field
                      v-model="approvalForms[item.id].serviceName"
                      label="Service Name"
                      required
                    ></v-text-field>
                    <v-text-field
                      v-model="approvalForms[item.id].price"
                      label="Service Price"
                      type="number"
                      required
                    ></v-text-field>
                    <v-text-field
                      v-model="approvalForms[item.id].timeRequired"
                      label="Time Required (minutes)"
                      type="number"
                      required
                    ></v-text-field>
                    <v-btn type="submit" color="success">Approve</v-btn>
                    <v-btn color="error" @click="rejectProfessional(item.id)">Reject</v-btn>
                  </v-form>
                </v-card-text>
              </v-card>
            </v-dialog>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </v-container>
</template> 