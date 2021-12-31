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

export const state = {
  [animateListState]: [],
  [animateInfoState]: [],
  [downloadAnime1AnimateState]: [],
  [loadingState]: true
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
