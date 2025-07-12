<template>
  <div class="booking-modal-wrapper">
    <v-dialog
      v-model="localDialog"
      max-width="500"
      persistent
      @update:model-value="handleDialogChange"
    >
      <v-card class="booking-modal">
        <v-card-title class="text-h5 pb-2">
          Book {{ service ? service.name : 'Service' }}
          <v-btn
            icon="mdi-close"
            density="compact"
            variant="text"
            @click="handleClose"
            class="float-right"
          ></v-btn>
        </v-card-title>

        <v-divider></v-divider>

        <v-card-text class="pt-4">
          <v-form ref="bookingForm" v-model="formValid">
            <!-- Date Field -->
            <v-menu
              v-model="dateMenu"
              :close-on-content-click="false"
              transition="scale-transition"
              min-width="auto"
            >
              <template v-slot:activator="{ props }">
                <v-text-field
                  v-model="dateDisplay"
                  label="Select Date"
                  prepend-inner-icon="mdi-calendar"
                  v-bind="props"
                  variant="outlined"
                  density="comfortable"
                  class="mb-3"
                  :rules="[v => !!v || 'Date is required']"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="bookingDate"
                :min="minDate"
                @update:model-value="dateSelected"
              ></v-date-picker>
            </v-menu>

            <!-- Time Field -->
            <v-select
              v-model="bookingTime"
              :items="availableTimes"
              label="Select Time"
              prepend-inner-icon="mdi-clock-outline"
              variant="outlined"
              density="comfortable"
              item-title="text"
              item-value="value"
              class="mb-3"
              :rules="[v => !!v || 'Time is required']"
              return-object
            ></v-select>

            <!-- Duration Field -->
            <v-select
              v-model="bookingDuration"
              :items="durationOptions"
              label="Select Duration"
              prepend-inner-icon="mdi-clock-time-four-outline"
              variant="outlined"
              density="comfortable"
              item-title="text"
              item-value="value"
              class="mb-4"
              :rules="[v => !!v || 'Duration is required']"
              return-object
              @update:model-value="updatePrice"
            ></v-select>

            <!-- Price Information -->
            <v-sheet class="pa-4 bg-grey-lighten-4 rounded-lg mb-3" v-if="service">
              <div class="d-flex align-center mb-2">
                <v-icon icon="mdi-currency-inr" color="primary" class="mr-2"></v-icon>
                <span class="text-subtitle-1 font-weight-bold">Price Details</span>
              </div>
              <div class="d-flex justify-space-between mt-2">
                <span>Base Price:</span>
                <span class="font-weight-medium">₹{{ service.price }}</span>
              </div>
              <div class="d-flex justify-space-between mt-1" v-if="additionalPrice > 0">
                <span>Additional Time:</span>
                <span class="font-weight-medium">₹{{ additionalPrice }}</span>
              </div>
              <v-divider class="my-2"></v-divider>
              <div class="d-flex justify-space-between mt-1">
                <span class="text-subtitle-1 font-weight-bold">Total:</span>
                <span class="text-subtitle-1 font-weight-bold primary--text">₹{{ totalPrice }}</span>
              </div>
            </v-sheet>
          </v-form>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions class="pa-4">
          <v-btn
            color="grey-darken-1"
            variant="text"
            @click="handleClose"
          >
            Close
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            variant="elevated"
            @click="handleAddToCart"
            :disabled="!formValid"
          >
            Add to Cart
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: 'BookingModal',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    service: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      localDialog: this.modelValue,
      formValid: false,
      dateMenu: false,
      bookingDate: new Date().toISOString().slice(0, 10),
      dateDisplay: '',
      bookingTime: null,
      bookingDuration: null,
      availableTimes: [
        { text: '9:00 AM', value: '09:00' },
        { text: '10:00 AM', value: '10:00' },
        { text: '11:00 AM', value: '11:00' },
        { text: '12:00 PM', value: '12:00' },
        { text: '1:00 PM', value: '13:00' },
        { text: '2:00 PM', value: '14:00' },
        { text: '3:00 PM', value: '15:00' },
        { text: '4:00 PM', value: '16:00' },
        { text: '5:00 PM', value: '17:00' },
        { text: '6:00 PM', value: '18:00' }
      ],
      durationOptions: [
        { text: '1 Hour', value: 60 },
        { text: '2 Hours', value: 120 },
        { text: '3 Hours', value: 180 },
        { text: '4 Hours', value: 240 }
      ],
      additionalPrice: 0
    };
  },
  computed: {
    minDate() {
      return new Date().toISOString().slice(0, 10);
    },
    totalPrice() {
      if (!this.service) return 0;
      return this.service.price + this.additionalPrice;
    }
  },
  watch: {
    modelValue: {
      immediate: true,
      handler(newVal) {
        this.localDialog = newVal;
        if (newVal) {
          this.resetForm();
        }
      }
    },
    localDialog(newVal) {
      if (newVal !== this.modelValue) {
        this.$emit('update:modelValue', newVal);
      }
    }
  },
  mounted() {
    this.initializeForm();
  },
  methods: {
    initializeForm() {
      // Set default values
      this.dateDisplay = this.formatDate(new Date());
      this.bookingTime = this.availableTimes[0];
      this.bookingDuration = this.durationOptions[0];
      this.updatePrice();
    },
    resetForm() {
      this.bookingDate = new Date().toISOString().slice(0, 10);
      this.dateDisplay = this.formatDate(new Date());
      this.bookingTime = this.availableTimes[0];
      this.bookingDuration = this.durationOptions[0];
      this.updatePrice();
      
      this.$nextTick(() => {
        if (this.$refs.bookingForm) {
          this.$refs.bookingForm.resetValidation();
        }
      });
    },
    formatDate(date) {
      if (!date) return '';
      
      if (typeof date === 'string') {
        date = new Date(date);
      }
      
      if (isNaN(date.getTime())) {
        return '';
      }
      
      return date.toLocaleDateString('en-US', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },
    dateSelected(date) {
      this.dateMenu = false;
      if (date) {
        this.bookingDate = date;
        this.dateDisplay = this.formatDate(date);
      }
    },
    updatePrice() {
      if (!this.service || !this.bookingDuration) {
        this.additionalPrice = 0;
        return;
      }
      
      const baseHours = 1; // First hour is base price
      const additionalHours = (this.bookingDuration.value / 60) - baseHours;
      
      if (additionalHours > 0) {
        // Additional hours cost 75% of the base price
        this.additionalPrice = Math.round(additionalHours * (this.service.price * 0.75));
      } else {
        this.additionalPrice = 0;
      }
    },
    handleDialogChange(val) {
      if (!val) {
        this.handleClose();
      }
    },
    handleClose() {
      this.localDialog = false;
      this.$emit('update:modelValue', false);
      this.$emit('cancel');
    },
    handleAddToCart() {
      if (!this.$refs.bookingForm) return;
      
      // Create booking details object
      const bookingDetails = {
        ...this.service,
        bookingDate: this.bookingDate,
        bookingTime: this.bookingTime.value,
        bookingTimeDisplay: this.bookingTime.text,
        duration: this.bookingDuration.value,
        durationDisplay: this.bookingDuration.text,
        additionalPrice: this.additionalPrice,
        totalPrice: this.totalPrice
      };
      
      // Emit event with booking details
      this.$emit('confirm-booking', bookingDetails);
      
      // Close dialog
      this.handleClose();
    }
  }
};
</script>

<style scoped>
.booking-modal .v-card-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.booking-modal .float-right {
  position: absolute;
  right: 8px;
  top: 8px;
}

.primary--text {
  color: rgb(var(--v-theme-primary)) !important;
}
</style>