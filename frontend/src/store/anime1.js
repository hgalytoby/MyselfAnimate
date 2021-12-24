import {
  animateInfoAction,
  animateInfoMutation,
  animateInfoState,
  animateListAction,
  animateListMutation,
  animateListState
} from '../variables/anime1'
import { axiosGet, axiosPost } from '../tools'
import { anima1Api } from '../api'

export const state = {
  [animateListState]: [],
  [animateInfoState]: []
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
