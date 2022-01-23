<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-sm">
        <h5 title="尚未下載">尚未下載</h5>
        <div v-for="data in animateUndone" :key="data.id">
          <BootstrapIcon icon="check2-square" v-show="checkCheckboxArray(data.id)"
                         @click="clickCheckbox(data.id)"/>
          <BootstrapIcon icon="square" v-show="!checkCheckboxArray(data.id)"
                         @click="clickCheckbox(data.id)"/>
          <span :title="data.name">{{ data.name }}</span>
        </div>
        <button type="button" class="btn btn-primary" title="下載所選的集數" @click="downloadAnimate">下載所選的集數</button>
      </div>
      <div class="col-sm">
        <h5 title="正在下載">正在下載</h5>
        <div v-for="data in animateDownloading" :key="data.id">
          <span :title="data.name">{{ data.name }}</span>
        </div>
      </div>
      <div class="col-sm">
        <h5 title="下載完成">下載完成</h5>
        <div v-for="data in animateDone" :key="data.id">
          <BootstrapIcon class="video-play" icon="play-btn" @click="startFancy(data.video)"/>
          <span class="episode" :title="data.name">{{ data.name }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref } from 'vue'
import { setToast, startFancy, toastData } from '../tools'
import { sendSocketMessage } from '../hooks/useWS'

export default {
  name: 'DownloadStatus',
  props: {
    animateInfoObj: Object,
    downloadStateArray: Array,
    action: String
  },
  setup (props) {
    const clickCheckboxData = ref([])
    const animateInfo = computed(() => props.animateInfoObj)
    const downloadAnimateArray = computed(() => props.downloadStateArray)
    const animateDownloading = computed(() => {
      const downloadingID = downloadAnimateArray.value.filter((item) => !item.done).map((item) => item.episode_id)
      return animateInfo.value.episode_info_model.filter((item) => downloadingID.indexOf(item.id) !== -1)
    })
    const animateUndone = computed(() => {
      const downloadingID = downloadAnimateArray.value.map((item) => item.episode_id)
      return animateInfo.value.episode_info_model.filter((item) => !item.done && downloadingID.indexOf(item.id) === -1)
    })
    const animateDone = computed(() => {
      const downloadingID = downloadAnimateArray.value.filter((item) => item.done).map((item) => item.episode_id)
      const downloadingVideoPath = new Map(downloadAnimateArray.value.map(i => [i.episode_id, i.video]))
      return animateInfo.value.episode_info_model.filter((item) => item.done || downloadingID.indexOf(item.id) !== -1).map((item) => {
        if (downloadingVideoPath.get(item.id)) {
          item.video = downloadingVideoPath.get(item.id)
        }
        return item
      })
    })
    const downloadAnimate = () => {
      sendSocketMessage({
        action: props.action,
        episodes: clickCheckboxData.value,
        id: animateInfo.value.id,
        animateName: animateInfo.value.name
      })
      clickCheckboxData.value = []
      setToast(toastData.downloadArrayCreateAnimate(animateInfo.value.name))
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
      downloadAnimate,
      downloadAnimateArray
    }
  }
}
</script>

<style scoped lang="scss">
@import "./src/assets/scss/tools";
</style>
