import axios from 'axios'
import {
  activeWeekState,
  weekAnimateState,
  animateInfoState,
  loadingState,
  finishListState,
  addAnimateInfoMutation,
  addFinishListMutation,
  changeActiveWeekMutation,
  addWeekAnimateMutation,
  animateInfoAction,
  loadingMutation,
  weekAnimateAction,
  finishListAction,
  finishAnimateUpdateState,
  finishAnimateUpdateButtonState,
  finishAnimateUpdateButtonMutation,
  checkboxAnimateEpisodeState,
  addCheckboxAnimateEpisodeMutation,
  removeCheckboxAnimateEpisodeMutation,
  downloadMyselfAnimateMutation,
  downloadMyselfAnimateState,
  downloadMyselfAnimateGetters,
  finishAnimateState,
  finishAnimateAction,
  addFinishAnimateMutation, searchMyselfAnimateMutation, displayFinishAnimateState, displayFinishAnimateMutation
} from '../variables/variablesMyself'
import { myselfApi } from '../../api'

export const state = {
  [weekAnimateState]: {},
  [activeWeekState]: {},
  [animateInfoState]: {},
  [loadingState]: true,
  [finishListState]: {},
  [finishAnimateUpdateState]: false,
  [finishAnimateUpdateButtonState]: '更新資料',
  [checkboxAnimateEpisodeState]: [],
  [finishAnimateState]: [],
  [displayFinishAnimateState]: []
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
      },
      error => {
        context.commit(addFinishListMutation, error.msg)
      }
    )
  },
  [finishAnimateAction] (context, value) {
    axios.get(myselfApi.finishAnimate).then(
      response => {
        context.commit(addFinishAnimateMutation, response.data)
        context.commit(displayFinishAnimateMutation)
      },
      error => {
        context.commit(addFinishAnimateMutation, error.msg)
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
    } else {
      alert('失敗')
    }
  },
  [addFinishAnimateMutation] (state, value) {
    if (value) {
      state[finishAnimateState] = value
    } else {
      alert('失敗')
    }
  },
  [finishAnimateUpdateButtonMutation] (state, value) {
    state[finishAnimateUpdateButtonState] = value.msg
    state[finishAnimateUpdateState] = value.updating
  },
  [addCheckboxAnimateEpisodeMutation] (state, value) {
    state[checkboxAnimateEpisodeState].push(value)
  },
  [removeCheckboxAnimateEpisodeMutation] (state, value) {
    state[checkboxAnimateEpisodeState].splice(value, 1)
  },
  [downloadMyselfAnimateMutation] (state, value) {
    // console.log(value)
    state[downloadMyselfAnimateState] = value
  },
  [searchMyselfAnimateMutation] (state, value) {
    state[displayFinishAnimateState] = value
  },
  [displayFinishAnimateMutation] (state, value) {
    state[displayFinishAnimateState] = state[finishAnimateState]
  }
}
export const getters = {
  getterWeekAnimate (state) {
    return state[weekAnimateState]
  },
  [downloadMyselfAnimateGetters] (state) {
    return state[downloadMyselfAnimateState]
  }
}

export default {
  state,
  actions,
  mutations,
  getters,
  namespaced: true
}
