import {
  myHistoryAction, myHistoryMutation,
  myHistoryState,
  myLogAction, myLogMutation,
  myLogState
} from '../variables/my'
import { myApi } from '../api'
import { axiosGet } from '../tools'

export const state = {
  [myLogState]: [],
  [myHistoryState]: []
}

export const actions = {
  [myLogAction] (context, value) {
    console.log(value)
    axiosGet(myApi.myLog(value.page, value.size), context, myLogMutation)
  },
  [myHistoryAction] (context, value) {
    axiosGet(myApi.myHistory(value.page, value.size), context, myHistoryMutation)
  }
}
export const mutations = {
  [myLogMutation] (state, value) {
    state[myLogState] = value
  },
  [myHistoryMutation] (state, value) {
    state[myHistoryState] = value
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
