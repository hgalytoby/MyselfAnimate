import AnimateList from '../views/Anime1/AnimateList'
import Animate from '../views/Anime1/Animate'

export const anime1Route = [
  {
    path: '/AnimateList',
    component: AnimateList,
    name: 'Anime1AnimateList'
  },
  {
    path: '/Animate',
    component: Animate,
    name: 'Anime1Animate',
    props ($route) {
      return { url: $route.query.url, animateData: $route.params.animateData }
    }
  }
]
