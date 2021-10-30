import axios from 'axios'
import {
  weekAnimateState,
  animateInfoState,
  loadingState,
  finishListState,
  addAnimateInfoMutation,
  addFinishListMutation,
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
  addFinishAnimateMutation,
  searchMyselfAnimateMutation,

  myLogState, myLogAction, myLogMutation
} from '../variables/variablesMyself'
import { myselfApi } from '../../api'

export const state = {
  [weekAnimateState]: {},
  [animateInfoState]: {},
  [loadingState]: true,
  [finishListState]: {},
  [finishAnimateUpdateState]: false,
  [finishAnimateUpdateButtonState]: '更新資料',
  [checkboxAnimateEpisodeState]: [],
  [finishAnimateState]: [],
  [myLogState]: [],
  searchTimer: null
}

export const actions = {
  [weekAnimateAction] (context, value) {
    axios.get(myselfApi.weekAnimate).then(
      response => {
        context.commit(addWeekAnimateMutation, response.data)
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
      },
      error => {
        context.commit(addFinishAnimateMutation, error.msg)
      }
    )
  },
  [myLogAction] (context, value) {
    axios.get(myselfApi.myLog).then(
      response => {
        context.commit(myLogMutation, response.data)
      },
      error => {
        context.commit(myLogMutation, error.msg)
      }
    )
  }
}

export const mutations = {
  [addWeekAnimateMutation] (state, value) {
    if (value) {
      state[weekAnimateState] = value
    } else {
      alert('失敗')
    }
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
    state[downloadMyselfAnimateState] = value
  },
  [searchMyselfAnimateMutation] (state, value) {
    if (Object.keys(state[finishAnimateState]).length > 0) {
      const count = state[finishAnimateState].data.length
      for (let i = 0; i < count; i++) {
        state[finishAnimateState].data.pop()
      }
    }
    if (state.timer) {
      clearInterval(state.timer)
    }
    state.timer = setTimeout(() => {
      state[finishAnimateState] = value
    }, 950)
  },
  [myLogMutation] (state, value) {
    if (value) {
      state[myLogState] = value
    } else {
      alert('失敗')
    }
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
