import { createStore } from 'vuex'
import ws from './ws'
import myself from './myself'
import my from './my'
import anime1 from './anime1'

export default createStore({
  modules: {
    ws,
    myself,
    my,
    anime1
  }
})
