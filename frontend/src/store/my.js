import {
  historyAction,
  historyMutation,
  historyState,
  logAction,
  logMutation,
  logState,
  settingsGetAction,
  settingsGetMutation,
  settingsPutMutation,
  settingsPutAction,
  settingsState,
  systemAction,
  systemMutation,
  systemState
} from '../variables/my'
import { myApi } from '../api'
import { axiosGet, axiosPut, setToast, toastData } from '../tools'
import { sendSocketMessage } from '../hooks/useWS'

export const state = {
  [logState]: [],
  [historyState]: [],
  [systemState]: [],
  [settingsState]: {
    myself_download_value: 2,
    anime1_download_value: 2
  }
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
  },
  [settingsGetAction] (context, value) {
    axiosGet(myApi.settings, context, settingsGetMutation)
  },
  [settingsPutAction] (context, value) {
    axiosPut(myApi.settings, context.state[settingsState], context, settingsPutMutation)
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
  },
  [settingsGetMutation] (state, value) {
    state[settingsState] = value
  },
  [settingsPutMutation] (state, value) {
    state[settingsState] = value
    sendSocketMessage({
      action: 'update_download_value',
      data: value
    })
    setToast(toastData.settingsPutOk)
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
