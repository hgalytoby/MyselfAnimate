import { createStore } from 'vuex'
import ws from './ws'
import api from './apiMyselfi'

export default createStore({
  modules: {
    ws,
    api
  }
})
