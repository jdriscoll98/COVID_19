import Vue from 'vue'
import VueRouter from 'vue-router'

import LandingPage from '@/components/LandingPage.vue'
import InfoPage from '@/components/InfoPage.vue'
import VerifyPage from '@/components/VerifyPage.vue'

const routes = [
  { path: '', component: LandingPage },
  { path: '/info', component: InfoPage },
  { path: '/verify', component: VerifyPage }
]

Vue.use(VueRouter)
const router = new VueRouter({
  scrollBehavior (to, from, savedPosition) { return { x: 0, y: 0 } },
  mode: 'history',
  routes
})

export default router
