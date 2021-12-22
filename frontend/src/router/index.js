import { createRouter, createWebHistory } from 'vue-router'
import { myRoute } from './my'
import { myselfRoute } from './myself'
import { anime1Route } from './anime1'

const routes = [
  ...myRoute, ...myselfRoute, ...anime1Route
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
