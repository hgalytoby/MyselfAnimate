<template>
  <button type="button" class="btn btn-success" @click="clearFinishDownload">清除已完成</button>
  <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#exampleModal">
    刪除動漫
  </button>
  <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">刪除動漫</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          確定要刪除勾選的動漫?
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-danger" @click="deleteAnimate" data-bs-dismiss="modal">確認</button>
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
        </div>
      </div>
    </div>
  </div>
  <div class="table-responsive">
    <table class="table table-hover" style="word-wrap:break-word;word-break:break-all;white-space:normal;">
      <thead>
      <tr class="table">
        <th scope="col" @click="clickCheckBoxAll">
          <BootstrapIcon v-show="!checkBoxAll" icon="square"/>
          <BootstrapIcon class="download-checked" v-show="checkBoxAll" icon="check2-square"/>
        </th>
        <th scope="col">播放</th>
        <th scope="col">動漫名字</th>
        <th scope="col">集數</th>
        <th scope="col">狀況</th>
        <th scope="col">下載進度</th>
      </tr>
      </thead>
      <tbody>
      <tr class="align-middle" v-for="animate in downloadMyselfAnimateArray" :key="animate.id">
        <td style="width: 2%;" @click="clickDownloadCheckBox(animate.id)">
          <BootstrapIcon v-show="!filterDownloadCheckBox(animate.id)" icon="square"/>
          <BootstrapIcon class="download-checked" v-show="filterDownloadCheckBox(animate.id)" icon="check2-square"/>
        </td>
        <td class="text-center video-play" style="width: 4%">
          <BootstrapIcon v-if="animate.video" icon="play-btn" @click="startFancy(animate.video)"/>
          <BootstrapIcon v-else icon="pause-circle"/>
        </td>
        <td>{{ animate.animate_name }}</td>
        <td>{{ animate.episode_name }}</td>
        <td>{{ animate.status }}</td>
        <td>
          <div class="progress">
            <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar"
                 :aria-valuenow="computeProgressRate(animate.count, animate.ts_count)"
                 aria-valuemin="0" aria-valuemax="100"
                 :style="`width: ${computeProgressRate(animate.count, animate.ts_count)}%`">
              {{ computeProgressRate(animate.count, animate.ts_count) }}%
            </div>
          </div>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { useStore } from 'vuex'
import { downloadMyselfAnimateGetters } from '../variables/variablesMyself'
import { computed } from 'vue'
import { useStartFancy } from '../hooks/useFancybox'
import { sendSocketMessage } from '../hooks/useWS'

export default {
  name: 'MyDownload',
  setup: function () {
    const store = useStore()
    const downloadCheckBox = []
    const downloadMyselfAnimateArray = computed(() => store.getters[`myself/${downloadMyselfAnimateGetters}`])

    function computeProgressRate (count, tsCount) {
      const result = parseInt(count / tsCount * 100)
      return !isNaN(result) ? result : 0
    }
    const clearFinishDownload = () => {
      sendSocketMessage({
        action: 'clear_finish_myself_animate'
      })
    }
    function deleteAnimate () {
      // sendSocketMessage({
      //   action: 'delete_myself_download_animate'
      // })
    }
    function filterDownloadCheckBox (downloadID) {
      return this.downloadCheckBox.indexOf(downloadID) !== -1
    }
    function clickDownloadCheckBox (downloadID) {
      const index = this.downloadCheckBox.indexOf(downloadID)
      if (index !== -1) {
        this.downloadCheckBox.splice(index, 1)
      } else {
        this.downloadCheckBox.push(downloadID)
      }
    }
    const checkBoxAll = computed(() => {
      if (downloadMyselfAnimateArray.value && downloadCheckBox) {
        return downloadMyselfAnimateArray.value.length === downloadCheckBox.length
      }
      return false
    })
    function clickCheckBoxAll () {
      console.log(checkBoxAll.value)
      if (checkBoxAll.value) {
        downloadCheckBox.length = 0
      } else {
        // downloadMyselfAnimateArray.value.map((animate) => animate.id))
        downloadMyselfAnimateArray.value.forEach((animate) => {
          if (downloadCheckBox.indexOf(animate.id) === -1) {
            downloadCheckBox.push(animate.id)
          }
        })
      }
    }
    const startFancy = useStartFancy
    return {
      downloadMyselfAnimateArray,
      computeProgressRate,
      startFancy,
      clearFinishDownload,
      deleteAnimate,
      downloadCheckBox,
      filterDownloadCheckBox,
      clickDownloadCheckBox,
      checkBoxAll,
      clickCheckBoxAll
    }
  }
}
</script>

<style lang="scss" scoped>
  @import '~@fancyapps/ui/dist/fancybox.css';

  .animate-name {
    text-overflow: ellipsis;
  }

  .video-play {
    font-size: 24px;
  }

  .trash {
    font-size: 20px;
  }
  .trash2 {
    font-size: 20px;
  }
  .download-checked {
    font-size: 18px;
  }
</style>
