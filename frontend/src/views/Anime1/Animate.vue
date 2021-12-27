<template>
  <div v-if="loading">
    <Loading/>
  </div>
  <div v-else>
    <h1>{{ animateInfo.name }}</h1>
    <span>集數: {{ animateInfo.episode }}</span>
    <span>年份: {{ animateInfo.years }}</span>
    <span>季節: {{ animateInfo.season }}</span>
    <span>字幕組: {{ animateInfo.subtitle_group }}</span>
    <DownloadStatus :animateInfoObj="animateInfo" :downloadStateArray="downloadAnime1Animate"
                    action="download_anime1_animate"/>
  </div>
</template>

<script>
import { useStore } from 'vuex'
import { computed } from 'vue'
import {
  animateInfoAction,
  animateInfoState,
  downloadAnime1AnimateState,
  loadingMutation,
  loadingState
} from '../../variables/anime1'
import DownloadStatus from '../../components/DownloadStatus'
import Loading from '../../components/Loading'

export default {
  name: 'Animate',
  props: {
    url: String,
    animateData: String
  },
  components: { Loading, DownloadStatus },
  setup (props) {
    const store = useStore()
    const loading = computed(() => store.state.anime1[loadingState])
    const animateInfo = computed(() => store.state.anime1[animateInfoState])
    store.commit(`anime1/${loadingMutation}`)
    store.dispatch(`anime1/${animateInfoAction}`, {
      animateData: props.animateData !== undefined ? JSON.parse(props.animateData) : null,
      url: props.url
    })
    const downloadAnime1Animate = computed(() => {
      return store.state.anime1[downloadAnime1AnimateState].filter((item) => item.animate_id === animateInfo.value.id)
    })
    return {
      animateInfo,
      downloadAnime1Animate,
      loading
    }
  }
}
</script>

<style scoped>

</style>
