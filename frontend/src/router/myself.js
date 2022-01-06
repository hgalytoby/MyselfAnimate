import Myself from '../views/Myself/Myself'
import Animate from '../views/Myself/Animate'
import Finish from '../views/Myself/Finish'
import Search from '../views/Myself/Search'

export const myselfRoute = [
  {
    path: '/Myself',
    component: Myself,
    children: []
  },
  {
    path: '/Myself/Animate',
    component: Animate,
    name: 'MyselfAnimate',
    props ($route) {
      return { query: $route.query }
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
