import {
  historyAction, historyMutation,
  historyState,
  logAction, logMutation,
  logState, systemAction, systemMutation, systemState
} from '../variables/my'
import { myApi } from '../api'
import { axiosGet } from '../tools'

export const state = {
  [logState]: [],
  [historyState]: [],
  [systemState]: []
}

export const actions = {
  [logAction] (context, value) {
    axiosGet(myApi.log, context, logMutation)
  },
  [historyAction] (context, value) {
    axiosGet(myApi.history(value.page, value.size), context, historyMutation)
  },
  [systemAction] (context, value) {
    axiosGet(myApi.system(value.page, value.size), context, systemMutation)
  }
}
export const mutations = {
  [logMutation] (state, value) {
    state[systemState] = value.system
    state[historyState] = value.history
  },
  [historyMutation] (state, value) {
    state[historyState] = value
  },
  [systemMutation] (state, value) {
    state[systemState] = value
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
