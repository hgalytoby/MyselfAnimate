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
    <div class="row">
      <h5>尚未下載</h5>
      <div class="col-sm-2" v-for="data in animateUndone" :key="data.id">
        <BootstrapIcon icon="check2-square" v-show="checkCheckboxArray(data.id)"
                       @click="clickCheckbox(data.id)"/>
        <BootstrapIcon icon="square" v-show="!checkCheckboxArray(data.id)"
                       @click="clickCheckbox(data.id)"/>
        <span>{{ data.name }}</span>
      </div>
      <h5>正在下載</h5>
       <div class="col-sm-2" v-for="data in animateDownloading" :key="data.id">
        <span>{{ data.name }}</span>
      </div>
      <h5>下載完成</h5>
       <div class="col-sm-2" v-for="data in animateDone" :key="data.id">
        <BootstrapIcon class="video-play" icon="play-btn" @click="startFancy(data.video)"/>
        <span>{{ data.name }}</span>
      </div>
    </div>
  </div>
  <button type="button" class="btn btn-primary" @click="downloadAnimate">下載所選的集數</button>
</template>

<script>
import { computed, ref } from 'vue'
import { useStore } from 'vuex'
import {
  animateInfoAction,
  animateInfoState,
  loadingMutation,
  loadingState,
  downloadMyselfAnimateState,
  animateInfoEpisodeInfoAction
} from '../../variables/myself'
import { sendSocketMessage } from '../../hooks/useWS'
import Loading from '../../components/Loading'
import { startFancy } from '../../tools'
import useWindowsFocus from '../../hooks/useWindowsFocus'

export default {
  name: 'Animate',
  props: {
    url: String
  },
  components: { Loading },
  setup (props) {
    const store = useStore()
    const loading = computed(() => store.state.myself[loadingState])
    const animateInfo = computed(() => store.state.myself[animateInfoState])
    const downloadMyselfAnimate = computed(() => {
      return store.state.myself[downloadMyselfAnimateState].filter((item) => item.animate_id === animateInfo.value.id)
    })
    const animateDownloading = computed(() => {
      const downloadingID = downloadMyselfAnimate.value.filter((item) => !item.done).map((item) => item.id)
      return animateInfo.value.episode_info_model.filter((item) => downloadingID.indexOf(item.id) !== -1)
    })
    const animateUndone = computed(() => {
      const downloadingID = downloadMyselfAnimate.value.map((item) => item.id)
      return animateInfo.value.episode_info_model.filter((item) => !item.done && downloadingID.indexOf(item.id) === -1)
    })
    const animateDone = computed(() => {
      const downloadingID = downloadMyselfAnimate.value.filter((item) => item.done).map((item) => item.id)
      return animateInfo.value.episode_info_model.filter((item) => item.done || downloadingID.indexOf(item.id) !== -1)
    })
    const clickCheckboxData = ref([])
    store.commit(`myself/${loadingMutation}`)
    store.dispatch(`myself/${animateInfoAction}`, props.url)
    useWindowsFocus(store.dispatch, `myself/${animateInfoEpisodeInfoAction}`, animateInfo)
    const downloadAnimate = () => {
      sendSocketMessage({
        action: 'download_myself_animate',
        episodes: clickCheckboxData.value,
        id: animateInfo.value.id,
        animateName: animateInfo.value.name
      })
    }

    function clickCheckbox (id) {
      console.log(clickCheckboxData.value.indexOf(id))
      const index = clickCheckboxData.value.indexOf(id)
      if (index === -1) {
        clickCheckboxData.value.push(id)
      } else {
        clickCheckboxData.value.splice(index, 1)
      }
    }

    function checkCheckboxArray (id) {
      return clickCheckboxData.value.indexOf(id) !== -1
    }

    return {
      loading,
      animateInfo,
      downloadAnimate,
      clickCheckbox,
      checkCheckboxArray,
      clickCheckboxData,
      startFancy,
      animateDownloading,
      animateUndone,
      animateDone,
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
