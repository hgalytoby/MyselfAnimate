import { createRouter, createWebHistory } from 'vue-router'
import MyHome from '../views/MyHome'
import MyLove from '../views/MyLove'
import MyDownload from '../views/MyDownload'
import MyHistory from '../views/MyHistory'
import Myself from '../views/Myself'
import MySettings from '../views/MySettings'
import Search from '../components/Search'
import Week from '../views/Myself/Week'
import Finish from '../views/Myself/Finish'

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
      },
      {
        path: 'Search',
        component: Search
      },
      {
        path: 'Finish',
        component: Finish
      }
    ]
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
