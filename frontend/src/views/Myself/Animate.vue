<template>
  <div v-if="loading">
    <Loading/>
  </div>
  <div v-else>
    <div class="card">
      <div class="row g-0">
        <div class="col-sm-12 col-lg-7 col-xl-4 col-xxl-3">
          <img :src="animateInfo.image" :alt="animateInfo.name" class="rounded mx-auto d-block img-thumbnail w-100 p-2">
        </div>
        <div class="col-lg">
          <div class="card-body">
            <h3 class="card-title">{{ animateInfo.name }}</h3>
          </div>
          <ul class="list-group list-group-flush">
            <li class="list-group-item">作品類型: {{ animateInfo.animate_type }}</li>
            <li class="list-group-item">首播日期: {{ animateInfo.premiere_date }}</li>
            <li class="list-group-item">播放集數: {{ animateInfo.episode }}</li>
            <li class="list-group-item">作者: {{ animateInfo.author }}</li>
            <li class="list-group-item">官方網站:
              <a class="link-primary" :href="animateInfo.official_website">{{ animateInfo.official_website }}</a>
            </li>
            <li class="list-group-item">備註: {{ animateInfo.remarks }}</li>
            <li class="list-group-item">
              <h5>劇情簡介</h5>
              {{ animateInfo.synopsis }}
            </li>
          </ul>
        </div>
      </div>
    </div>
    <DownloadStatus :animateInfoObj="animateInfo" :downloadStateArray="downloadMyselfAnimate"
                    action="download_myself_animate"/>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import {
  animateInfoAction,
  animateInfoState,
  loadingMutation,
  loadingState,
  // animateInfoEpisodeInfoAction, downloadMyselfAnimateState
  downloadMyselfAnimateState
} from '../../variables/myself'
import Loading from '../../components/Loading'
// import useWindowsFocus from '../../hooks/useWindowsFocus'
import DownloadStatus from '../../components/AnimateEpisode'

export default {
  name: 'Animate',
  props: {
    url: String
  },
  components: { Loading, DownloadStatus },
  setup (props) {
    const store = useStore()
    const loading = computed(() => store.state.myself[loadingState])
    const animateInfo = computed(() => store.state.myself[animateInfoState])
    store.commit(`myself/${loadingMutation}`)
    store.dispatch(`myself/${animateInfoAction}`, props.url)
    // useWindowsFocus(store.dispatch, `myself/${animateInfoEpisodeInfoAction}`, animateInfo)
    const downloadMyselfAnimate = computed(() => {
      return store.state.myself[downloadMyselfAnimateState].filter((item) => item.animate_id === animateInfo.value.id)
    })
    return {
      loading,
      animateInfo,
      downloadMyselfAnimate
    }
  }
}
</script>

<style lang="scss" scoped>
  @import '~@fancyapps/ui/dist/fancybox.css';

  .video-play {
    font-size: 24px;
  }
</style>
