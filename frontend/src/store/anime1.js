import {
  animateInfoAction,
  animateInfoMutation,
  animateInfoState,
  animateListAction,
  animateListMutation,
  animateListState,
  downloadAnime1AnimateGetters,
  downloadAnime1AnimateMutation,
  downloadAnime1AnimateState,
  loadingMutation,
  loadingState
} from '../variables/anime1'
import { axiosGet, axiosPost } from '../tools'
import { anima1Api } from '../api'
import {
  clickAllDownloadCheckBoxMutation,
  clickDownloadCheckBoxMutation,
  downloadCheckBoxMutation,
  downloadCheckBoxState
} from '../variables/my'

export const state = {
  [animateListState]: [],
  [animateInfoState]: [],
  [downloadAnime1AnimateState]: [],
  [loadingState]: true,
  [downloadCheckBoxState]: []
}

export const actions = {
  [animateListAction] (context, value) {
    axiosGet(anima1Api.animateList, context, animateListMutation)
  },
  [animateInfoAction] (context, value) {
    axiosPost(anima1Api.animateInfo(value.url), value.animateData, context, animateInfoMutation)
  }
}

export const mutations = {
  [animateListMutation] (state, value) {
    state[animateListState] = value
  },
  [animateInfoMutation] (state, value) {
    state[animateInfoState] = value
    state[loadingState] = false
  },
  [downloadAnime1AnimateMutation] (state, value) {
    state[downloadAnime1AnimateState] = value
  },
  [loadingMutation] (state, value) {
    state[loadingState] = true
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
  }
}

export const getters = {
  [downloadAnime1AnimateGetters] (state) {
    return state[downloadAnime1AnimateState].map((item) => {
      item.progressValue = item.progress_value
      item.progressColor = item.progress_value > 50 ? 'white' : 'black'
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
