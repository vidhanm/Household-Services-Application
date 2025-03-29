<template>
  <v-container>
    <v-card>
      <v-card-title>
        Service Summary
      </v-card-title>
      <v-card-text>
        <v-data-table
          :headers="headers"
          :items="summaryItems"
          :items-per-page="5"
          class="elevation-1"
        >
        </v-data-table>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'CustomerSummary',
  data() {
    return {
      headers: [
        { text: 'Service', value: 'service' },
        { text: 'Date', value: 'date' },
        { text: 'Status', value: 'status' },
        { text: 'Amount', value: 'amount' }
      ],
      summaryItems: []
    }
  }
}
</script> 