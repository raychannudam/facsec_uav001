import { createRouter, createWebHistory } from 'vue-router'
import SignInView from '@/views/auth/SignInView.vue'
import LayoutView from '@/LayoutView.vue'
import ControllerIndexView from '@/views/controller/ControllerIndexView.vue'
import DronesIndexView from '@/views/drones/DronesIndexView.vue'
import SettingsIndexView from '@/views/settings/SettingsIndexView.vue'
import AccountIndexView from '@/views/account/AccountIndexView.vue'
import StationIndexView from '@/views/stations/StationIndexView.vue'

const routes = [
  {
    path: "/",
    redirect: "/controller"
  },
  {
    path: "/",
    name: "layout",
    component: LayoutView,
    meta: { requiresAuth: true },
    children: [
      {
        path: "/controller",
        name: "controller",
        component: ControllerIndexView,
        meta: { requiresAuth: true }
      },
      {
        path: "/drones",
        name: "drones",
        component: DronesIndexView,
        meta: { requiresAuth: true }
      },
      {
        path: "/stations",
        name: "stations",
        component: StationIndexView,
        meta: { requiresAuth: true }
      },
      {
        path: "/settings",
        name: "settings",
        component: SettingsIndexView,
        meta: { requiresAuth: true }
      },
      {
        path: "/account",
        name: "account",
        component: AccountIndexView,
        meta: { requiresAuth: true }
      }
    ]
  },
  {
    path: "/sign-in",
    name: "sign-in",
    component: SignInView
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem("access_token"); 

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'sign-in' });
  } else if (to.name === 'sign-in' && isAuthenticated) {
    next({ name: 'controller' }); 
  } else {
    next();
  }
});


export default router
