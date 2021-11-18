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
      <div class="col-sm-2" v-for="data in animateInfo.episode_info_model" :key="data.id">
        <BootstrapIcon icon="check2-square" v-show="checkCheckboxArray(data.id, data.download)"
                       @click="clickCheckbox(data.id)"/>
        <BootstrapIcon icon="square" v-show="!checkCheckboxArray(data.id, data.download)"
                       @click="clickCheckbox(data.id)"/>
        <!--      <input type="checkbox" :id="data.id" :value="data" v-model="checkboxAnimateEpisode">-->
        <BootstrapIcon class="video-play" icon="play-btn" v-if="data.done" @click="startFancy(data.video)"/>
        <BootstrapIcon class="video-play" icon="pause-circle"/>
        <span>{{ data.name }}</span>
      </div>
      {{checkboxAnimateEpisode}}
    </div>
  </div>
  <button type="button" class="btn btn-primary" @click="downloadAnimate">下載所選的集數</button>
</template>

<script>
import { onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import {
  animateInfoAction,
  animateInfoState, addCheckboxAnimateEpisodeMutation,
  checkboxAnimateEpisodeState,
  loadingMutation,
  loadingState, removeCheckboxAnimateEpisodeMutation
} from '../../variables/myself'
import { sendSocketMessage } from '../../hooks/useWS'
import Loading from '../../components/Loading'
import { startFancy } from '../../tools'

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
    const checkboxAnimateEpisode = computed({
      get () {
        return store.state.myself[checkboxAnimateEpisodeState]
      },
      set (value) {
        store.commit(`myself/${addCheckboxAnimateEpisodeMutation}`, value)
      }
    })
    store.commit(`myself/${loadingMutation}`)
    onMounted(() => {
      store.dispatch(`myself/${animateInfoAction}`, props.url)
    })
    const downloadAnimate = () => {
      sendSocketMessage({
        action: 'download_myself_animate',
        episodes: checkboxAnimateEpisode.value,
        id: animateInfo.value.id,
        animateName: animateInfo.value.name
      })
    }

    function clickCheckbox (id) {
      const index = checkboxAnimateEpisode.value.indexOf(id)
      if (index === -1) {
        store.commit(`myself/${addCheckboxAnimateEpisodeMutation}`, id)
      } else {
        store.commit(`myself/${removeCheckboxAnimateEpisodeMutation}`, index)
      }
    }

    function checkCheckboxArray (id, download) {
      // console.log(checkboxAnimateEpisode.value[0])
      return checkboxAnimateEpisode.value.indexOf(id) !== -1 || download
    }
    return {
      loading,
      animateInfo,
      checkboxAnimateEpisode,
      downloadAnimate,
      clickCheckbox,
      checkCheckboxArray,
      startFancy
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
