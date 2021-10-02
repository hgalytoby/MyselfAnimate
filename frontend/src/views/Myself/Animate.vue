<template>
  <div>我是animate</div>
  <div v-if="loading">加載中...</div>
  <div v-else>
    <img :src="animateInfo.image" :alt="animateInfo.name">
    <li>名字: {{ animateInfo.name }}</li>
    <li>作品類型: {{ animateInfo.animate_type }}</li>
    <li>首播日期: {{ animateInfo.premiere_date }}</li>
    <li>播放集數: {{ animateInfo.episode }}</li>
    <li>作者: {{ animateInfo.author }}</li>
    <li>官方網站:
      <a :href="animateInfo.official_website">{{ animateInfo.official_website }}</a>
    </li>
    <li>備註: {{ animateInfo.remarks }}</li>
    <li>synopsis{{ animateInfo.synopsis }}</li>
    <div v-for="data in animateInfo.video" :key="data.url">
      <input type="checkbox" :id="data.name" :value="data" v-model="checkboxAnimateEpisode">
      <label :for="data.name">{{ data.name }}</label>
    </div>
    <button type="button" class="btn btn-primary" @click="downloadAnimate">下載所選的集數</button>
    <button type="button" class="btn btn-primary" @click="saveMyLove">儲存到我的最愛</button>
  </div>

</template>

<script>
import { onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import {
  animateInfoAction,
  animateInfoState, checkboxAnimateEpisodeMutation,
  checkboxAnimateEpisodeState,
  loadingMutation,
  loadingState
} from '../../variables/variablesMyself'
import { sendSocketMessage } from '../../hooks/useWS'

export default {
  name: 'Animate',
  props: {
    url: String
  },
  setup (props) {
    const store = useStore()
    const loading = computed(() => store.state.myself[loadingState])
    const animateInfo = computed(() => store.state.myself[animateInfoState])
    const checkboxAnimateEpisode = computed({
      get () {
        return store.state.myself[checkboxAnimateEpisodeState]
      },
      set (value) {
        store.commit(`myself/${checkboxAnimateEpisodeMutation}`, value)
      }
    })
    store.commit(`myself/${loadingMutation}`)
    onMounted(() => {
      store.dispatch(`myself/${animateInfoAction}`, props.url)
    })
    const downloadAnimate = () => {
      const copy = {}
      Object.assign(copy, animateInfo.value)
      delete copy.video
      sendSocketMessage({
        action: 'downloadMyselfAnimate',
        episodes: checkboxAnimateEpisode.value,
        animateInfo: copy
      })
    }
    function saveMyLove () {
      console.log(animateInfo.value)
    }
    return {
      loading,
      animateInfo,
      checkboxAnimateEpisode,
      downloadAnimate,
      saveMyLove
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
