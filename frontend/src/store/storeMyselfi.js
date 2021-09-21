import axios from 'axios'
import {
  activeWeekState, weekAnimateState, animateInfoState, loadingState, finishListState,
  addAnimateInfoMutation, addFinishListMutation, changeActiveWeekMutation, addWeekAnimateMutation,
  animateInfoAction, loadingMutation, weekAnimateAction, finishListAction
} from '../variables/variablesMyself'
import { myselfApi } from '../../api'

export const state = {
  [weekAnimateState]: {},
  [activeWeekState]: {},
  [animateInfoState]: {},
  [loadingState]: true,
  [finishListState]: {}
}

export const actions = {
  [weekAnimateAction] (context, value) {
    axios.get(myselfApi.weekAnimate).then(
      response => {
        context.commit(addWeekAnimateMutation, response.data)
        // context.commit('changeActiveWeek', response.data)
      },
      error => {
        context.commit(addWeekAnimateMutation, error.msg)
      }
    )
  },
  [animateInfoAction] (context, value) {
    axios.get(`${myselfApi.animateInfo}?url=${value}`).then(
      response => {
        context.commit(addAnimateInfoMutation, response.data)
        // context.commit('changeActiveWeek', response.data)
      },
      error => {
        context.commit(addAnimateInfoMutation, error.msg)
      }
    )
  },
  [finishListAction] (context, value) {
    axios.get(myselfApi.finishList).then(
      response => {
        context.commit(addFinishListMutation, response.data)
        // context.commit('changeActiveWeek', response.data)
      },
      error => {
        context.commit(addFinishListMutation, error.msg)
      }
    )
  }
}

export const mutations = {
  [addWeekAnimateMutation] (state, value) {
    if (value) {
      state[weekAnimateState] = value
      state[activeWeekState] = state[weekAnimateState].Monday
    } else {
      alert('失敗')
    }
  },
  [changeActiveWeekMutation] (state, value) {
    state.activeWeekState = state[weekAnimateState][value]
  },
  [addAnimateInfoMutation] (state, value) {
    if (value) {
      state[animateInfoState] = value
      state[loadingState] = false
    } else {
      alert('失敗')
    }
  },
  [loadingMutation] (state, value) {
    state[loadingState] = true
  },
  [addFinishListMutation] (state, value) {
    if (value) {
      state[finishListState] = value.data
      console.log(state[finishListState])
    } else {
      alert('失敗')
    }
  }
}
export const getters = {
  getterWeekAnimate (state) {
    return state[weekAnimateState]
  }
}

export default {
  state,
  actions,
  mutations,
  getters,
  namespaced: true
}
