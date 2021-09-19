import axios from 'axios'

export const state = {
  weekAnimateData: {},
  activeWeek: {},
  myselfAnimateInfo: {},
  myselfAnimateInfoLoading: true
}
export const actions = {
  weekAnimateAction (context, value) {
    axios.get('/api/myself/week-animate/').then(
      response => {
        context.commit('addWeekAnimateDataMutation', response.data)
        // context.commit('changeActiveWeek', response.data)
      },
      error => {
        context.commit('addWeekAnimateDataMutation', error.msg)
      }
    )
  },
  myselfAnimateInfoAction (context, value) {
    axios.get(`/api/myself/animate-info/?url=${value}`).then(
      response => {
        context.commit('addMyselfAnimateInfoMutation', response.data)
        // context.commit('changeActiveWeek', response.data)
      },
      error => {
        context.commit('addMyselfAnimateInfoMutation', error.msg)
      }
    )
  }
}

export const mutations = {
  addWeekAnimateDataMutation (state, value) {
    if (value) {
      state.weekAnimateData = value
      state.activeWeek = state.weekAnimateData.Monday
    } else {
      alert('失敗')
    }
  },
  changeActiveWeek (state, value) {
    state.activeWeek = state.weekAnimateData[value]
  },
  addMyselfAnimateInfoMutation (state, value) {
    if (value) {
      state.myselfAnimateInfo = value
      state.myselfAnimateInfoLoading = false
    } else {
      alert('失敗')
    }
  },
  initMyselfAnimateInfoLoading (state, value) {
    state.myselfAnimateInfoLoading = true
  }
}
export const getters = {
  getterWeekAnimate (state) {
    return state.weekAnimateData
  }
}

export default {
  state,
  actions,
  mutations,
  getters,
  namespaced: true
}
