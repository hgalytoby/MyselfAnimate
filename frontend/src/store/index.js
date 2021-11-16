import { createStore } from 'vuex'
import ws from './ws'
import myself from './myself'
import my from './my'

export default createStore({
  modules: {
    ws,
    myself,
    my
  }
})
