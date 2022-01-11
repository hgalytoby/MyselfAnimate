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
  downloadMyselfAnimateMutation,
  downloadMyselfAnimateState,
  downloadMyselfAnimateGetters,
  finishAnimateState,
  finishAnimateAction,
  addFinishAnimateMutation,
  searchMyselfAnimateMutation,
  animateInfoEpisodeInfoAction,
  animateInfoEpisodeInfoMutation, searchAnimateAction, searchAnimateMutation
} from '../variables/myself'
import { myselfApi } from '../api'
import { axiosGet, axiosPost, toastData } from '../tools'
import {
  clickAllDownloadCheckBoxMutation,
  clickDownloadCheckBoxMutation,
  downloadCheckBoxMutation,
  downloadCheckBoxState,
  animateCollectState,
  animateCollectAction,
  animateCollectMutation
} from '../variables/my'
import router from '../router'
import { createToast } from 'mosha-vue-toastify'

export const state = {
  [weekAnimateState]: {},
  [animateInfoState]: {},
  [loadingState]: true,
  [finishListState]: [],
  [finishAnimateUpdateState]: false,
  [finishAnimateUpdateButtonState]: '更新資料',
  [finishAnimateState]: [],
  [animateCollectState]: [],
  [downloadMyselfAnimateState]: [],
  [downloadCheckBoxState]: [],
  searchTimer: null
}

export const actions = {
  [weekAnimateAction] (context, value) {
    axiosGet(myselfApi.weekAnimate, context, addWeekAnimateMutation)
  },
  [animateInfoAction] (context, value) {
    axiosPost(myselfApi.animateInfo, value, context, addAnimateInfoMutation)
  },
  [finishListAction] (context, value) {
    axiosGet(myselfApi.finishList, context, addFinishListMutation)
  },
  [finishAnimateAction] (context, value) {
    axiosGet(myselfApi.finishAnimate, context, addFinishAnimateMutation)
  },
  [animateCollectAction] (context, value) {
    axiosGet(myselfApi.animateEpisodeDone, context, animateCollectMutation)
  },
  [animateInfoEpisodeInfoAction] (context, value) {
    if (value.value.id) {
      axiosGet(myselfApi.animateInfoEpisodeInfo(value.value.id), context, animateInfoEpisodeInfoMutation)
    }
  },
  [searchAnimateAction] (context, value) {
    axiosPost(myselfApi.searchAnimate, value, context, searchAnimateMutation)
  }
}

export const mutations = {
  [addWeekAnimateMutation] (state, value) {
    state[weekAnimateState] = value
  },
  [addAnimateInfoMutation] (state, value) {
    state[animateInfoState] = value
    state[loadingState] = false
  },
  [loadingMutation] (state, value) {
    state[loadingState] = true
  },
  [addFinishListMutation] (state, value) {
    state[finishListState] = value.data
  },
  [addFinishAnimateMutation] (state, value) {
    state[finishAnimateState] = value
  },
  [finishAnimateUpdateButtonMutation] (state, value) {
    state[finishAnimateUpdateButtonState] = value.msg
    state[finishAnimateUpdateState] = value.updating
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
    if (state.searchTimer) {
      clearInterval(state.searchTimer)
    }
    state.searchTimer = setTimeout(() => {
      state[finishAnimateState] = value
    }, 950)
  },
  [animateCollectMutation] (state, value) {
    state[animateCollectState] = value
  },
  [animateInfoEpisodeInfoMutation] (state, value) {
    state[animateInfoState].episode_info_model = value
  },
  [downloadCheckBoxMutation] (state, value) {
    state[downloadCheckBoxState].length = 0
  },
  [clickDownloadCheckBoxMutation] (state, value) {
    const index = state[downloadCheckBoxState].indexOf(value)
    if (index !== -1) {
      state[downloadCheckBoxState].splice(index, 1)
    } else {
      state[downloadCheckBoxState].push(value)
    }
  },
  [clickAllDownloadCheckBoxMutation] (state, value) {
    state[downloadCheckBoxState].push(value)
  },
  [searchAnimateMutation] (state, value) {
    if (value.result) {
      setTimeout(() => {
        router.push({
          name: 'MyselfAnimate',
          query: {
            url: JSON.stringify(value.url)
          }
        })
      }, 500)
    } else {
      createToast(...toastData.searchMyselfAnimateFail)
    }
  }
}
export const getters = {
  getterWeekAnimate (state) {
    return state[weekAnimateState]
  },
  [downloadMyselfAnimateGetters] (state) {
    return state[downloadMyselfAnimateState].map((item) => {
      const progress = parseInt(item.count / item.ts_count * 100)
      item.progressValue = !isNaN(progress) ? progress : 0
      item.progressColor = progress > 50 ? 'white' : 'black'
      return item
    })
  }
}

export default {
  state,
  actions,
  mutations,
  getters,
  namespaced: true
}
