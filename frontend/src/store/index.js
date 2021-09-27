import { createStore } from 'vuex'
import ws from './ws'
import myself from './storeMyself'

export default createStore({
  modules: {
    ws,
    myself
  }
})
