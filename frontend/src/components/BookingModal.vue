<template>
  <v-dialog
    v-model="dialog"
    max-width="500"
    persistent
  >
    <v-card>
      <v-card-title class="text-h5">
        Book {{ service.name }}
      </v-card-title>

      <v-card-text>
        <v-form ref="form" v-model="valid">
          <v-menu
            ref="dateMenu"
            v-model="dateMenu"
            :close-on-content-click="false"
            transition="scale-transition"
            offset-y
            min-width="auto"
          >
            <template #activator="{ props }">
              <v-text-field
                v-model="formattedDate"
                label="Booking Date"
                prepend-icon="mdi-calendar"
                readonly
                v-bind="props"
                :rules="dateRules"
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="bookingDate"
              :min="minDate"
              @update:model-value="handleDateSelect"
            ></v-date-picker>
          </v-menu>

          <v-select
            v-model="bookingTime"
            :items="timeSlots"
            label="Service Start Time"
            prepend-icon="mdi-clock-outline"
            :rules="timeRules"
          ></v-select>

          <v-select
            v-model="duration"
            :items="durationOptions"
            label="Duration"
            prepend-icon="mdi-clock-time-four-outline"
            :rules="durationRules"
          ></v-select>

          <v-divider class="my-4"></v-divider>

          <v-list-item>
            <template v-slot:prepend>
              <v-icon color="primary">mdi-currency-inr</v-icon>
            </template>
            <v-list-item-title>Price Breakdown</v-list-item-title>
            <template v-slot:append>
              <div class="text-right">
                <div>Base Price: ₹{{ service.price }}</div>
                <div v-if="additionalPrice > 0">Additional: ₹{{ additionalPrice }}</div>
                <div class="text-h6 primary--text">Total: ₹{{ totalPrice }}</div>
              </div>
            </template>
          </v-list-item>
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="grey-darken-1"
          variant="text"
          @click="closeDialog"
        >
          Cancel
        </v-btn>
        <v-btn
          color="primary"
          :disabled="!valid"
          @click="confirmBooking"
        >
          Book Now
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'BookingModal',
  props: {
    modelValue: Boolean,
    service: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      dialog: this.modelValue,
      valid: true,
      dateMenu: false,
      bookingDate: new Date().toISOString().substr(0, 10),
      bookingTime: '9:00',
      duration: '60',
      timeSlots: [
        '9:00', '10:00', '11:00', '12:00', '13:00',
        '14:00', '15:00', '16:00', '17:00', '18:00', '19:00'
      ],
      durationOptions: [
        { text: '1 hour', value: '60' },
        { text: '2 hours', value: '120' },
        { text: '3 hours', value: '180' },
        { text: '4 hours', value: '240' }
      ],
      dateRules: [
        v => !!v || 'Date is required',
        v => {
          const selectedDate = new Date(v);
          const today = new Date();
          today.setHours(0, 0, 0, 0);
          return selectedDate >= today || 'Cannot select past dates';
        }
      ],
      timeRules: [v => !!v || 'Time is required'],
      durationRules: [v => !!v || 'Duration is required'],
      formattedDate: ''
    }
  },
  computed: {
    minDate() {
      return new Date().toISOString().substr(0, 10)
    },
    additionalPrice() {
      const additionalHours = (parseInt(this.duration) - 60) / 60
      return additionalHours > 0 ? Math.round(additionalHours * (this.service.price * 0.75)) : 0
    },
    totalPrice() {
      return this.service.price + this.additionalPrice
    }
  },
  watch: {
    modelValue(val) {
      this.dialog = val
    },
    dialog(val) {
      this.$emit('update:modelValue', val)
    }
  },
  methods: {
    closeDialog() {
      this.dialog = false
      this.$refs.form?.reset()
    },
    confirmBooking() {
      if (!this.$refs.form?.validate()) return

      const bookingDetails = {
        ...this.service,
        bookingDate: this.bookingDate,
        bookingTime: this.bookingTime,
        duration: parseInt(this.duration),
        totalPrice: this.totalPrice
      }

      this.$emit('confirm-booking', bookingDetails)
      this.closeDialog()
    },
    handleDateSelect(date) {
      this.dateMenu = false;
      this.bookingDate = date;
      this.formattedDate = this.formatDate(date);
    },
    formatDate(dateStr) {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      return date.toLocaleDateString('en-US', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    }
  },
  created() {
    this.formattedDate = this.formatDate(this.bookingDate);
  },
  mounted() {
    this.$nextTick(() => {
      this.$refs.form?.validate();
    });
  },
}
</script>