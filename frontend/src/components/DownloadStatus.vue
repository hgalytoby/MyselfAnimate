<template>
    <div class="container">
      <div class="row">
        <div class="col-sm">
          <h5>尚未下載</h5>
          <div v-for="data in animateUndone" :key="data.id">
            <BootstrapIcon icon="check2-square" v-show="checkCheckboxArray(data.id)"
                           @click="clickCheckbox(data.id)"/>
            <BootstrapIcon icon="square" v-show="!checkCheckboxArray(data.id)"
                           @click="clickCheckbox(data.id)"/>
            <span>{{ data.name }}</span>
          </div>
          <button type="button" class="btn btn-primary" @click="downloadAnimate">下載所選的集數</button>
        </div>
        <div class="col-sm">
          <h5>正在下載</h5>
          <div v-for="data in animateDownloading" :key="data.id">
            <span>{{ data.name }}</span>
          </div>
        </div>
        <div class="col-sm">
          <h5>下載完成</h5>
          <div v-for="data in animateDone" :key="data.id">
            <BootstrapIcon class="video-play" icon="play-btn" @click="startFancy(data.video)"/>
            <span>{{ data.name }}</span>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import { computed, ref } from 'vue'
import { startFancy } from '../tools'
import { sendSocketMessage } from '../hooks/useWS'

export default {
  name: 'DownloadStatus',
  props: {
    animateInfoObj: Object,
    downloadStateArray: Array
  },
  setup (props) {
    const clickCheckboxData = ref([])
    const animateInfo = computed(() => props.animateInfoObj)
    const downloadMyselfAnimate = computed(() => props.downloadStateArray)
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
      clickCheckboxData,
      animateDownloading,
      animateUndone,
      animateDone,
      clickCheckbox,
      checkCheckboxArray,
      startFancy,
      downloadAnimate
    }
  }
}
</script>

<style scoped>

</style>
