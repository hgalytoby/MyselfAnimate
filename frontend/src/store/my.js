import {
  myLogAction, myLogMutation,
  myLogState
} from '../variables/my'
import axios from 'axios'
import { myApi } from '../api'

export const state = {
  [myLogState]: []
}

export const actions = {
  [myLogAction] (context, value) {
    console.log('value', value)
    axios.get(myApi.myLog(value.page, value.size)).then(
      response => {
        context.commit(myLogMutation, response.data)
      },
      error => {
        alert(error.msg)
      }
    )
  }
}
export const mutations = {
  [myLogMutation] (state, value) {
    state[myLogState] = value
  }
}
export const getters = {
}
export default {
  state,
  actions,
  mutations,
  getters,
  namespaced: true
}
