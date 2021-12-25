<template>
  <div>
    <h1>{{ animateInfo.name }}</h1>
    <span>集數: {{ animateInfo.episode }}</span>
    <span>年份: {{ animateInfo.years }}</span>
    <span>季節: {{ animateInfo.season }}</span>
    <span>字幕組: {{ animateInfo.subtitle_group }}</span>
  </div>
<!--  {{animateInfo}}-->
  <div v-for="episode in animateInfo.episode_info_model" :key="episode.id">
    <span>{{ episode.name }}</span>
    <span>{{ episode.published_updated_date }}</span>
    <span>{{ episode.updated }}</span>
    <BootstrapIcon class="video-play" icon="play-btn" v-if="episode.done" @click="startFancy(episode.video)"/>
    <BootstrapIcon class="video-play" icon="pause-circle" v-else/>
  </div>
</template>

<script>
import { useStore } from 'vuex'
import { computed } from 'vue'
import { animateInfoAction, animateInfoState } from '../../variables/anime1'
import { startFancy } from '../../tools'
import { sendSocketMessage } from '../../hooks/useWS'
// import { sendSocketMessage } from '../../hooks/useWS'

export default {
  name: 'Animate',
  props: {
    url: String,
    animateData: String
  },
  setup (props) {
    const store = useStore()
    const animateInfo = computed(() => store.state.anime1[animateInfoState])
    store.dispatch(`anime1/${animateInfoAction}`, {
      animateData: props.animateData !== undefined ? JSON.parse(props.animateData) : null,
      url: props.url
    })
    // const checkboxAnimateEpisode = computed({
    //   get () {
    //     return store.state.anime1[checkboxAnimateEpisodeState]
    //   },
    //   set (value) {
    //     store.commit(`anime1/${CheckboxAnimateEpisodeMutation}`, value)
    //   }
    // })
    const downloadAnimate = () => {
      sendSocketMessage({
        action: 'download_myself_animate',
        // episodes: checkboxAnimateEpisode.value,
        id: animateInfo.value.id,
        animateName: animateInfo.value.name
      })
    }

    return {
      animateInfo,
      startFancy,
      downloadAnimate
    }
  }
}
</script>

<style scoped>

</style>
