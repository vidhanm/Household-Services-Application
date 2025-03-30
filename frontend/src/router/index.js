import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/login.vue';
import Register from '../components/customerregister.vue';
import CustomerDashboard from '../components/customerdashboard.vue';
import ProfessionalDashboard from '../components/professionaldashboard.vue';
import RegisterProfessional from '../components/registerprofessional.vue';
import RejectedRequests from '../components/ProfRejectedRequests.vue';
import CustomerServiceHistory from '../components/custservicehistory.vue';
import AdminDashboard from '@/components/admindashboard.vue'
import AdminUsers from '@/components/admin/AdminUsers.vue'
import AdminServices from '@/components/admin/AdminServices.vue'
import AdminVerifyProfessionals from '@/components/admin/AdminVerifyProfessionals.vue'
import AdminExportReport from '@/components/admin/AdminExportReport.vue'
import AdminAnalytics from '@/components/adminanalytics.vue'
import ProfessionalHistory from '@/components/ProfessionalHistory'
//import AdminDashboard from '../components/AdminDashboard.vue';

const routes = [
  { 
    path: '/login', 
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    component: Register,
    meta: { requiresAuth: false }
  },
  {
    path: '/register-professional',
    component: () => import('../components/registerprofessional.vue'),
    meta: { requiresAuth: false }
  },
  { 
    path: '/customer-dashboard', 
    component: CustomerDashboard,
    meta: { requiresAuth: true, role: 'customer' }
  },
  { 
    path: '/professional-dashboard', 
    component: ProfessionalDashboard,
    meta: { requiresAuth: true, role: 'professional' }
  },
  { 
    path: '/admin-dashboard', 
    component: () => import('../components/admindashboard.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/analytics',
    component: AdminAnalytics,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/customer/ongoing-services',
    component: () => import('../components/custongoingservice.vue'),
    meta: { requiresAuth: true, role: 'customer' }
  },
  {
    path: '/customer/completed-services',
    component: () => import('../components/custcompletedservice.vue'),
    meta: { requiresAuth: true, role: 'customer' }
  },
  { 
    path: '/checkout', 
    component: () => import('../components/checkout.vue'),
    meta: { requiresAuth: true, role: 'customer' },
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('token');
      if (!token) {
        next('/login');
        return;
      }
      next();
    }
  },
  { 
    path: '/', 
    redirect: '/login' 
  },
  {
    path: '/admin',
    component: AdminDashboard,
    children: [
      {
        path: 'users',
        component: AdminUsers
      },
      {
        path: 'verify-professionals',
        component: AdminVerifyProfessionals
      },
      {
        path: 'export-report',
        component: AdminExportReport
      },
      {
        path: 'services',
        component: AdminServices
      }
    ],
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/professional/history',
    name: 'ProfessionalHistory',
    component: () => import('../components/ProfessionalHistory.vue'),
    meta: { requiresAuth: true, role: 'professional' }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Add navigation guard to check for authentication
router.beforeEach((to, from, next) => {
  const publicPages = ['/login', '/register', '/register-professional'];
  const authRequired = !publicPages.includes(to.path);
  const token = localStorage.getItem('token');

  // For debugging
  console.log('Navigation to:', to.path);
  console.log('Auth required:', authRequired);
  console.log('Token exists:', !!token);

  if (authRequired && !token) {
    console.log('Redirecting to login - no token');
    return next('/login');
  }

  if (token) {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const payload = JSON.parse(window.atob(base64));
      
      // Check token expiration
      if (payload.exp < Date.now() / 1000) {
        console.log('Token expired');
        localStorage.removeItem('token');
        return next('/login');
      }

      // Check role requirements
      if (to.meta.role && to.meta.role !== payload.role) {
        console.log('Role mismatch:', to.meta.role, payload.role);
        return next('/login');
      }

      // Special handling for root path
      if (to.path === '/') {
        switch (payload.role) {
          case 'customer':
            return next('/customer-dashboard');
          case 'professional':
            return next('/professional-dashboard');
          case 'admin':
            return next('/admin-dashboard');
        }
      }
    } catch (error) {
      console.error('Token validation error:', error);
      localStorage.removeItem('token');
      return next('/login');
    }
  }

  next();
});
export default router;
