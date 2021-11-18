import { createRouter, createWebHistory } from 'vue-router'
import MyHome from '../views/MyHome'
import MyCollect from '../views/MyCollect'
import MyDownload from '../views/MyDownload'
import MyHistory from '../views/MyHistory'
import Myself from '../views/Myself'
import MySettings from '../views/MySettings'
import Week from '../views/Myself/Week'
import Finish from '../views/Myself/Finish'
import Animate from '../views/Myself/Animate'
import Search from '../views/Myself/Search'
import MyLog from '../views/MyLog'

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
    path: '/MyCollect',
    component: MyCollect
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
    path: '/Myself/AnimateSearch',
    component: Search,
    name: 'MyselfAnimateSearch'
  },
  {
    path: '/MyLog',
    component: MyLog
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
