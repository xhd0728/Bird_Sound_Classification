import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from '../views/main.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/main',
    name: 'Main',
    component: Main,
  },
  {
    path: '/login',
    name: 'Login',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/login.vue')
  },
  {
    path:'/',
    redirect:'/login'
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
