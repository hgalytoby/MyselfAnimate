import { createStore } from 'vuex'
import ws from './ws'
import api from './storeMyselfi'

export default createStore({
  modules: {
    ws,
    api
  }
})
