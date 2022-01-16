import AnimateList from '../views/Anime1/AnimateList'
import Animate from '../views/Anime1/Animate'
import Season from '../views/Anime1/Season'

export const anime1Route = [
  {
    path: '/Anime1/AnimateList',
    component: AnimateList,
    name: 'Anime1AnimateList'
  },
  {
    path: '/Anime1/Animate',
    component: Animate,
    name: 'Anime1Animate',
    props ($route) {
      return { url: $route.query.url }
    }
  },
  {
    path: '/Anime1/Season/:season',
    component: Season,
    name: 'Anime1Season'
  }
]
