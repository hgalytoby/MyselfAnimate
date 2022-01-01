<template>
  <transition appear name="animate__animated animate__bounce" enter-active-class="animate__fadeIn"
              leave-active-class="animate__fadeOut">
    <div class="table-responsive">
      <table class="table table-hover" style="word-wrap:break-word;word-break:break-all;white-space:normal;">
        <thead>
        <tr class="table">
          <th scope="col" @click="clickAllDownloadCheckBox">
            <BootstrapIcon v-show="!checkBoxAll" icon="square"/>
            <BootstrapIcon class="download-checked" v-show="checkBoxAll" icon="check2-square"/>
          </th>
          <th scope="col">播放</th>
          <th scope="col">下載順序</th>
          <th scope="col">動漫名字</th>
          <th scope="col">集數</th>
          <th scope="col">狀況</th>
          <th scope="col">下載進度</th>
        </tr>
        </thead>
        <tbody>
        <tr class="align-middle" v-for="(animate, index) of downloadAnimateData" :key="animate.id">
          <td>
            <BootstrapIcon v-show="!filterDownloadCheckBox(animate.id)" @click="clickDownloadCheckBox(animate.id)"
                           icon="square"/>
            <BootstrapIcon class="download-checked" v-show="filterDownloadCheckBox(animate.id)"
                           @click="clickDownloadCheckBox(animate.id)" icon="check2-square"/>
          </td>
          <td class="video-play">
            <BootstrapIcon v-if="animate.done" icon="play-btn" @click="startFancy(animate.video)"/>
            <BootstrapIcon v-else icon="pause-circle"/>
          </td>
          <td>
            <BootstrapIcon class="order me-3" @click="orderUpOrDown('up', index)" icon="arrow-up-circle"/>
            <BootstrapIcon class="order" @click="orderUpOrDown('down', index)" icon="arrow-down-circle"/>
          </td>
          <td>{{ animate.animate_name }}</td>
          <td>{{ animate.episode_name }}</td>
          <td>{{ animate.status }}</td>
          <td>
            <div class="progress">
              <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar"
                   :aria-valuenow="animate.progressValue"
                   aria-valuemin="0" aria-valuemax="100"
                   :style="`width: ${animate.progressValue}%`">
              </div>
              <span class="progress-value" :style="{color: animate.progressColor}">{{ animate.progressValue }}%</span>
            </div>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </transition>
</template>

<script>
import { sendSocketMessage } from '../hooks/useWS'
import { computed } from 'vue'
import { startFancy } from '../tools'
import {
  clickAllDownloadCheckBoxMutation,
  clickDownloadCheckBoxMutation,
  downloadCheckBoxMutation
} from '../variables/my'
import { useStore } from 'vuex'

export default {
  name: 'AnimateDownload',
  props: {
    animate: String,
    orderAction: String,
    downloadAnimateData: Array,
    downloadCheckBox: Array
  },
  setup (props) {
    const store = useStore()
    const downloadAnimateArray = computed(() => props.downloadAnimateData)
    const downloadCheckBoxArray = computed(() => props.downloadCheckBox)
    const checkBoxAll = computed(() => {
      if (downloadAnimateArray.value && downloadCheckBoxArray.value) {
        if (downloadAnimateArray.value.length > 0) {
          return downloadAnimateArray.value.length === downloadCheckBoxArray.value.length
        }
      }
      return false
    })

    function filterDownloadCheckBox (downloadID) {
      return downloadCheckBoxArray.value.indexOf(downloadID) !== -1
    }

    function clickDownloadCheckBox (downloadID) {
      store.commit(`${props.animate}/${clickDownloadCheckBoxMutation}`, downloadID)
      // const index = downloadCheckBoxArray.value.indexOf(downloadID)
      // if (index !== -1) {
      //   this.downloadCheckBox.splice(index, 1)
      // } else {
      //   this.downloadCheckBox.push(downloadID)
      // }
    }

    function clickAllDownloadCheckBox () {
      if (checkBoxAll.value) {
        store.commit(`${props.animate}/${downloadCheckBoxMutation}`)
      } else {
        downloadAnimateArray.value.forEach((animate) => {
          if (downloadCheckBoxArray.value.indexOf(animate.id) === -1) {
            store.commit(`${props.animate}/${clickAllDownloadCheckBoxMutation}`, animate.id)
          }
        })
      }
    }

    function orderUpOrDown (method, index) {
      sendSocketMessage({
        action: props.orderAction,
        method,
        index
      })
    }

    return {
      startFancy,
      filterDownloadCheckBox,
      clickDownloadCheckBox,
      checkBoxAll,
      clickAllDownloadCheckBox,
      orderUpOrDown,
      downloadAnimateArray
    }
  }
}
</script>

<style lang="scss" scoped>
  @import '~@fancyapps/ui/dist/fancybox.css';

  .animate-name {
    text-overflow: ellipsis;
  }

  .video-play, .order {
    font-size: 24px;
  }

  .download-checked {
    font-size: 18px;
  }

  .progress {
    position: relative;
  }

  .progress span {
    position: absolute;
    left: 0;
    width: 100%;
    text-align: center;
    z-index: 2;
  }
</style>
