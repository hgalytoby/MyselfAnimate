export const state = {
  wsRes: {},
  wsClick: {}
}
export const actions = {}

export const mutations = {
  setWsRes (state, value) {
    console.log('setWsRes', value)
    if (value.type === 'while') {
      state.wsWeekData = value.data
    } else if (value.type === 'click') {
      state.wsClick = value
    }
  }
}
export const getters = {}

export default {
  state,
  actions,
  mutations,
  getters,
  namespaced: true
}
