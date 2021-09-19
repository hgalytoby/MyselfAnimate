import { createStore } from 'vuex'
import ws from './ws'
import api from './api'

export default createStore({
  modules: {
    ws,
    api
  }
})
