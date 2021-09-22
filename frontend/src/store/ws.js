export const state = {
  wsRes: {},
  wsClick: {}
}
export const actions = {}

export const mutations = {
  setWsRes (state, value) {
    console.log(value)
    // if (value.type === 'connect') {
    state.wsClick = value
    // } else if (value.type === 'click') {
    //   state.wsClick = value
    // }
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
