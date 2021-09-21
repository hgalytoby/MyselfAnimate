import { createRouter, createWebHistory } from 'vue-router'
import MyHome from '../views/MyHome'
import MyLove from '../views/MyLove'
import MyDownload from '../views/MyDownload'
import MyHistory from '../views/MyHistory'
import Myself from '../views/Myself'
import MySettings from '../views/MySettings'
import Week from '../views/Myself/Week'
import Finish from '../views/Myself/Finish'
import Animate from '../components/Animate'

const routes = [
  {
    path: '/',
    component: MyHome
  },
  {
    path: '/MyHistory',
    component: MyHistory
  },
  {
    path: '/MyDownload',
    component: MyDownload
  },
  {
    path: '/MyLove',
    component: MyLove
  },
  {
    path: '/Myself',
    component: Myself,
    children: [
      {
        path: 'Week',
        component: Week
      }
    ]
  },
  {
    path: '/Myself/Animate',
    component: Animate,
    name: 'MyselfAnimate',
    props ($route) {
      return { url: $route.query.url }
    }
  },
  {
    path: '/Myself/AnimateFinish',
    component: Finish,
    name: 'MyselfAnimateFinish'
  },
  {
    path: '/MySettings',
    component: MySettings
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
