import MyHome from '../views/MyHome'
import MyHistory from '../views/MyHistory'
import MyDownload from '../views/MyDownload'
import MyCollect from '../views/MyCollect'
import MyLog from '../views/MyLog'
import MySettings from '../views/MySettings'

export const myRoute = [
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
    path: '/MyLog',
    component: MyLog
  },
  {
    path: '/MySettings',
    component: MySettings
  }
]
