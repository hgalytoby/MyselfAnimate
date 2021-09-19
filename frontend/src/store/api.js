import axios from 'axios'

export const state = {
  weekAnimateData: {},
  activeWeek: {}
}
export const actions = {
  weekAnimateAction (context, value) {
    console.log(1)
    axios.get('/api/week-animate/').then(
      response => {
        console.log(response.data)
        context.commit('addWeekAnimateDataMutation', response.data)
        // context.commit('changeActiveWeek', response.data)
      },
      error => {
        context.commit('addWeekAnimateDataMutation', error.msg)
      }
    )
  }
}

export const mutations = {
  addWeekAnimateDataMutation (state, value) {
    console.log(value)
    if (value) {
      console.log('state', state, 'this', this)
      state.weekAnimateData = value
      state.activeWeek = state.weekAnimateData.Monday
    } else {
      alert('失敗')
    }
  },
  changeActiveWeek (state, value) {
    console.log(value)
    state.activeWeek = state.weekAnimateData[value]
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
