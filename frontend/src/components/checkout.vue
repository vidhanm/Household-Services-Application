<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card class="elevation-3">
            <v-toolbar color="primary" dark>
              <v-toolbar-title>Your Cart</v-toolbar-title>
              <v-spacer></v-spacer>
              <v-btn icon @click="clearCartItems" v-if="cartItems.length > 0">
                <v-icon>mdi-delete-sweep</v-icon>
              </v-btn>
            </v-toolbar>
            
            <v-card-text v-if="cartItems.length === 0" class="text-center pa-8">
              <v-icon size="64" color="grey lighten-1">mdi-cart-off</v-icon>
              <h3 class="mt-4 grey--text text--darken-1">Your cart is empty</h3>
              <v-btn color="primary" to="/customer-dashboard" class="mt-4">
                Browse Services
              </v-btn>
            </v-card-text>
  
            <template v-else>
              <v-list two-line>
                <v-list-item v-for="(item, index) in cartItems" :key="index">
                  <v-list-item-avatar>
                    <v-icon size="40" color="primary">{{ getServiceIcon(item.name) }}</v-icon>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title class="text-h6">{{ item.name }}</v-list-item-title>
                    <v-list-item-subtitle>Base Price</v-list-item-subtitle>
                  </v-list-item-content>
                  <v-list-item-action class="d-flex flex-column align-end">
                    <div class="text-h6 primary--text">₹{{ item.price }}</div>
                    <v-btn icon small class="mt-1" @click="removeItem(index)" color="red lighten-3">
                      <v-icon small>mdi-delete</v-icon>
                    </v-btn>
                  </v-list-item-action>
                </v-list-item>
              </v-list>
  
              <v-divider></v-divider>
  
              <v-card-text class="pa-4">
                <div class="d-flex justify-space-between align-center">
                  <div>
                    <div class="text-h6">Total Amount</div>
                    <div class="text-subtitle-2 grey--text">Including all taxes</div>
                  </div>
                  <div class="text-h4 primary--text">₹{{ totalAmount }}</div>
                </div>
              </v-card-text>
  
              <v-card-actions class="pa-4">
                <v-btn text to="/customer-dashboard">
                  <v-icon left>mdi-arrow-left</v-icon>
                  Continue Shopping
                </v-btn>
                <v-spacer></v-spacer>
                <v-btn 
                  color="primary" 
                  large 
                  @click="proceedToCheckout"
                  :loading="isProcessing"
                >
                  <v-icon left>mdi-check-circle</v-icon>
                  Proceed to Checkout
                </v-btn>
              </v-card-actions>
            </template>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  export default {
    name: 'Checkout',
    inject: ['updateCart', 'getCartItems', 'clearCart', 'removeFromCart'],
    data() {
      return {
        isProcessing: false
      }
    },
    computed: {
      cartItems() {
        return this.getCartItems();
      },
      totalAmount() {
        return this.cartItems.reduce((total, item) => total + item.price, 0);
      }
    },
    methods: {
      getServiceIcon(serviceName) {
        const icons = {
          'Plumber': 'mdi-water-pump',
          'Electrical Work': 'mdi-lightning-bolt',
          'Carpenter': 'mdi-hammer',
          'Home Cleaning': 'mdi-broom',
          'Painter': 'mdi-paint',
          'Beauty and Spa': 'mdi-spa',
          'Fitness and Yoga': 'mdi-yoga',
          'Pest Control': 'mdi-bug',
          'Interior Design': 'mdi-floor-plan',
          'AC Repair': 'mdi-air-conditioner',
          'Saloon': 'mdi-content-cut',
          'Massage': 'mdi-hand-heart'
        }
        return icons[serviceName] || 'mdi-briefcase'
      },
      removeItem(index) {
        this.removeFromCart(index);
      },
      clearCartItems() {
        this.clearCart();
      },
      async proceedToCheckout() {
        try {
          this.isProcessing = true;
          const serviceRequests = this.cartItems.map(item => ({
            service_id: item.id,
            service_type: item.name,
            price: item.totalPrice || item.price,
            booking_date: item.bookingDate,
            booking_time: item.bookingTime,
            duration: parseInt(item.duration),
            remarks: item.remarks
          }));
          
          const payload = {
            requests: serviceRequests
          };
          
          console.log("Cart Items:", this.cartItems);
          console.log("Payload being sent:", payload);

          const response = await fetch('http://localhost:5000/api/customer/service-requests', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify(payload)
          });

          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Failed to create service requests');
          }

          const data = await response.json();
          this.clearCartItems();
          alert('Service requests have been sent to professionals!');
          this.$router.push('/customer-dashboard');
        } catch (error) {
          console.error('Checkout failed:', error);
          alert(error.message || 'Failed to create service requests. Please try again.');
        } finally {
          this.isProcessing = false;
        }
      }
    }
  }
</script>
