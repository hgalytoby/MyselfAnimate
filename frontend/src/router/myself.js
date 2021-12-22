import Myself from '../views/Myself'
import Animate from '../views/Myself/Animate'
import Finish from '../views/Myself/Finish'
import Search from '../views/Myself/Search'

export const myselfRoute = [
  {
    path: '/Myself',
    component: Myself
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
  }
]
